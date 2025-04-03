"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



from typing import Dict, Callable
from privacy.service.Video_service import *
from privacy.service.csv_service import *
from privacy.service.json_service import *
from privacy.service.files_service import *
from privacy.service.pdf_service import PDFService
from privacy.service.ppt_service import PPTService  
from privacy.service.docs_service import DOCService
from fastapi import Response

class FileService:
    @staticmethod
    def anonymize_file(payload: Dict, file_extension: str) -> str:
        """
        Anonymizes the given file based on the file extension.

        Args:
            payload (Dict): The payload containing the file data.
            file_extension (str): The extension of the file.

        Returns:
            str: The anonymized file.

        Raises:
            ValueError: If the file extension is not supported.
        """
        if file_extension == 'csv':
            return CSVService.csv_anonymize(payload)
        elif file_extension == 'json':
            return JSONService.anonymize_json(payload)
        elif file_extension == 'pdf':
            # ans=PDFService.mask_pdf(payload)
            # response = Response(content=ans.read(), media_type="application/pdf")
            return PDFService.mask_pdf(payload)
            # return response
        elif file_extension == 'pptx' or file_extension == 'ppt':
            # ans=PPTService.mask_ppt(payload)
            # response = Response(content=response.read(), media_type="application/pdf")
            return PPTService.mask_ppt(payload)
        elif file_extension == 'docx':
            return DOCService.mask_doc(payload)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")