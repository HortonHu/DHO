# -*- coding: utf-8 -*-

# from __future__ import unicode_literals

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from wechat_sdk import WechatBasic, WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage


import wx_config

# 实例化微信配置
conf = WechatConf(
    token=wx_config.WECHAT_TOKEN,
    appid=wx_config.AppID,
    appsecret=wx_config.AppSecret,
    encrypt_mode='normal',
)
wechat = WechatBasic(conf=conf)


class Weixin(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Weixin, self).dispatch(*args, **kwargs)

    def get(self, request):
        # 接入时，微信的服务器发送过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        if wechat.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)

    def post(self, request):
        try:
            wechat.parse_data(request.body)
        except ParseError:
            return HttpResponse('Invalid Body Text')

        id = wechat.message.id  # 对应于 XML 中的 MsgId
        target = wechat.message.target  # 对应于 XML 中的 ToUserName
        source = wechat.message.source  # 对应于 XML 中的 FromUserName
        time = wechat.message.time  # 对应于 XML 中的 CreateTime
        type = wechat.message.type  # 对应于 XML 中的 MsgType
        raw = wechat.message.raw  # 原始 XML 文本，方便进行其他分析

        if isinstance(wechat.message, TextMessage):
            content = wechat.message.content

        xml = wechat.response_text(content='Hello World!')

        return HttpResponse(xml)



