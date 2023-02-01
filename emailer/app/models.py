# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'topic'
        verbose_name = 'Тема рассылки'
        verbose_name_plural = 'Темы рассылок'
        ordering = ['id']


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    topics = models.ManyToManyField(to=Topic, blank=True, related_name='customers')

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)

    class Meta:
        db_table = 'customer'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']


class NewsLetter(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.SET_NULL, related_name='newsletters')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    run_immediately = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return '{}, topic: {}, created at: {}, run immediately: {}'.format(
            self.title, self.topic, self.created_at, self.run_immediately)

    class Meta:
        db_table = 'newsletter'
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-created_at']


class Tracking(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, related_name='trackings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='trackings')
    sent_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(blank=True, null=True, editable=False)
    error_on_send = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '{} {} {}, sent at: {}'.format(self.id, self.newsletter, self.customer.id, self.sent_at)

    class Meta:
        db_table = 'tracking'
        verbose_name = 'Результат рассылки'
        verbose_name_plural = 'Результаты рассылок'
        ordering = ['-sent_at']
