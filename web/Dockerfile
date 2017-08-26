FROM python:3
ENV PYTHONUNBUFFERED 1
RUN echo 'deb http://mirrors.aliyun.com/debian/ jessie main non-free contrib' > /etc/apt/sources.list \
&& echo 'deb http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib' >> /etc/apt/sources.list \
&& echo 'deb http://mirrors.aliyun.com/debian-security/ jessie/updates main non-free contrib' >> /etc/apt/sources.list


# 安装tesseract-ocr
RUN apt-get update \
    && apt-get install -y \
        leptonica-progs \
        ghostscript \
        tesseract-ocr \
    && apt-get purge --auto-remove -y \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE "letters_in_image.settings_dev"
