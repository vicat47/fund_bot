FROM python:3.8.3-alpine3.11 as Base
FROM Base as Build
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt

FROM Base as Final

COPY --from=Build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
WORKDIR /app
COPY . /app
EXPOSE 5000
VOLUME [ "/app/data" ]

CMD ["python","app.py"]