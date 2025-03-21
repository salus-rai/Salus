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

from llm_explain.utility.prompts.output_format import *
from llm_explain.utility.prompts.few_shot import *
from llm_explain.utility.prompts.instructions import *

class Prompt:

    def get_classification_prompt(input_prompt):
        
        template = f"""
            Imagine you are a Responsible AI expert with experience in explaining why a model has made a decision. 
            Your task is to determine the sentiment of the given prompt, identify the keywords the model used to arrive at that sentiment, and provide a clear explanation of why the model classified the prompt as that sentiment.

            Calculate the importance value of each token  towards getting the overall sentiment from the given prompt using a score between 1 (low importance) and 100 (high importance). 
            Provide all the tokens as a list. Ensure that you give an importance score for all tokens, and there are no empty spaces or inconsistencies in the output, which might cause issues while parsing. 
            Make your analysis consistent so that if given the same input again, you produce a similar output.

            similarly, provide sentiment, keywords identified to determine the sentiment and Explanation for the below given information.
            Make sure identified key words are individual words and not combined words.

            Make sure the response is simple and easy to understand. Use polite language. Do not write as a third person. Do not include Certainly! at the beginning of your response, just give response.
            
            Example Data:
            {one_shot_sentiment_analysis}
            
            Return the output only in the following JSON format. Do not output anything other than this JSON object:
            {output_format_sentiment_analysis}

            Task Data:
            [Prompt]: {input_prompt}
            """
        return template
        
    def get_local_explanation_prompt(prompt, response):

        template = f'''
            You are a Responsible AI expert with extensive experience in Explainable AI for Large Language Models. Your role is to clearly generate explanations for why the Large Language Model has generated a certain response for the given prompt.

            You are a helpful assistant. Do not fabricate information or provide assumptions in your response.

            Given the following prompt-response pair:

            Prompt: {prompt}
            Response: {response}

            Please assess the following metrics:

            1. Uncertainty: Evaluate the uncertainty associated with the response for the given prompt using a score between 0 (certain) and 95 (highly uncertain). Additionally, explain your reasoning behind the assigned score.
            2. Coherence: Evaluate the logical flow and coherence of the response using a score between 0 (incoherent) and 95 (highly coherent). Additionally, explain your reasoning behind the assigned score.

            Based on the score and explanation for each metric, provide a recommendation for how to change the input prompt so that the response will be better and the scores will improve. Ensure that each recommendation is concrete and actionable. If a metric has a perfect score, provide positive reinforcement or suggest maintaining the current quality.

            Return the output only in the following JSON format. Do not output anything other than this JSON object:
            {output_format_local_explanation}
            
        '''
        return template

    def get_token_importance_prompt(prompt):
       
        template = f'''
            You are a helpful assistant. Do not fabricate information or do not provide assumptions in your response.
 
            Given the following prompt:
 
            Prompt: {prompt}
 
            Please assess the following metric:
            1. Token Importance: Evaluate the importance of each token in the prompt. Calculate the importance value of each token in the given prompt using a
            score between 0 (low importance) and 1 (high importance). Provide all the tokens as a list. Ensure that you give an importance score for all tokens,
            and there are no empty spaces or inconsistencies in the output, which might cause issues while parsing. Make your analysis consistent so that if given
            the same input again, you produce a similar output.
 
            Return the output only in the following JSON format. Do not output anything other than this JSON object:
            {output_format_token_importance}
        '''
        return template
    
    def get_tone_prediction_prompt(response):

        template = f'''
            You are a detail-oriented LLM that pays close attention to the nuances of language. 
            You will be given a text and your job is to analyze its tone. 

            Specifically, you need to consider the following tones and identify which tone is most appropriate for the given text:

            Formal: Professional, respectful, objective (e.g., scientific reports, business emails)
            Informal: Casual, conversational, friendly (e.g., text messages, social media posts)
            Informative: Primarily focused on conveying information clearly and concisely (e.g., news reports, summaries)
            Positive: Happy, optimistic, encouraging (e.g., motivational speeches, congratulations)
            Negative: Sad, angry, frustrated (e.g., complaints, critical reviews)
            Neutral: Objective, unbiased, unemotional (e.g., factual summaries, news reports)
            Humorous: Funny, witty, sarcastic (e.g., jokes, lighthearted stories)
            Dramatic: Suspenseful, exciting, intense (e.g., fictional narratives, descriptions of events)
            Inspiring: Uplifting, motivating, thought-provoking (e.g., speeches, self-help content)
            Persuasive: Trying to convince the reader of something (e.g., marketing copy, arguments)
            Empathetic: Understanding and supportive (e.g., responses to someone going through a tough time)
            Authoritative: Confident, knowledgeable (e.g., expert opinions, instructions)

            Based on the score and explanation for each metric, provide a recommendation for how to change the input prompt so that the response will be better and the scores will improve. Ensure that each recommendation is concrete and actionable. If a metric has a perfect score, provide positive reinforcement or suggest maintaining the current quality.

            Example Data:
            {few_shot_examples_tone_analysis}

            Return the output only in the following JSON format. Do not output anything other than this JSON object:
            {output_format_tone_analysis}

            Task Data:
            [Response]: {response}
        '''
        return template
    
    def get_coherehce_prompt(response):

        template = f"""
            You are a detail-oriented LLM which pays close attention to the details. You are given a text and your job is to evaluate the quality of the provided text, focusing on the coherence aspect.

            Coherence is the quality of the text that makes it logical and consistent. It is important that the text is well-organized and the ideas are connected in a clear and meaningful way. A coherent text is easy to follow and understand.

            Please provide a score on the scale of 1-5, with 1 meaning that the text is completely incoherent and the elements in the text do not stitch together to produce meaningful text, and 5 meaning that the text is completely coherent and the elements in the text stitch together to produce meaningful text.

            Example Data.
            {LANGUAGE_COHERENCE_FEW_SHOT__COT}

            First, analyze the text and determine how fluent and natural sounding it is. Consider the structure, connectivity of ideas, and overall readability of the text. Write down step-by-step reasoning to make sure that your conclusion is correct.

            {CHAIN_OF_THOUGHT}

            Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
            {LANGUAGE_COHERENCE_OUTPUT_FORMAT__COT}

            Task data.
            [Resposne]: {response}
        """
        return template
    
    def get_response_revelance_prompt(prompt, response):

        template = f"""
            You are a detail-oriented LLM which pays close attention to the details, checks for consistency, and is adept at identifying logical fallacies, incorrect assumptions, or other errors in reasoning.
            Your task is to determine the degree of irrelevant information present in the given response.

            Example Data.
            {RESPONSE_RELEVANCE_FEW_SHOT__COT}

            For the given task data, carefully examine the response and assess if it has any additional irrelevant information or not. Don't focus on aspects like style, grammar, or punctuation. 
            Assign a score between 0 and 1, where 0 indicates that the response is completely irrelevant to the prompt, and 1 indicates that the response is highly relevant to the prompt.
            {CHAIN_OF_THOUGHT}

            Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
            {RESPONSE_RELEVANCE_OUTPUT_FORMAT__COT}

            Task Data.
            [Question]: {prompt}
            [Response]: {response}
            [Output]:
        """

        return template
    
    def generate_facts_prompt(prompt, response, current_date):

        template = f"""
            You are given a response along with its question. For the given task data, please breakdown the response into independent 
            facts. A fact is a sentence that is true and can only be stated from the response. Facts should not depend on each another 
            and must not convey the same information. While generating facts, ensure that the facts are contextually mentioned and 
            do not begin with pronouns like 'He,' 'She,' or references to third-party entities. Limit to 5 facts in the output.
            
            Response may contain information that is not asked in Question, consider only required information in Response that is 
            relevant to the Question.
            
            Example Data.
            {FACT_GENERATE_FEW_SHOT}

            Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
            {FACT_GENERATE_OUTPUT_FORMAT}

            Task Data.
            [Question]: {prompt}
            [Response]: {response}
            [Output]: 
        """

        return template
    
    def evaluate_facts_prompt(facts, context, prompt):

        template = f"""
            You are a detail-oriented LLM whose task is to determine if the given facts or questions are supported by the given context
            and prompt. 
            Each fact or question is separated by the following symbol: "#". 

            For the given task data, go over each fact or question sentence one by one, and write down your judgement.
            If it is a question then answer the question based on the context and prompt. 
            Use important dates if any available in the context to make a better judgement.
            If it is a fact, determine if the fact is supported by both context and prompt.

            Before answering, reason in a step-by-step manner to provide your final judgement.
            If the reasoning is clear then give judgement as "yes" or "no" otherwise give judgement as "unclear".

            Example Data.
            {FACT_EVAL_FEW_SHOT__COT}

            Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
            {FACT_EVALUATE_OUTPUT_FORMAT__COT}

            Task Data.
            [Prompt]: {prompt}
            [Facts]: {facts}
            [Context]: {context}
            [Output]:
        """

        return template
    
    def filter_facts_prompt(prompt, facts):

        FACT_FILTER_PROMPT_TEMPLATE = f"""
            You are provided with a list of facts generated from a response to a specific question. Your task is to filter and retain only those 
            facts that are directly relevant to the question. Ignore any facts that do not pertain to the original question.

            While filtering facts, ensure that the facts are contextually mentioned and 
            do not begin with pronouns like 'He,' 'She,' or references to third-party entities. If any such facts are identified, rewrite them.

            Focus on identifying and selecting the facts that specifically answer the question asked, while discarding any irrelevant 
            or off-topic information.

            Example Data:
            {FACT_FILTER_FEW_SHOT}

            Return the output in the specified JSON format. If no relevant facts are found, return an empty list [].

            Task Data:
            [Question]: {prompt}
            [Response Facts]: {facts}

            [Output]:
        """

        return FACT_FILTER_PROMPT_TEMPLATE
    
    def summarize_prompt(qa_dict_list):

        SUMMARIZATION_PROMPT_TEMPLATE = f"""
            You are provided with a list of JSON objects, each containing a 'question' and an 'answer'. The answer is obtained from
            Google Search API and is a detailed response to the corresponding question.
            
            Your task is to create a separate summary for each question-answer pair, preserving the context and tense of the original 
            question and answer. Don't mention anything other than what is given in answer.

            Ensure that:
            - Each summary is in a separate paragraph.
            - There is a one-line space between each paragraph.
            - The tense and context of the original question and answer are maintained accurately.

            Ensure that there is no fabricated or hallucinated information in your response and make sure that there are no conflicting statements 
            from one para to another in your summary. Do not mention paragraph or such type of words in your response, just summarize and provide answers.

            Task Data:
            [Input]: 
            {qa_dict_list}

            [Output]: 
        """

        return SUMMARIZATION_PROMPT_TEMPLATE