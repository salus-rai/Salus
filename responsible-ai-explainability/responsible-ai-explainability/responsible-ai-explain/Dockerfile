FROM python:3.9.13

ENV DEBIAN_FRONTEND=noninteractive
	
COPY . .

RUN pip install -r requirements/requirement.txt
RUN pip install scikit-learn==1.3.0
WORKDIR src

CMD ["sh", "-c", "python main.py"]
