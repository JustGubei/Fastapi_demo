FROM python:3.11.0-alpine

COPY . /app
WORKDIR ./app

RUN rm -f /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10159"]