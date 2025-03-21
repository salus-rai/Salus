FROM python:3.9.13

RUN useradd myLowPrivilegeUser
USER myLowPrivilegeUser

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    ffmpeg=7.1* \
    libsm6=2:1.2.3-1 \
    libxext6=2:1.3.3-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirement/requirnments.txt

WORKDIR src

CMD ["sh", "-c", "python3 main.py"]
