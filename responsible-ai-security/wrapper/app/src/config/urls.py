"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



class UrlLinks:
    Assessment_Generation = False
    #(Current_ID is Starting with 220 as it is ASCII sum of RAI)
    Current_ID = 220

    AvailableModel_url = "http://10.212.115.38:30017/Security/model/get"
    AddModel_url = "http://10.212.115.38:30017/Security/Model/add"
    SetModel_url = "http://10.212.115.38:30017/Security/select/model"
    SetAttack_url = "http://10.212.115.38:30017/Security/select/attack"

    AddModel_url = "http://localhost:8000/Security/Model/add"
    SetModel_url = "http://127.0.0.1:8000/Security/select/model"
    SetAttack_url = "http://127.0.0.1:8000/Security/select/attack"
    AvailableModel_url = "http://localhost:8000/Security/model/get"





