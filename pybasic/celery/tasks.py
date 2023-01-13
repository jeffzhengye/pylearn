from celery import Celery

BROKER_URL = 'redis://:wd_redis@59.68.29.90:6379/0'

celery_app = Celery('Restaurant', broker=BROKER_URL)

@celery_app.task
def cooking_task(table_no, dishes):
    print("Started cooking for Table Number : "+table_no)
    for dish in dishes:
        print("Cooking : "+dish)
    print("Done cooking for Table Number : "+table_no)