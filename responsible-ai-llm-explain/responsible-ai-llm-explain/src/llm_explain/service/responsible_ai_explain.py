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

from llm_explain.utility.query_serper import GoogleSerperAPIWrapper
from llm_explain.utility import got as GraphOfThoughts
from llm_explain.utility.prompts.base import Prompt
from llm_explain.config.logger import CustomLogger
from llm_explain.utility.utility import Utils
from llm_explain.utility.azure import Azure
from json.decoder import JSONDecodeError
import pandas as pd
import time
import json
import ast


log = CustomLogger()

class ResponsibleAIExplain:

    @staticmethod
    def llm_response_to_json(response):
        """
        Converts a substring of the given response that is in JSON format into a Python dictionary.
        
        This function searches for the first occurrence of '{' and the last occurrence of '}' to find the JSON substring.
        It then attempts to parse this substring into a Python dictionary. If the parsing is successful, the dictionary
        is returned. If the substring is not valid JSON, the function will return None.
        
        Parameters:
        - response (str): The response string that potentially contains JSON content.
        
        Returns:
        - dict: A dictionary representation of the JSON substring found within the response.
        - None: If no valid JSON substring is found or if an error occurs during parsing.
        """
        try:
            result = None # Initialize result to None in case no valid JSON is found

            # Find the start index of the first '{' character and end index of the last '}' character
            start_index = response.find('{')
            end_index = response.rfind('}')

            # Check if both '{' and '}' are found and '{' comes before '}'
            if start_index != -1 and end_index != -1 and end_index > start_index:
                json_content = response[start_index:end_index+1] # Extract the substring that is potentially in JSON format
                result = json.loads(json_content) # Attempt to parse the JSON substring into a Python dictionary
            
            return result
        
        except Exception as e:
            # Log the exception if any error occurs during parsing
            log.error(f"An error occurred while parsing JSON from response: {e}", exc_info=True)
            raise ValueError("An error occurred while parsing JSON from response.")

    async def analyze_heatmap(df_input):
        base64_encoded_imgs=[]
        try:
            
            df = df_input.copy()

            if "token" not in df.columns or "importance_value" not in df.columns:
                raise ValueError("The DataFrame must contain 'token' and 'importance_value' columns.")

            df["Position"] = range(len(df))
            
            top_10_important = df.nlargest(10, 'importance_value')
            top_10=top_10_important.to_dict(orient='records')

            base64_encoded_imgs = None
            html_string = None
            return top_10,base64_encoded_imgs,html_string
        except Exception as e:
            log.error(e, exc_info=True)
            raise
        
    @staticmethod
    def normalize_scores(dict_list):
        try:
            # Calculate the total sum of all importance scores
            total_sum = sum(d['importance_score'] for d in dict_list)
            
            # If the total sum is zero, return the original list (to handle cases where all scores are zero)
            if total_sum == 0:
                return dict_list

            # Normalize the scores to ensure their sum equals 100
            normalized_scores = [round((d['importance_score'] / total_sum) * 100) for d in dict_list]
            
            # Adjust the scores to ensure their sum is exactly 100
            adjustment = 100 - sum(normalized_scores)
            normalized_scores[0] += adjustment

            # Update the original list with normalized scores
            for i, d in enumerate(dict_list):
                d['importance_score'] = normalized_scores[i]
            
            return dict_list
        
        except KeyError as e:
            log.error(f"KeyError: Missing key in one of the dictionaries - {e}")
            raise KeyError(f"KeyError: Missing key in one of the dictionaries - {e}")
        except TypeError as e:
            log.error(f"TypeError: Invalid type encountered - {e}")
            raise TypeError(f"TypeError: Invalid type encountered - {e}")
        except Exception as e:
            log.error(f"An unexpected error occurred: {e}")
            raise
    
    @staticmethod
    def filter_token_importance(scores, anchors):
        import re
        try:
            # Split each phrase in anchors into individual words, remove special characters, and convert to lowercase
            anchors = [re.sub(r'\W+', '', word).lower() for anchor in anchors for word in anchor.split()]
            
            importance_scores = [] # Initialize a list to store the importance scores of the anchors
            for score in scores: # Iterate through the scores list
                cleaned_token = re.sub(r'\W+', '', str(score['token'])).lower()
                if cleaned_token in anchors: # Check if the token value is in the anchors list
                    importance_scores.append(score['importance_score']) # Append the importance score to the list
            
            # Calculate the remaining importance score
            x = 100 - sum(importance_scores) 

            filtered_tokens = []
            for score in scores: # Iterate through the scores list
                cleaned_token = re.sub(r'\W+', '', str(score['token'])).lower()
                if cleaned_token in anchors: # Check if the token value is in the anchors list
                    updated_importance = {'token': score['token'],
                                        'importance_score': score['importance_score'] + (x / len(importance_scores)),
                                        'position': score['position']}
                    filtered_tokens.append(updated_importance) # Append the updated importance score to the new list
            return filtered_tokens
        
        except KeyError as e:
            log.error(f"KeyError: Missing key in one of the dictionaries - {e}")
            raise
        except TypeError as e:
            log.error(f"TypeError: Invalid type encountered - {e}")
            raise
        except ZeroDivisionError as e:
            log.error(f"ZeroDivisionError: Division by zero encountered - {e}")
            raise
        except Exception as e:
            log.error(f"An unexpected error occurred: {e}")
            raise
        
    def sentiment_analysis(text: str, class_names):
        log.info("Running local_explain")
        try:
            start_time = time.time()
            explanation = Azure().generate(Prompt.get_classification_prompt(text))
            end_time = time.time()
            total_time = round(end_time-start_time, 3)
            explanation = ResponsibleAIExplain.llm_response_to_json(explanation)

            # Normalize the importance scores to ensure their sum equals 100
            explanation['token_importance_mapping'] = ResponsibleAIExplain.normalize_scores(explanation['token_importance_mapping'])

            # Extract the top 10 important tokens
            tokens_mapping = ResponsibleAIExplain.filter_token_importance(explanation['token_importance_mapping'], explanation['Keywords'])

            return {"predictedTarget": explanation['Sentiment'], 
                    "anchor": explanation['Keywords'], 
                    "explanation": explanation['Explanation'],
                    "token_importance_mapping": tokens_mapping,
                    "time_taken": total_time}
        except Exception as e:
            log.error(e,exc_info=True)
            raise

    async def local_explanation(prompt: str, response: str):
        try:
            start_time = time.time()
            explanation = Azure().generate(Prompt.get_local_explanation_prompt(prompt, response))
            end_time = time.time()
            total_time = round(end_time-start_time, 3)

            explanation = ResponsibleAIExplain.llm_response_to_json(explanation)
            explanation['time_taken'] = total_time

            return explanation
        except Exception as e:
            log.error(e, exc_info=True)
            raise
        
    async def process_importance(importance_function, *args, **kwargs):
        try:
            start_time = time.time()
            importance_map = await importance_function(*args, **kwargs)
            importance_map_df = pd.DataFrame(importance_map, columns=['token', 'importance_value'])
            offset = importance_map_df['importance_value'].mean()

            importance_log = Utils.scale_importance_log(
                importance_map, 
                base=None, 
                offset=offset, 
                min_percentile=0,
                max_percentile=100, 
                scaling_factor=1, 
                bias=0
            )
            importance_log_df = pd.DataFrame(importance_log, columns=['token', 'importance_value'])
            end_time = time.time()
            total_time = round(end_time-start_time, 3)
            return importance_log_df, total_time
        
        except Exception as e:
            log.error(e, exc_info=True)
            raise 
    
    async def prompt_based_token_importance(prompt):
       
        try:
            start_time = time.time()
            max_retries = 5
            attempts = 0
            while attempts < max_retries:
                try:
                    explanation = Azure().generate(Prompt.get_token_importance_prompt(prompt))
                    # Manually find the JSON substring within the mixed content
                    start_index = explanation.find('{')
                    end_index = explanation.rfind('}')
                    if start_index != -1 and end_index != -1 and end_index > start_index:
                        json_content = explanation[start_index:end_index+1]
                        result = json.loads(json_content)
                        # If JSON loads successfully, break out of the loop
                        break
                except JSONDecodeError:
                    attempts += 1
                    if attempts == max_retries:
                        raise Exception("Failed to decode JSON after 5 attempts.")
                    else:
                        log.debug(f"JSONDecodeError encountered. Retrying... Attempt {attempts}/{max_retries}")
                        # Add a delay before the next attempt
                        time.sleep(2) # Delay for 2 seconds
                        
            # Assuming 'result' is a dictionary with "Token" and "Importance Score" as keys, and their values are lists
            # First, create a DataFrame from the 'result' dictionary
            tokens = result['Token']
            scores = result['Importance Score']
            positions = list(range(1, len(result['Token']) + 1))

            # Find the length of the shortest list
            min_length = min(len(tokens), len(scores), len(positions))

            # Trim the lists to the length of the shortest list
            tokens = tokens[:min_length]
            scores = scores[:min_length]
            positions = positions[:min_length]

            df = pd.DataFrame({
                'token': tokens,
                'importance_value': scores,
                'position': positions
            })
 
            df['importance_value'] = df['importance_value'].astype(float)
 
            # Sort the DataFrame by 'Importance Score' in descending order to get the most important tokens first
            df_sorted = df.sort_values(by='importance_value', ascending=False)
 
            # Select the top 10 important tokens
            df_top10 = df_sorted.head(10)
            df_top10.reset_index(drop=True, inplace=True)
            end_time = time.time()
            total_time = round(end_time-start_time, 3)
            top_10, base64_encoded_imgs, token_heatmap = await ResponsibleAIExplain.analyze_heatmap(df_top10[['token', 'importance_value']])
 
            return df_top10.to_dict(orient='records'), base64_encoded_imgs, token_heatmap, total_time
        
        except Exception as e:
            log.error(e, exc_info=True)
            raise 

    async def graph_of_thoughts(prompt: str, modelName: str):
        try:
            start_time = time.time()
            budget = 30
            task = "answer the following question"
            question = prompt
            approaches = [GraphOfThoughts.got]
            modelName = modelName
            
            formatted_graph, formatted_thoughts = GraphOfThoughts.run(task=task, question=question, 
                                                                      methods=approaches, 
                                                                      budget=budget, 
                                                                      lm_name=modelName)
            
            formatted_graph[3]['operation'] = 'final_thought'
            for i in range(4):
                thoughts = formatted_graph[i]['thoughts']
                for j in range(len(thoughts)):
                    formatted_graph[i]['thoughts'][j]['score'] = round(formatted_graph[i]['thoughts'][j]['score'], 2)
            end_time = time.time()
            total_time = round(end_time-start_time, 3)

            return formatted_graph, formatted_thoughts, total_time
        except Exception as e:
            log.error(e, exc_info=True)
            raise

    async def search_augmentation(inputPrompt, llmResponse):
        try:
            import datetime
            current_date = datetime.datetime.now()

            start_time = time.time()

            # Step 1: Generate Facts with LLM response
            facts = Azure().generate(Prompt.generate_facts_prompt(inputPrompt, llmResponse, current_date))
            if isinstance(facts, str):
                facts = ResponsibleAIExplain.llm_response_to_json(facts)
            facts_list = [fact['Fact'] for fact in facts['Facts']] # Extracting the facts into a list of strings

            # Step 2: Filter the facts that are relevant to the input prompt
            filtered_facts = Azure().generate(Prompt.filter_facts_prompt(prompt=inputPrompt, facts=facts_list))
            filtered_facts = ast.literal_eval(filtered_facts)
            filtered_facts_ir = [fact + ' is this statement valid as of today ? why ? #' for fact in filtered_facts]
            questions = [inputPrompt] + filtered_facts_ir

            # Step 3: Run the prompt and facts through the Google Serper API
            search = GoogleSerperAPIWrapper()
            internet_responses = await search.run([inputPrompt])
            answers = [item[0]['content'] for item in internet_responses]
            qa_dict_list_prompt = [{'question': q, 'answer': a} for q, a in zip([inputPrompt], answers)] # Creating the list of dictionaries

            internet_responses = await search.run(questions)
            answers_facts = [item[0]['content'] for item in internet_responses]
            qa_dict_list = [{'question': q, 'answer': a} for q, a in zip(questions, answers_facts)] # Creating the list of dictionaries

            if len(facts_list) == 0:
                return {'internetResponse': qa_dict_list_prompt[0]['answer'], 
                        'factual_check': {"Score": 0.0,
                                          "explanation_factual_accuracy": {'Result': ['No facts found in the LLM response.']} }}

            # Step 4: Summarize the internet responses for prompt and facts
            summary_prompt = Azure().generate(Prompt.summarize_prompt(qa_dict_list_prompt))

            # Step 5: Evaluate fact with Google Search results
            facts = Azure().generate(Prompt.evaluate_facts_prompt(facts=filtered_facts_ir, context=qa_dict_list, prompt=inputPrompt))
            if isinstance(facts, str):
                facts = ResponsibleAIExplain.llm_response_to_json(facts)

            # In facts['Result'], each fact is a dictionary with keys 'Fact', 'Reasoning', and 'Judgement', update Fact with the filtered facts
            for i, fact in enumerate(facts['Result']):
                fact['Fact'] = filtered_facts[i]

            factuality_check = { "Score": 1.0,
                                "explanation_factual_accuracy": facts }
            end_time = time.time()
            total_time = round(end_time-start_time, 3)
            return {'internetResponse': summary_prompt,
                    'factual_check': factuality_check,
                    'time_taken': total_time}
        
        except Exception as e:
            log.error(e, exc_info=True)
            raise 