# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from picklefield import PickledObjectField


class Location(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    iso_code = models.CharField(max_length=10, null=False, unique=True)
    lat = models.FloatField()
    long = models.FloatField()


class CachedData(models.Model):
    handle = models.CharField(max_length=255, null=False, unique=True)
    timeout = models.DateTimeField(auto_now=False)
    data = PickledObjectField()
