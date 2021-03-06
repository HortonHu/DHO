# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from models import Fowler, Dialog, Location, Function

from wechat_sdk import WechatConf, WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, LocationMessage, EventMessage, ImageMessage, VoiceMessage, \
    VideoMessage, ShortVideoMessage, LinkMessage

from weixin_conf import token, appid, appsecret, encrypt_mode
# 微信SDK配置
conf = WechatConf(token=token,
                  appid=appid,
                  appsecret=appsecret,
                  encrypt_mode=encrypt_mode,
                  )
wechat = WechatBasic(conf=conf)


class Weixin(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Weixin, self).dispatch(*args, **kwargs)

    def get(self, request):
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

        id = wechat.message.id              # MsgId
        target = wechat.message.target      # ToUserName
        source = wechat.message.source      # FromUserName
        time = wechat.message.time          # CreateTime
        type = wechat.message.type          # MsgType
        raw = wechat.message.raw            # 原始 XML 文本

        # get_or_create会得到一个tuple (object, created)
        fowler = Fowler.objects.get_or_create(OpenID=source)[0]

        if isinstance(wechat.message, TextMessage):
            keywords = [func.keyword for func in Function.objects.all()]
            content = wechat.message.content                # 对应于 XML 中的 Content
            if content in keywords:
                reply = Function.objects.get(keyword=content).explain
            elif content == "功能":
                reply = "本公众号支持的回复有： \n" + "，".join(keywords)
            else:
                reply = "回复'功能'了解本公众号提供的全部功能"
            self.save_dialog(content=content, reply=reply, fowler=fowler)
            rsp_xml = wechat.response_text(content=reply, escape=True)
            return HttpResponse(rsp_xml)

        elif isinstance(wechat.message, LocationMessage):
            location = wechat.message.location
            scale = wechat.message.scale
            label = wechat.message.label

            loc = Location(fowler=fowler, x=location[0], y=location[1], label=label)
            loc.save()
            rsp_xml = wechat.response_text(content="已收到您的地理位置")
            return HttpResponse(rsp_xml)

        elif isinstance(wechat.message, ImageMessage):
            picurl = wechat.message.picurl
            media_id = wechat.message.media_id
            rsp_xml = wechat.response_image(media_id=media_id)
            return HttpResponse(rsp_xml)

        elif isinstance(wechat.message, VoiceMessage):
            media_id = wechat.message.media_id
            format = wechat.message.format
            recognition = wechat.message.recognition
            rsp_xml = wechat.response_voice(media_id=media_id)
            return HttpResponse(rsp_xml)

        elif isinstance(wechat.message, (VideoMessage, ShortVideoMessage)):
            media_id = wechat.message.media_id
            thumb_media_id = wechat.message.thumb_media_id
            rsp_xml = wechat.response_video(media_id=media_id,
                                            title='视频标题是media_id:' + str(media_id),
                                            description='视频描述是thumb_media_id:' + str(thumb_media_id))
            return HttpResponse(rsp_xml)

        elif isinstance(wechat.message, LinkMessage):
            title = wechat.message.title
            description = wechat.message.description
            url = wechat.message.url
            rsp_xml = wechat.response_text(content=' '.join([url, title, description]))
            return HttpResponse(rsp_xml)

        elif isinstance(wechat.message, EventMessage):
            if wechat.message.type == 'subscribe':
                fowler.activate = 1
                fowler.save()
                rsp_xml = wechat.response_text(content="欢迎关注本公众号\n回复'功能'了解本公众号提供的全部功能",
                                               escape=True)
                return HttpResponse(rsp_xml)
            elif wechat.message.type == 'unsubscribe':
                fowler.activate = 0
                fowler.save()
        else:
            rsp_xml = wechat.response_text(content="回复'功能'了解本公众号提供的全部功能")
            return HttpResponse(rsp_xml)

    @staticmethod
    def save_dialog(content, reply, fowler):
        dialog = Dialog(message=content, reply=reply, fowler=fowler)
        dialog.save()


class Token(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Token, self).dispatch(*args, **kwargs)

    def get(self, request):
        try:
            access_token = json.dumps(wechat.get_access_token())
        except Exception, e:
            access_token = 'Error is %s' % e
        return HttpResponse(access_token)

