from finale_web.celery import app
import os


@app.task()
def get_task():
    return 'test'


@app.task()
def get_task2():  # test for every 2 mins
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RUN_DIR = BASE_DIR + '/../final_spider/'
    result = os.system(f'cd {RUN_DIR};./runscrapy')
    return f'Run Scrapy: {result}'


@app.task()
def run_scrapy():  # every day
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RUN_DIR = BASE_DIR + '/../final_spider/'
    result = os.system(f'cd {RUN_DIR};./runscrapy')
    return f'Run Scrapy: {result}'
