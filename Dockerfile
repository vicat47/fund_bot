FROM python:3.8-buster
COPY . /app
WORKDIR /app
WORKDIR /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt
EXPOSE 5000
VOLUME [ "/app/data" ]

CMD ["python","app.py"]