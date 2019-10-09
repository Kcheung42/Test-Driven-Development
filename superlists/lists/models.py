# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# TODO: Support more than one list
class Item(models.Model):
	text = models.TextField(default="")
