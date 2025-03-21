FROM python:3.9.13
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx
	
COPY . .

RUN pip install -r requirements/requirement.txt 

WORKDIR src

CMD ["sh", "-c", "python main.py"]
