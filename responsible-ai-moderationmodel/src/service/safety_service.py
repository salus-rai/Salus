'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from diffusers import StableDiffusionPipeline
import torch


# model_name = "../models/stable_diffusion_v_1_5"
if(torch.cuda.is_available()):
    pipe = StableDiffusionPipeline.from_pretrained(model_name,torch_dtype=torch.float16,safety_checker=None)
    inference=50
    device = torch.device("cuda")
    pipe=pipe.to(device)

else:
    pipe = StableDiffusionPipeline.from_pretrained(model_name,safety_checker=None)
    inference=2

class ImageGen:
    def generate(prompt):
        try:
            image = pipe(prompt,num_inference_steps=inference).images[0]
            # image.show()
            return image
        except Exception as e:
            
            raise Exception("Error in generating image")
        
