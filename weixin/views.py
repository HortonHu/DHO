# -*- coding: utf-8 -*-

# from __future__ import unicode_literals

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from wechat_sdk import WechatBasic, WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, LocationMessage, EventMessage


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

        # 公共信息
        id = wechat.message.id              # 对应于 XML 中的 MsgId
        target = wechat.message.target      # 对应于 XML 中的 ToUserName
        source = wechat.message.source      # 对应于 XML 中的 FromUserName
        time = wechat.message.time          # 对应于 XML 中的 CreateTime
        type = wechat.message.type          # 对应于 XML 中的 MsgType
        raw = wechat.message.raw            # 原始 XML 文本，方便进行其他分析

        # 接收消息类型：
        # 文字
        if isinstance(wechat.message, TextMessage):
            content = wechat.message.content                # 对应于 XML 中的 Content
            xml = wechat.response_text(content='您发送的信息类型是{}'.format(type))
        # 地理位置
        elif isinstance(wechat.message, LocationMessage):
            location = wechat.message.location              # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
            scale = wechat.message.scale                    # 对应于 XML 中的 Scale
            label = wechat.message.label                    # 对应于 XML 中的 Label
        # 事件
        elif isinstance(wechat.message, EventMessage):
            if wechat.message.type == 'subscribe':          # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                key = wechat.message.key                    # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
                ticket = wechat.message.ticket              # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
            elif wechat.message.type == 'unsubscribe':      # 取消关注事件（无可用私有信息）
                pass
            elif wechat.message.type == 'scan':             # 用户已关注时的二维码扫描事件
                key = wechat.message.key                    # 对应于 XML 中的 EventKey
                ticket = wechat.message.ticket              # 对应于 XML 中的 Ticket
            elif wechat.message.type == 'location':         # 上报地理位置事件
                latitude = wechat.message.latitude          # 对应于 XML 中的 Latitude
                longitude = wechat.message.longitude        # 对应于 XML 中的 Longitude
                precision = wechat.message.precision        # 对应于 XML 中的 Precision
            elif wechat.message.type == 'click':            # 自定义菜单点击事件
                key = wechat.message.key                    # 对应于 XML 中的 EventKey
            elif wechat.message.type == 'view':             # 自定义菜单跳转链接事件
                key = wechat.message.key                    # 对应于 XML 中的 EventKey
            elif wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
                status = wechat.message.status              # 对应于 XML 中的 Status
            elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                                         'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
                key = wechat.message.key                    # 对应于 XML 中的 EventKey
            xml = wechat.response_text(content='您发送的信息类型是{}'.format(type))
        else:
            xml = wechat.response_text(content="回复'功能'了解本公众号提供的查询功能")
        return HttpResponse(xml)



