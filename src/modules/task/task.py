from cele import celery_app


@celery_app.task
def add(x, y):
    print("Start add tasks")
    return x + y


@celery_app.task
def mul(x, y):
    return x * y


@celery_app.task
def xsum(numbers):
    return sum(numbers)