FROM alpine/git:v2.32.0
RUN git clone https://github.com/TECH4DX/developer-churn-prediction.git /developer-churn-prediction

FROM python:3.8.12-slim-buster
#RUN apk add g++

COPY --from=0 /developer-churn-prediction /developer-churn-prediction
WORKDIR /developer-churn-prediction

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN chmod +x ./run.sh

CMD ["./run.sh"]
