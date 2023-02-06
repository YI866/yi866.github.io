from celery import Celery

celery_app = Celery('ama',
                    broker='amqp://ikas:ikas@localhost:5672',
                    backend='redis://localhost:6379/3',
                    include=['task'],
             )
