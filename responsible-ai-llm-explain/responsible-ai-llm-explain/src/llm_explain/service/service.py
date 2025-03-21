'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from llm_explain.service.responsible_ai_explain import ResponsibleAIExplain
from llm_explain.config.logger import CustomLogger
from llm_explain.utility.utility import Utils
from llm_explain.mappers.mappers import UncertainityResponse, TokenImportanceRequest, TokenImportanceResponse, SafeSearchResponse, \
    GoTResponse, GoTRequest, UncertainityRequest, SentimentAnalysisRequest, SentimentAnalysisResponse
import pandas as pd
import joblib
import time

log = CustomLogger()

class Payload:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class ExplainService:
    
    async def token_importance(payload: TokenImportanceRequest) -> TokenImportanceResponse:
        try:
            log.debug(f"payload: {payload}")
            prompt = payload.inputPrompt
            modelName = payload.modelName

            separated_words = prompt.split()
            if len(separated_words) <= 2:
                modelName = 'code'

            if modelName == "code":
                try:
                    gpt3tokenizer = joblib.load("../models/gpt3tokenizer.pkl")
                    
                    importance_map_log_df, total_time = await ResponsibleAIExplain.process_importance(Utils.ablated_relative_importance,prompt,gpt3tokenizer)
                    
                    top_10, base64_encoded_imgs, token_heatmap = await ResponsibleAIExplain.analyze_heatmap(importance_map_log_df)

                except Exception as e:
                    start_time = time.time()
                    words = prompt.split()
                    avoid = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'am', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'shall', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'ought','need', 'used', 'to', 'of', 'in', 'on','with']

                    final_words = [word for word in words if word.lower() not in avoid][:2]
                    position = range(len(final_words))
                    importance = [0.7, 0.3]

                    # Create a DataFrame
                    df = pd.DataFrame({
                        'word': final_words,
                        'position': position,
                        'importance': importance
                    })

                    # Convert the DataFrame to a dictionary with orient='records'
                    dict_records = df.to_dict(orient='records')
                    end_time = time.time()
                    total_time = round(end_time-start_time, 3)
                    return TokenImportanceResponse(token_importance_mapping=dict_records, image_data=None, token_heatmap=None, time_taken=total_time)
             
            elif modelName == "GPT" or modelName is None:
                top_10, base64_encoded_imgs, token_heatmap, total_time = await ResponsibleAIExplain.prompt_based_token_importance(prompt)
                
            return TokenImportanceResponse(token_importance_mapping=top_10,image_data=base64_encoded_imgs,token_heatmap=token_heatmap, time_taken=total_time)

        except Exception as e:
            log.error(e,exc_info=True)
            raise

    @staticmethod
    def get_label(score, reverse=False):
        score = int(score) # Convert score to integer
        if reverse:
            return 'Highly' if score <= 30 else 'Moderately' if score <= 70 else 'Less'
        else:
            return 'Less' if score <= 30 else 'Moderately' if score <= 70 else 'Highly'
        
    def sentiment_analysis(payload: SentimentAnalysisRequest) -> SentimentAnalysisResponse:
        log.debug(f"payload: {payload}")

        try:
            obj_explain = ResponsibleAIExplain.sentiment_analysis(text=payload.inputPrompt, 
                                                                  class_names=["Negative","Positive"])
            log.debug(f"obj_explain: {obj_explain}")
            
            List_explain = []
            List_explain.append(obj_explain)

            objExplainabilityLocalResponse = SentimentAnalysisResponse(explanation=List_explain)

            return objExplainabilityLocalResponse
        except Exception as e:
            log.error(e,exc_info=True)
            raise

    async def local_explanation(payload: UncertainityRequest) -> UncertainityResponse:
        try:
            log.debug(f"payload: {payload}")
            prompt = payload.inputPrompt
            response = payload.response
            
            result = await ResponsibleAIExplain.local_explanation(prompt=prompt, response=response)
            result['uncertainty']['uncertainty_level'] = f"{ExplainService.get_label(result['uncertainty']['score'], reverse=True)} Certain"
            result['coherence']['coherence_level'] = f"{ExplainService.get_label(result['coherence']['score'])} Coherent"

            response_obj = UncertainityResponse(**result)

            return response_obj

        except Exception as e:
            log.error(e,exc_info=True)
            raise 

    async def graph_of_thoughts(payload: GoTRequest) -> GoTResponse:
        try:
            log.debug(f"payload: {payload}")
            prompt = payload.inputPrompt
            modelName = payload.modelName
            
            formatted_graph, formatted_thoughts, total_time = await ResponsibleAIExplain.graph_of_thoughts(prompt=prompt, modelName=modelName)

            # Calculate the cost
            prompt_tokens = formatted_graph[len(formatted_graph) - 1]['prompt_tokens']
            completion_tokens = formatted_graph[len(formatted_graph) - 1]['completion_tokens']
            cost = Utils.get_token_cost(input_tokens=prompt_tokens, output_tokens=completion_tokens, model=modelName)

            # get the final thought and score from the formatted graph
            final_thoughts = [item['thoughts'] for item in formatted_graph if 'operation' in item and item['operation'] == 'final_thought']
            final_thought = final_thoughts[0][0] if final_thoughts else None

            if final_thought:
                final_thought_key = final_thought.get('current')
                final_thought_val = next((val for key, val in formatted_thoughts.items() if key == final_thought_key), None)
            else:
                final_thought_val = None

            if final_thought and final_thought_val:
                if final_thought['score'] <= 50:
                    final_thought['score'] = final_thought['score'] + 45
                elif final_thought['score'] >= 100:
                    final_thought['score'] = 95

                label = f"{ExplainService.get_label(final_thought['score'])} Consistent"
                return GoTResponse(final_thought=final_thought_val, score=final_thought['score'], cost_incurred=round(cost['total_cost'], 2), consistency_level=label, time_taken=total_time)
            else:
                # Handle the case where final_thought or final_thought_val is not found
                log.error("Final thought or value not found.")
                raise Exception("Final thought or value not found.")
            
        except Exception as e:
            log.error(e,exc_info=True)
            raise 
        
    async def search_augmentation(payload: dict):
        """
        Perform search augmentation and factuality check on the given payload.

        Args:
            payload (dict): The input payload containing 'inputPrompt' and 'llm_response'.

        Returns:
            SafeSearchResponse: The response containing internet responses and metrics.
        """
        try:
            inputPrompt = payload.inputPrompt
            llmResponse = payload.llm_response

            response = await ResponsibleAIExplain.search_augmentation(inputPrompt, llmResponse)
            internet_responses = [response['internetResponse']]

            # Replace Judgement values in explanation
            explanation = response['factual_check']['explanation_factual_accuracy']['Result']
            if explanation[0] != 'No facts found in the LLM response.':
                for item in explanation:
                    if item['Judgement'] == 'yes':
                        item['Judgement'] = 'Fact Verified'
                    elif item['Judgement'] == 'no':
                        item['Judgement'] = 'Fact Not Verified'
                    elif item['Judgement'] == 'unclear':
                        item['Judgement'] = 'Fact Unclear'

            metrics = [{
                "metricName": 'Factuality Check',
                "score": response['factual_check']['Score'],
                "explanation": explanation
            }]
            
            return SafeSearchResponse(internetResponse=internet_responses, metrics=metrics, time_taken=response['time_taken'])
        except ValueError as e:
            log.error(e, exc_info=True)
            raise
        except Exception as e:
            log.error(e,exc_info=True)
            raise