#!/usr/bin/env python
# -*- coding:utf-8 -*-


class StatusCodeEnum:

    Success = 2000





class BaseResponse:
    def __init__(self):
        self.status =False
        self.code = StatusCodeEnum.Success
        self.summary = None
        self.message = {}
        self.data = {}
