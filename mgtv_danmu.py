import re
import json
import time
import base64
import requests
import random
from uuid import uuid4
from collections import OrderedDict

chrome = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}

pno_params = {
    "pad":"1121",
    "ipad":"1030"
}

type_params = {
    "h5flash":"h5flash",
    "padh5":"padh5",
    "pch5":"pch5"
}

def duration_to_sec(duration: str):
    return sum(x * int(t) for x, t in zip([3600, 60, 1][2 - duration.count(":"):], duration.split(":")))

class mgtv_danmu():
    def __init__(self, url):
        self.url = url
        self.duration = 0
        self.vid = ''
        self.cid = ''
        self.medianame = ''

    def get_danmu_by_url(self):
        self.get_vinfos_by_url()
        danmlist = []
        danmudata = []
        if self.vid == '':
            return danmudata
        self.get_danmu_by_vid(danmlist)
        random.shuffle(danmlist)
        jsonout = {'danmu_type':'mgtv','danmu':danmlist}
        self.medianame = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "_", self.medianame)
        #outfile = path + '\\mgtv_[' + self.medianame + ']_' + str(self.vid) + '.json'
        #with open(outfile,"w", encoding='utf8') as f:
        #    json.dump(jsonout,f,sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        danmudata.append({'title':self.medianame,'data':jsonout})
        return danmudata
    
    def get_danmu_by_vid(self, comments : list):
        api_url = "https://galaxy.bz.mgtv.com/rdbarrage"
        params = OrderedDict({
            "version": "2.0.0",
            "vid": self.vid,
            "abroad": "0",
            "pid": "",
            "os": "",
            "uuid": "",
            "deviceid": "",
            "cid": self.cid,
            "ticket": "",
            "time": "0",
            "mac": "",
            "platform": "0",
            "callback": ""
        })
        index = 0
        max_index = self.duration // 60 + 1
        while index < max_index:
            params["time"] = str(index * 60 * 1000)
            try:
                r = requests.get(api_url, params=params, headers=chrome, timeout=3).content.decode("utf-8")
            except Exception as e:
                continue
            items = json.loads(r)["data"]["items"]
            index += 1
            if items is None:
                continue
            for item in items:
                newitem = {'tp':item['time'],'msg':item['content']}
                comments.append(newitem)

    def get_tk2(self,did):
        pno = pno_params["ipad"]
        ts = str(int(time.time()))
        text = f"did={did}|pno={pno}|ver=0.3.0301|clit={ts}"
        tk2 = base64.b64encode(text.encode("utf-8")).decode("utf-8").replace("+", "_").replace("/", "~").replace("=", "-")
        return tk2[::-1]

    def get_vinfo_by_vid(self,vid: str):
        api_url = "https://pcweb.api.mgtv.com/player/video"
        type_ = type_params["pch5"]
        did = uuid4().__str__()
        suuid = uuid4().__str__()
        params = OrderedDict({
            "did": did,
            "suuid": suuid,
            "cxid": "",
            "tk2": self.get_tk2(did),
            "video_id": vid,
            "type": type_,
            "_support": "10000000",
            "auth_mode": "1",
            "callback": ""
        })
        try:
            r = requests.get(api_url, params=params, headers=chrome, timeout=3).content.decode("utf-8")
        except Exception as e:
            return
        info = json.loads(r)["data"]["info"]
        self.medianame = info["title"]
        self.duration = int(info["duration"])
        self.cid = info["collection_id"]
        self.vid = vid

    def get_vinfos_by_url(self):
        # url = https://www.mgtv.com/b/323323/4458375.html
        ids = re.match("[\s\S]+?mgtv.com/b/(\d+)/(\d+)\.html", self.url)
        if ids is None:
            return 
        if ids and ids.groups().__len__() == 2:
            cid, vid = ids.groups()
            self.get_vinfo_by_vid(vid)
        return 
    
    
if __name__ == "__main__":
    r = input('请输入芒果tv视频网页地址：\n')
    dm = mgtv_danmu(r)
    dm.get_danmu_by_url('f:\\py')
    #danmu =  mgtv_danmu("https://www.mgtv.com/b/330234/7149408.html?fpa=8&fpt=1&lastp=v_play&ftl=3")
    #danmu.get_danmu_by_url('mgtv.json')