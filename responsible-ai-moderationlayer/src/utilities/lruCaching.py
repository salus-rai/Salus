# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.
 
"""
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time
import hashlib
from config.logger import CustomLogger


log = CustomLogger()


################################# Caching Logic ######################################
# LRU Caching Technique
'''
   ttl : time for which cache entries can be stored

   max_size : maximum number of cache entries that can be stored , here each entry is a key-value pair.
              Key is a prompt and value is the response for that prompt.Since, we are storing for 15 calls in the cache for a single prompt, so
              if max_size is 750, means we can store values in cache for 50 prompts. This size is configurable.
'''
def lru_cache_response(func,ttl=7200,max_size=750,flag=False):
    
    cache = {}
    lru_queue = []
    
    def generate_sha256_hash(input_string):
        """Generates a SHA-256 hash of the given input string.
        Args:
        input_string (str): The input string to be hashed.
        Returns:
        str: The SHA-256 hash of the input string in hexadecimal format.
        """
        encoded_string = input_string.encode()
        sha256_hash = hashlib.sha256(encoded_string)
        hex_digest = sha256_hash.hexdigest()
        return hex_digest
    
    def wrapper(*args, **kwargs):
        if flag=="True":
            param = ""
            for element in args:
                if isinstance(element, dict):
                    param = str(args[0])
                else:
                    param = str(args)
            
            key = generate_sha256_hash(param)
            now = time.time()
            
            if key in cache and now - cache[key][1] < ttl:
                log.info("Within time limit !!!")
                lru_queue.remove(key)
                lru_queue.append(key)
                return cache[key][0]
            
            if len(cache) > max_size:
                log.info("Cache is full, remove oldest prompt and its response")
                oldest_key = lru_queue.pop(0)
                del cache[oldest_key]

            log.info("May be Time exceeded or memory is full or it's a new entry for cache !!")
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            lru_queue.append(key)
        else:
            log.info("Caching not applied.....")
            result = func(*args, **kwargs)
        
        return result

    
    return wrapper


def lru_cache(ttl,size,flag):
    def decorator(func):
        return lru_cache_response(func,ttl,size,flag)
    return decorator
