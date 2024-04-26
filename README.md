Run celery worker first with this command:

celery -A main.celery worker --beat --loglevel=info


Then run fastAPI application and hit your desired endpoint:
 uvicorn main:app --reload
