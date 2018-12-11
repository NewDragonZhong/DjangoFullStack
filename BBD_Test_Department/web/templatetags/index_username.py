# -*- coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
from web import models
from django.shortcuts import render, HttpResponse
import json


register = template.Library()

@register.filter()
def index_user(nid):
    # username = models.UserInfo.objects.filter(nid=nid).values("username")[0]


    pass

