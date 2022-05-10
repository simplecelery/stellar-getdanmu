import time
import bs4
import requests
import StellarPlayer
import re
import os
import sys
from . import iqiyi_danmu
from . import qq_danmu
from . import youku_danmu
from . import mgtv_danmu
from . import bilibili_danmu

class danmuplugin(StellarPlayer.IStellarPlayerPlugin):
    def __init__(self,player:StellarPlayer.IStellarPlayer):
        super().__init__(player)
        self.danmudata = []
    
    def start(self):
        super().start()
    
    
    def show(self):
        controls = self.makeLayout()
        self.doModal('main',800,400,'',controls)        
    
    def makeLayout(self):
        danmu_layout = [
            {'type':'link','name':'title','fontSize':15,'@click':'onDanmuClick'}
        ]
        controls = [
            {'type':'space','height':5},
            {
                'group':[
                    {'type':'edit','name':'url_edit','label':'网页地址','width':0.7},
                    {'type':'button','name':'解析','@click':'onGetDanmu','width':100},
                ],
                'width':1.0,
                'height':30
            },
            {'type':'label','name':'desc','textColor':'#ff7f00','fontSize':15,'value':'请输入bilibili、芒果tv、爱奇艺、腾讯视频、优酷的视频页面地址','height':40},
            {'type':'label','name':'list','textColor':'#557f55','fontSize':15,'value':'爬取的弹幕列表:','height':40},
            {'type':'grid','name':'danmugrid','itemlayout':danmu_layout,'value':self.danmudata,'itemheight':30,'itemwidth':775,'height':280,'width':1.0},
        ]
        return controls
        
    def onGetDanmu(self, *args):
        url = self.player.getControlValue('main','url_edit')
        match = re.match("[\s\S]+?mgtv.com", url)
        danmu = None
        self.danmudata = []
        medianame = ""
        if match:
            danmu = mgtv_danmu.mgtv_danmu(url)
        match = re.match("[\s\S]+?v.qq", url)
        if match:
            danmu = qq_danmu.qq_danmu(url)
        match = re.match('[\s\S]+?iqiyi.com', url)
        if match:
            danmu = iqiyi_danmu.iqiyi_danmu(url)
        match = re.match("[\s\S]+?youku.com", url)
        if match:
            danmu = youku_danmu.youku_danmu(url)
        match = re.match("[\s\S]+?bilibili.com", url)
        if match:
            danmu = bilibili_danmu.bilibili_danmu(url)
        if danmu:
            self.loading()
            self.danmudata = danmu.get_danmu_by_url()
            self.loading(True)
            self.player.updateControlValue('main','danmugrid',self.danmudata)
        else:
            self.player and self.player.toast('main','不支持的网站')

    def onDanmuClick(self, page, listControl, item, itemControl):
        print(item)
        print(len(self.danmudata))
        if len(self.danmudata) > item:
            danmu_list =  self.danmudata[item]['data']['danmu']
            self.player.showDanmu(True)
            print(danmu_list)
            self.player.batchAddDanmu(danmu_list)
        
    def playMovieUrl(self,playpageurl):
        return
        
    def loading(self, stopLoading = False):
        if hasattr(self.player,'loadingAnimation'):
            self.player.loadingAnimation('main', stop=stopLoading)
        
def newPlugin(player:StellarPlayer.IStellarPlayer,*arg):
    plugin = danmuplugin(player)
    return plugin

def destroyPlugin(plugin:StellarPlayer.IStellarPlayerPlugin):
    plugin.stop()