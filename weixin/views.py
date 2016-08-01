# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context

from xml.etree import ElementTree as ET

# from wechat_sdk import WechatBasic
# from wechat_sdk.exceptions import ParseError
# from wechat_sdk.messages import TextMessage

import time
import hashlib

import wx_config

WECHAT_TOKEN = wx_config.WECHAT_TOKEN
AppID = wx_config.AppID
AppSecret = wx_config.AppSecret


class Weixin(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Weixin, self).dispatch(*args, **kwargs)

    def get(self, request):
        # 下面这四个参数是在接入时，微信的服务器发送过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        # 把token，timestamp, nonce放在一个序列中，并且按字符排序
        hashlist = [WECHAT_TOKEN, timestamp, nonce]
        hashlist.sort()

        # 将上面的序列合成一个字符串
        hashstr = ''.join([s for s in hashlist])

        # 通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
        hashstr = hashlib.sha1(hashstr).hexdigest()

        # 把我们生成的字符串和微信服务器发送过来的字符串比较，
        # 如果相同，就把服务器发过来的echostr字符串返回去
        if hashstr == signature:
            return HttpResponse(echostr)

    def post(self, request):
        # 通过xml.etree.ElementTree.fromstring将接收到数据字符串转成xml
        str_xml = ET.fromstring(request.body)

        # 从xml中读取我们需要的数据。注意这里使用了from接收的to，使用to接收了from，
        # 这是因为一会我们还要用这些数据来返回消息，这样一会使用看起来更符合逻辑关系
        fromUser = str_xml.find('ToUserName').text
        toUser = str_xml.find('FromUserName').text
        content = str_xml.find('Content').text

        # 这里获取当前时间的秒数，time.time()取得的数字是浮点数，所以有了下面的操作
        nowtime = str(int(time.time()))

        # 加载text.xml模板
        t = loader.get_template('weixin/text.xml')
        # 将我们的数据组成Context用来render模板。
        c = Context({'toUser': toUser, 'fromUser': fromUser,
                     'nowtime': nowtime, 'content': 'hello world'})

        return HttpResponse(t.render(c))


# 实例化 WechatBasic
# wechat_instance = WechatBasic(
#     token=WECHAT_TOKEN,
#     appid=AppID,
#     appsecret=AppSecret
# )


# @csrf_exempt
# def index(request):
#     if request.method == 'GET':
#         # 检验合法性
#         # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
#         signature = request.GET.get('signature')
#         timestamp = request.GET.get('timestamp')
#         nonce = request.GET.get('nonce')
#
#         if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
#             return HttpResponseBadRequest('Verify Failed')
#         else:
#             return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")
#
#     # 解析本次请求的 XML 数据
#     try:
#         wechat_instance.parse_data(data=request.body)
#     except ParseError:
#         return HttpResponseBadRequest('Invalid XML Data')
#
#     # 获取解析好的微信请求信息
#     message = wechat_instance.get_message()
#
#     # 关注事件以及不匹配时的默认回复
#     response = wechat_instance.response_text(
#         content=(
#             '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容开始聊天'
#             '\n【<a href="http://www.ziqiangxuetang.com">自强学堂手机版</a>】'
#         ))
#     if isinstance(message, TextMessage):
#         # 当前会话内容
#         content = message.content.strip()
#         if content == '功能':
#             reply_text = (
#                 '目前支持的功能：\n1. 关键词后面加上【教程】两个字可以搜索教程，'
#                 '比如回复 "Django 后台教程"\n'
#                 '2. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'
#                 '还有更多功能正在开发中哦 ^_^\n'
#                 '【<a href="http://www.ziqiangxuetang.com">自强学堂手机版</a>】'
#             )
#         elif content.endswith('教程'):
#             reply_text = '您要找的教程如下：'
#
#         response = wechat_instance.response_text(content=reply_text)
#
#     return HttpResponse(response, content_type="application/xml")
