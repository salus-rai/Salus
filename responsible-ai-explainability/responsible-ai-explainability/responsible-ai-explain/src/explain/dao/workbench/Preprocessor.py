# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.
 
"""
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from explain.dao.workbench.DatabaseConnection import DB
from explain.config.logger import CustomLogger
from dotenv import load_dotenv
load_dotenv()

log = CustomLogger()

# Create a MongoDB database instance
RAIExplainDB = DB.connect()

class Preprocessor:
    
    # Access the "DataAttributes" collection in the Common Workbench database
    collection = RAIExplainDB['Preprocessor']
        
    def find(preprocessor_id: float):
        # Check if preprocessor_id is not None and is a float
        if preprocessor_id is None or not isinstance(preprocessor_id, float):
            raise ValueError("Preprocessor ID must be a non-empty float")
        # Try to find the preprocessor by preprocessor_id in the database
        try:
            result = Preprocessor.collection.find_one({"PreprocessorId": preprocessor_id}, {"_id": 0, "PreprocessorName": 1, "PreprocessorFileId": 1})
            if result is None:
                raise ValueError(f"Invalid Preprocessor ID {preprocessor_id}")
        except Exception as e:
            raise 
        
        return result