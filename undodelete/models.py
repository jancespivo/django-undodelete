# -*- coding: utf-8 -*-
import hashlib
import random

from datetime import datetime

from django.conf import settings
from django.db import models

from project.core.utils import get_random_hash

from signals import pre_soft_delete, post_soft_delete
from tasks import delete_hard

HARD_DELETE_TIME = getattr(settings, 'HARD_DELETE_TIME', 30)


def _get_random_hash():
    """
    Generates random hash using current microseconds and random number
    """
    return hashlib.md5('%s.%s' % (random.random(), datetime.now().microsecond)).hexdigest()


class SoftDeletedQuerySet(models.query.QuerySet):
    '''
    Queryset pro vsechny modely
     - zajistuje nastavovani is_deleted pri zavolani methody delete()
    '''
    def exclude_deleted(self):
        qs = self._clone()
        return qs.exclude(is_deleted=True)

    def delete(self, db_delete=False):
        if db_delete:
            super(SoftDeletedQuerySet, self).delete()
        else:
            pre_soft_delete.send(sender=self.__class__, queryset=self)
            deleted_key = 'queryset_%s' % get_random_hash()
            deleted_at = datetime.now()
            self.update(is_deleted=True, deleted_at=deleted_at, deleted_key=deleted_key)
            post_soft_delete.send(sender=self.__class__, queryset=self)

            kwargs = {
                'module': self.model.__module__,
                'cls': self.model.__name__,
                'deleted_at': deleted_at,
                'deleted_key': deleted_key
            }
            delete_hard.apply_async(kwargs=kwargs, countdown=HARD_DELETE_TIME)


class SoftDeletedManager(models.Manager):
    '''
    Base manager pro vsechny modely
     - zajistuje spravne chovani policka is_deleted
    '''
    def __init__(self, all_objects=False):
        self.all_objects = all_objects
        return super(SoftDeletedManager, self).__init__()

    def get_query_set(self):
        if self.all_objects:
            return SoftDeletedQuerySet(self.model, using=self._db)
        else:
            return SoftDeletedQuerySet(self.model, using=self._db).exclude_deleted()


class SoftDeletedModel(models.Model):
    #soft delete
    is_deleted = models.BooleanField(db_index=True, editable=False, default=False)
    deleted_at = models.DateTimeField(db_index=True, editable=False, null=True)
    deleted_key = models.CharField(max_length=255, db_index=True, editable=False, blank=True)

    objects = SoftDeletedManager()
    all_objects = SoftDeletedManager(all_objects=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        '''
        Zajistuje nastavovani is_deleted misto mazani
        '''
        if kwargs.pop('db_delete', False):
            super(SoftDeletedModel, self).delete(*args, **kwargs)
        else:
            pre_soft_delete.send(sender=self.__class__, instance=self)
            self.is_deleted = True
            self.deleted_key = _get_random_hash()
            self.deleted_at = datetime.now()
            self.save()
            post_soft_delete.send(sender=self.__class__, instance=self)

            kwargs = {
                'module': self.__module__,
                'cls': self.__class__.__name__,
                'deleted_at': self.deleted_at,
                'deleted_key': self.deleted_key
            }
            delete_hard.apply_async(kwargs=kwargs, countdown=HARD_DELETE_TIME)
