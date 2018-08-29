from flask import Flask
import os

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
host=os.environ['redis']

app.config.update(
    CELERY_BROKER_URL='redis://{0}:6379'.format(host),
    CELERY_RESULT_BACKEND='redis://{0}:6379'.format(host)
)



