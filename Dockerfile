FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
VOLUME /usr/src/app

ADD Model.py /usr/src/app
ADD Model_train.py /usr/src/app
ADD database.db /usr/src/app
ADD model_trained.pkl /usr/src/app
ADD templates /usr/src/app/templates

RUN pip install numpy
RUN pip install flask
RUN pip install flask_restful
RUN pip install sklearn

CMD [ "python", "/usr/src/app/Model.py" ]