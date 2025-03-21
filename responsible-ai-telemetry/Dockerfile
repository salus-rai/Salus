FROM python:3.9.13

RUN useradd myLowPrivilegeUser
USER myLowPrivilegeUser
ENV DEBIAN_FRONTEND=noninteractive

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python3 main.py"]

