from flask_app import app
from celery import Celery

def make_celery(app):
    print('Backend is')
    print(app.config['CELERY_RESULT_BACKEND'])
    print('Broker is')
    print(app.config['CELERY_BROKER_URL'])
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
    
celery = make_celery(app)

