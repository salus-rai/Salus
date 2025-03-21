"""
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import base64
from io import BytesIO
from PIL import Image
import requests
from IPython.display import Image, display, Audio, Markdown
import cv2
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import base64
import uuid
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage,ChatMessage
from RAG.service.service import cache,MAX_CACHE_SIZE,fs, dbtypename
import os
import time
import traceback
import json
from RAG.config.logger import CustomLogger,request_id_var

log=CustomLogger()
request_id_var.set("Startup")

try:
    azureaddfileurl=os.getenv("AZUREADDFILE")
    containername=os.getenv("CONTAINERNAME")
    azureblobnameurl=os.getenv("AZUREBLOBNAME")
except Exception as e:
    log.info("Failed at azure loading")

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

import tempfile
import shutil

def video_rag(payload):
    try:  
        payload = AttributeDict(payload) 
        text = payload.text  
        filevid = payload.file
        
        
        # response = requests.post(url=azureaddfileurl, files={"file": (filevid.filename, filevid.file)}, data={"container_name": containername}, headers=None, verify=False)
        # if response.status_code == 200:
        #     log.info(f"File uploaded successfully.")
        # else:
        #     log.info(f"Error uploading file': {response.status_code} - {response.text}")
        
        temp_dir = "../data/multimodal/video"   
        os.makedirs(temp_dir, exist_ok=True)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", dir=temp_dir, mode='wb') as temp_file:
            shutil.copyfileobj(filevid.file, temp_file)
            temp_file_path = temp_file.name
        
        base64Frames, audio_path= process_video(temp_file_path, seconds_per_frame=1)
        
        audio_text = convert_audio_to_text(audio_path)
        print("soundsound",audio_text)
        
        # os.remove(temp_file_path)
        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary video file deleted: {temp_file_path}")
        
        if os.path.isfile(audio_path):
            os.remove(audio_path)
            print(f"Temporary audio file deleted: {audio_path}")
        
        # display_handle = display(None, display_id=True)
        # for img in base64Frames[:9]:
        #     display_handle.update(Image(data=base64.b64decode(img.encode("utf-8")), width=600))
        #     time.sleep(0.025)

        # Audio(audio_path)
        llm = AzureChatOpenAI(deployment_name=os.getenv("OPENAI_MODEL_GPT4_O"), openai_api_version=os.getenv('OPENAI_API_VERSION_GPT4_O'), openai_api_key=os.getenv('OPENAI_API_KEY_GPT4_O'), openai_api_base=os.getenv('OPENAI_API_BASE_GPT4_O'))
        # messages=[
        #     {"role": "system", "content": []},
        #     {"role": "user", "content": [
        #         {"type": "text", "text": "These are the frames from the video."},
        #         *map(lambda x: {"type": "image_url", 
        #                         "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames[:9])
        #         ],
        #     }
        # ]
        
        messages = [
            {"role": "system", "content": []},
            {"role": "user", "content": [
                {"type": "text", "text": "These are the frames from the video."},
                *map(lambda x: {"type": "image_url", 
                                "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames),
                {"type": "text", "text": f"Audio transcript: {audio_text}" if audio_text else "Audio transcript could not be generated."}
            ]}
        ]
        
        messages[0]["content"].append({"type": "text", "text": text})
        ai_message = llm.invoke(messages)
        print(ai_message.content)
        output = [ai_message.content]
        return output
            
    except Exception as e:
        log.info("Failed at video_rag")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
        
def process_video(video_path, seconds_per_frame=2):
    try:
        id = uuid.uuid4().hex
        # path = "../data/multimodal/"+str(id)+"/"
        base64Frames = []
        # base_video_path, _ = os.path.splitext(video_path)

        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise RuntimeError(f"Failed to open video file: {video_path}")
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        frames_to_skip = int(fps * seconds_per_frame)
        curr_frame=0

        # Loop through the video and extract frames at specified sampling rate
        while curr_frame < total_frames - 1:
            video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
            curr_frame += frames_to_skip
        video.release()
        
        temp_dir = "..//data//multimodal//audio//"
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3",dir=temp_dir, mode='wb') as temp_audio_file:
        #     audio_path = temp_audio_file.name
          
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        # audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        # audio_path = os.path.join(temp_dir, audio_filename)

        # Extract audio from video
        audio_path = f"{temp_dir}audio.wav"
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, bitrate="32k")
        clip.audio.close()
        clip.close()

        print(f"Extracted {len(base64Frames)} frames")
        print(f"Extracted audio to {audio_path}")
        # if os.path.isfile(audio_path):
        #     os.remove(audio_path)
        #     print(f"Temporary audio file deleted: {audio_path}")
        return base64Frames, audio_path
    
    except Exception as e:
        log.info("Failed at process_video")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno),e}")
        
def convert_audio_to_text(audio_path):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        log.info("Failed at convert_audio_to_text")
        log.error(f"Exception: {str(traceback.extract_tb(e.__traceback__)[0].lineno)}, {e}")
        return None
    