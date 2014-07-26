# -*- coding: utf-8 -*-
from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
#app.config_from_object({
    #'BROKER_URL': 'redis://localhost:6379/0',
    #'BROKER_TRANSPORT_OPTIONS': {'visibility_timeout': 3600},
    #'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0',
    #'CELERY_IMPORTS': ("project.softdelete",)
#})


@celery.task(name='delete_hard')
def delete_hard(module=None, cls=None, deleted_at=None, deleted_key=None):
    from importlib import import_module
    getattr(import_module(module), cls).all_objects.filter(
        is_deleted=True,
        deleted_at=deleted_at,
        deleted_key=deleted_key
    ).delete(db_delete=True)
