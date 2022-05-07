import time
import bs4
import requests
import StellarPlayer
import re
from . import iqiyi_danmu
from . import qq_danmu
from . import youku_danmu
from . import mgtv_danmu
from . import bilibili_danmu

class danmuplugin(StellarPlayer.IStellarPlayerPlugin):
    def __init__(self,player:StellarPlayer.IStellarPlayer):
        super().__init__(player)
        self.outpath = ""
    
    def start(self):
        super().start()
        self.outpath = os.path.split(os.path.realpath(__file__))[0]
    
    
    def show(self):
        controls = self.makeLayout()
        self.doModal('main',800,400,'',controls)        
    
    def makeLayout(self):
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
            {'type':'space','height':5}
        ]
        return controls
        
    def onGetDanmu(self, *args):
        url = self.player.getControlValue('main','url_edit')
        match = re.match("[\s\S]+?mgtv.com", url)
        danmu = None
        filepath = ""
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
            filepath =  danmu.get_danmu_by_url(self.outpath)
        print(filepath)
            
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