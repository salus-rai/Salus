'''
MIT license https://opensource.org/licenses/MIT Copyright 2024 Infosys Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import base64
import io
from typing import Tuple
import cv2
from PIL import Image
from privacy.service.imagePrivacy import AttributeDict, ImagePrivacy
import numpy as np
from privacy.config.logger import request_id_var
from privacy.config.logger import CustomLogger
import os
import shutil
import threading
import time
import uuid

log = CustomLogger()

path="../video/"
error_dict={}

class VideoService:
        def frameAnonymization(payload,frame,indx,procFrame,request_id):
                try:
                        # request_id_var.set(request_id)
                        id = uuid.uuid4().hex
                        request_id_var.set(id)
                        ipath=path+str(request_id)+"/"+str(indx)+".jpg"
                        # print(ipath)
                        # Convert the frame to PIL Image
                        # base64.b64encode(frame).decode()
                        # Image.open(base64.b64encode(frame).decode())
                        # print(type(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                        imagef = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        imagef.save(ipath)
                        # image=open("test.jpg","rb")
                        # print(type(imagef))
                        image={"file":ipath}
                        image=AttributeDict(image)
                        payload["image"]=image
                        payload["piiEntitiesToBeRedacted"]=None
                        # ocr=None
                        # global imageAnalyzerEngine

                        # imageAnalyzerEngine = ImageAnalyzerEngine(analyzer_engine=analyzer,ocr=ocr)  
                        # imageRedactorEngine = ImageRedactorEngine(image_analyzer_engine=imageAnalyzerEngine)
                        # redacted_image = imageRedactorEngine.redact(image, (255, 192, 203))
                        # payload={"easyocr":"Tesseract","mag_ratio":False,"rotationFlag":False,"image":image,"portfolio":None,"account":None,"exclusion":None}

                        redacted_image=ImagePrivacy.image_anonymize(payload)
                        decoded_bytes = base64.b64decode(redacted_image)

                        # Create a BytesIO object to simulate a file-like object
                        bio = io.BytesIO(decoded_bytes)

                        # Use OpenCV (assuming it's an image) or other libraries to load the image from the BytesIO object
                        img = cv2.imdecode(np.fromstring(bio.getvalue(), np.uint8), cv2.IMREAD_COLOR)

                        # Convert the PIL Image back to OpenCV frame
                        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                        procFrame[indx]=frame
                        return (frame,indx)
                        # Write the frame into the file 'output.avi'
                        # out.write(frame)

                    # else:
                except Exception as e:
                        log.error(str(e))
                        log.error("Line No:"+str(e.__traceback__.tb_lineno))
                        log.error(str(e.__traceback__.tb_frame))
                        # error_dict[request_id_var.get()].append({"UUID":request_id_var.get(),"function":"VideoAnalyzeMainFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
                        # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnalyzeMainFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
                        raise Exception(e)
                    #     break


        async def videoPrivacy(payload) -> Tuple[str, str]:
            error_dict[request_id_var.get()]=[]
            try:     
                  payload=AttributeDict(payload)
                  upload_file = payload.video
                  filename=upload_file.filename

                  id = uuid.uuid4().hex
                  request_id_var.set(id)
                  _path=path+str(id)
                  if(not os.path.exists(_path)):
                    os.makedirs(_path)
                  video_data = await upload_file.read()
                  s=time.time()
                  temp_file_path = path+"input.pm4"
                  output_file_path =path+"output3.mp4"
                  with open(temp_file_path, "wb") as temp_file:
                      temp_file.write(video_data)
                  video = cv2.VideoCapture(temp_file_path)
                  # Get video properties
                  width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                  height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                  fps = video.get(cv2.CAP_PROP_FPS)
                  sampling_rate=int(fps*0.3)
                  # Define the codec and create a VideoWriter object
                  fourcc = cv2.VideoWriter_fourcc(*'XVID')
                  out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))
                  frameList=[]
                  indxList=[]
                  first=True
                  count=0
                  last_frame=None
                  log.debug("samp "+str(sampling_rate))


                  # audio_fps = video.get(cv2.CAP_PROP_FPS)
                  # fourcc = int(video.get(cv2.CAP_PROP_FOURCC)) 
                  # print("aud",audio_fps,fourcc)
                  # sampling_rate=1
                  while(video.isOpened()):
                      ret, frame = video.read()
                      # print(ret)
                      if ret==True:
                          if first:
                                frameList.append(frame)
                                indxList.append(count)
                                first=False          
                          else:
                            if count % sampling_rate == 0:
                              frameList.append(frame)
                              indxList.append(count)
                            # else:
                            #   frameList.append(None)
                          last_frame=frame
                          count+=1    
                      else:
                          break
                  if(count%sampling_rate!=0):
                    frameList.append(last_frame)
                    indxList.append(count)
                  log.debug("totalFrame:"+str(count))
                  # print(indxList,len(indxList))       
                  log.debug("after sampling"+str(len(frameList)))
                  rcount=len(frameList)
                  framecopy=frameList.copy()
                  procFrame=[None]*(count+1)
                  # print(len(procFrame))
                  # indx=0
                  while framecopy:
                      threads = []
                      for _ in range(min(6, len(framecopy))):  # Limit calls to remaining arguments
                        arg = framecopy.pop(0)  # Get the first argument and remove it
                        indx=indxList.pop(0)
                        thread = threading.Thread(target=VideoService.frameAnonymization, args=(payload,arg,indx,procFrame,request_id_var.get()))
                        thread.start()
                        threads.append(thread)
                        # print(thread)
                        indx+=1
                      # Wait for all threads in the current set to finish

                      log.debug("remaining:"+str(rcount-len(framecopy))+"/"+str(rcount))
                      for thread in threads:
                        thread.join()   
                  # print("===",procFrame)     
                  # Release everything when job is finished
                  # print(procFrame)
                  lstFrame=None
                  for frm in procFrame:
                      # print(frm,frm.any())
                      # print(frm,frm.all())
                      if(lstFrame is None):
                          lstFrame=frm
                      if(frm is not None):
                        lstFrame=frm 
                      else:
                          frm=lstFrame
                      out.write(frm)
                  video.release()
                  out.release()
                  # Remove temporary file
                  # os.remove(temp_file_path)
                  # Read the processed video file
                  with open(output_file_path, "rb") as video_file:
                      video_data = video_file.read()
                  # Convert the video to base64
                  video_str = base64.b64encode(video_data).decode()
                  # Remove the output file
                  # os.remove(output_file_path)
                #   log.debug(path)
                  shutil.rmtree(_path)
                #   log.debug("====",time.time()-s)
                  del procFrame
                  del indxList
                  del frameList
                  return video_str

            except Exception as e:
                log.error(str(e))
                log.error("Line No:"+str(e.__traceback__.tb_lineno))
                log.error(str(e.__traceback__.tb_frame))
                error_dict[request_id_var.get()].append({"UUID":request_id_var.get(),"function":"VideoAnonymizeMainFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
                # ExceptionDb.create({"UUID":request_id_var.get(),"function":"textAnalyzeMainFunction","msg":str(e.__class__.__name__),"description":str(e)+"Line No:"+str(e.__traceback__.tb_lineno)})
                raise Exception(e)
