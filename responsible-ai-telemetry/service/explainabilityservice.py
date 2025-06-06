"""
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from datetime import datetime
import json
from pydantic import parse_obj_as
from zoneinfo import ZoneInfo
import os
from elasticsearch import Elasticsearch
from mapper.explainabilitytelemetrydata import TelemetryData
from service.elasticconnectionservice import es
from dateutil.parser import parse
def explainabilityElasticDataPush(data):
    # print(json_string)
    if isinstance(data, str):
        data = parse_obj_as(TelemetryData, json.loads(data))
    # data = parse_obj_as(TelemetryData, json.loads(json_string))
    # Index Creation
    index_name = 'explainabilityindex'
    if not es.indices.exists(index=index_name):
        index_body = {
            'mappings': {
                'properties': {
                    'uniqueid': {'type': 'keyword'},
                    'tenant': {'type': 'keyword'},
                    'apiname': {'type': 'keyword'},
                    'user': {'type': 'keyword'},
                    'lotNumber':{'type': 'keyword'},
                    'date': {'type': 'date'},
                    'request': {
                        'properties': {
                            'portfolio_name': {'type': 'keyword'},
                            'account_name': {'type': 'keyword'},
                            'inputText': {'type': 'keyword'},
                            'explainerID': {'type': 'integer'}
                        }
                    },
                    'response': {
                        'properties': {
                            'explainerID': {'type': 'integer'},
                            'explanation': {
                                'properties': {
                                    'predictedTarget': {'type': 'keyword'},
                                    'anchor': {'type': 'keyword'}
                                }
                            }
                        }
                    }
                }
            }
        }
        es.indices.create(index=index_name, body=index_body)
    date = parse(data.date)
    es_data = []
    es_doc = {
        'uniqueid': data.uniqueid,
        'tenant': data.tenant,
        'apiname': data.apiname,
        'user': data.user,
        'lotNumber': data.lotNumber,
        'date': date.now(),
        'request': data.request.dict(),
        'response': [explanation.dict() for explanation in data.response.explanation]
    }
    es_data.append(es_doc)
    print("es_doc=========",es_doc)
    for doc in es_data:
        try:
            es.index(index=index_name, body=doc)
            print("DOC INSERTED IN THE ELASTIC", doc)
        except Exception as e:
            print("Error occurred while inserting document")

    print("ELASTIC DATA AFTER INSERTION", es_data)
    es.indices.refresh(index=index_name)