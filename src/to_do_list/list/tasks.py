from datetime import datetime
from itertools import islice
from .models import Task
from to_do_list.celery import app


@app.task
def save_tasks_from_csv(tasks_list, user_id):
    batch_size = 100
    tasks = (Task(
        title=task[0],
        description=task[1],
        date=task[2],
        done_date=task[3],
        author_id=user_id
    ) for task in tasks_list)

    while batch_tasks := list(islice(tasks, batch_size)):
        Task.objects.bulk_create(batch_tasks, batch_size)
