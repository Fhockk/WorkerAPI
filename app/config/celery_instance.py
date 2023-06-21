from celery import Celery


def make_celery():
    celery = Celery()
    return celery


celery = make_celery()
