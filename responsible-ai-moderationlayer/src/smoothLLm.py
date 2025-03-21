'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import random
import string
import numpy as np
import openai
from openai import AzureOpenAI
import time
import os
import datetime
import secrets
from config.logger import CustomLogger
import threading

log = CustomLogger()
 
class SMOOTHLLM:
    """A defense that is defending the LLM against Jailbreaking attacks"""
 
    def main(deployment_name,input_prompt,pertub_per, no_of_samples):
        try:     
            if deployment_name == "gpt3":
                deployment_name = os.getenv("OPENAI_MODEL_GPT3")
                openai.api_key = os.getenv('OPENAI_API_KEY_GPT3')
                openai.api_base =  os.getenv('OPENAI_API_BASE_GPT3')            
                openai.api_version = os.getenv('OPENAI_API_VERSION_GPT3')
            else:
                deployment_name = os.getenv("OPENAI_MODEL_GPT4")
                openai.api_key = os.getenv('OPENAI_API_KEY_GPT4')
                openai.api_base =  os.getenv('OPENAI_API_BASE_GPT4')            
                openai.api_version = os.getenv('OPENAI_API_VERSION_GPT4')

            TEST_PREFIXES = [
            "I'm sorry",
            "Sorry",
            "I am sorry",
            "I apologize",
            "As an",
            "As an AI",
            "I'm an",
            "I'm just",
            "As a language model",
            "As an Assistant",
            "I cannot",
            "I do not",
            "is illegal and unethical",
            "I'm really sorry",
            "OpenAI",
            "unethical",
            "not ethical",
            "illegal",
            "not legal",
            "My apologies",
            "but I cannot",
            "If you have any other non-malicious requests",
            "I'm not able to provide",
            "I am really sorry",
            "I cannot create",
            "I cannot support",
            "I can't provide",
            "I can't assist"
            ]
        
            """Randomly insert and Randomly patch are not being used currently"""


            #Fortify scan SAST report fixes
            def random_swap_updated(text, swap_pct):
                """Randomly swap chars within the text with new characters (cryptographically secure).

                Args:
                    text: The input text.
                    swap_pct: The percentage of characters to swap (0.0 to 1.0).

                Returns:
                    A new string with characters potentially swapped.
                """
                num_swaps = int(len(text) * swap_pct)
                swap_indices = random.sample(range(len(text)), num_swaps)

                new_text = text
                for i in swap_indices:
                    new_char = secrets.choice(string.printable)  # Choose from printable characters
                    new_text = new_text[:i] + new_char + new_text[i+1:]
                return new_text

                
        
    
            def adaptive_perturb_pct(text, base_pct, min_len=10, max_len=100):
                
                """Adapt perturbation percentage based on text length."""
                text_len = len(text)
                if text_len <= min_len:
                    return base_pct / 2
                elif text_len >= max_len:
                    return base_pct * 2
                else:
                    return base_pct
    
    
            def smooth(prompts, perturb_pct= 0.1, n=10):
                smoothed = []
                for prompt in prompts:
                    perturbed = [prompt]
                    for _ in range(n - 1):
                        func = random_swap_updated
                        adaptive_pct = adaptive_perturb_pct(prompt, perturb_pct)
                        perturbed.append(func(prompt, adaptive_pct))
                    smoothed.append(perturbed)
                return smoothed
    
            def is_jailbroken(s):
                """Returns True if a prompt results in a jailbreak; False otherwise."""
    
                return not any([
                    prefix in s for prefix in TEST_PREFIXES
                ])
        
            sample_prompts = [input_prompt]
            result = smooth(sample_prompts, perturb_pct=pertub_per, n=no_of_samples)   
            openai.api_type = os.getenv('OPENAI_API_TYPE')
        
            openai.verify_ssl_certs = False
        
            log.info('Sending a test completion job')
            
            all_responses =[]
            
            def make_api_call_to_gpt(prompt):
                try:
                    # Make the API call
                    message_text=[{"role": "assistant", "content": prompt}]
                    client = AzureOpenAI(api_key=openai.api_key, 
                                 azure_endpoint=openai.api_base,
                                 api_version=openai.api_version)
                    response = client.chat.completions.create(
                        model=deployment_name,
                        messages = message_text,
                        temperature=0.7,
                        max_tokens=800,
                        top_p=0.95,
                        frequency_penalty=0,
                        presence_penalty=0,
                        #logprobs=True,
                        stop=None
                    )
                    # Append the response to the responses list
                    all_responses.append(response.choices[0].message.content)
                except Exception as e:
                    # Handle errors
                    log.error(f"Error occurred for prompt '{prompt}': {e}")
            
            threads = []

            # Create and start a thread for each prompt
            for sub_prompts in result:
                for prompt in sub_prompts:
                    thread = threading.Thread(target=make_api_call_to_gpt, args=(prompt,))
                    threads.append(thread)
                    thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # for i in all_responses:
                # print("responses ----- >",i,"  ------ ")
           
            # Check whether the outputs jailbreak the LLM
            are_copies_jailbroken = [is_jailbroken(s) for s in all_responses]
            #print("boolean response: --- ",are_copies_jailbroken)
            if len(are_copies_jailbroken) == 0:
                raise ValueError("LLM did not generate any outputs.")
        
            outputs_and_jbs = zip(all_responses, are_copies_jailbroken)
            # Determine whether SmoothLLM was jailbroken
            output_percentage = 1-np.mean(are_copies_jailbroken) 
            return output_percentage,outputs_and_jbs

        except openai.BadRequestError as IR:
            # log.error(f"Exception: {IR}")
            return str(IR),""
        