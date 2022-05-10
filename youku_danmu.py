import json
import requests
import re
import bs4
import csv
import time
import base64
import hashlib
import urllib.request
import random

chrome = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}

def matchit(patterns, text):
    ret = None
    for pattern in patterns:
        match = re.match(pattern, text)
        if match:
            ret = match.group(1)
            break
    return ret

def yk_msg_sign(msg: str):
    return hashlib.new("md5", bytes(msg + "MkmC9SoIw6xCkSKHhJ7b5D2r51kBiREr", "utf-8")).hexdigest()

def yk_t_sign(token, t, appkey, data):
    text = "&".join([token, t, appkey, data])
    return hashlib.new('md5', bytes(text, 'utf-8')).hexdigest()

def get_tk_enc():
    api_url = "https://acs.youku.com/h5/mtop.com.youku.aplatform.weakget/1.0/?jsv=2.5.1&appKey=24679788"
    try:
        r = requests.get(api_url, headers=chrome, timeout=5)
    except Exception as e:
        return
    tk_enc = dict(r.cookies)
    if tk_enc.get("_m_h5_tk_enc") and tk_enc.get("_m_h5_tk"):
        return tk_enc
    return
    
def get_cna():
    api_url = "https://log.mmstat.com/eg.js"
    try:
        r = requests.get(api_url, headers=chrome, timeout=5)
    except Exception as e:
        return
    cookies = dict(r.cookies)
    if cookies.get("cna"):
        return cookies["cna"]
    return
    
class youku_danmu():
    def __init__(self, url):
        self.url = url
        self.vid = None
        self.duration = 0
        self.medianame = ''

    def get_danmu_by_url(self):
        danmudata = []
        cna = get_cna()
        danmlist = []
        if cna is None:
            return danmudata
        self.vid,self.duration = self.get_vinfos_by_video_id()
        if self.vid is None:
            return danmudata
        max_mat = self.duration // 60 + 1
        for mat in range(max_mat):
            result = self.get_danmu_by_mat(cna, mat + 1,danmlist)
        random.shuffle(danmlist)
        jsonout = {'danmu_type':'youku','danmu':danmlist}
        self.medianame = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "_", self.medianame)
        #outfile = path + '\\youku_[' + self.medianame + ']_' + str(self.vid) + '.json'
        #with open(outfile,"w", encoding='utf8') as f:
        #    json.dump(jsonout,f,sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        danmudata.append({'title':self.medianame,'data':jsonout})
        return danmudata
        
    def get_vinfos_by_video_id(self):
        vid_patterns = ["[\s\S]+?youku.com/video/id_(/+?)\.html", "[\s\S]+?youku.com/v_show/id_(.+?)\.html"]
        video_id = matchit(vid_patterns, self.url)
        duration = 0
        if video_id:
            api_url = "https://openapi.youku.com/v2/videos/show.json?client_id=53e6cc67237fc59a&package=com.huawei.hwvplayer.youku&ext=show&video_id={}".format(video_id)
            try:
                r = requests.get(api_url, headers=chrome, timeout=5).content.decode("utf-8")
            except Exception as e:
                print("get_vinfos_by_video_id error info -->", e)
                return None
            data = json.loads(r)
            if data.get("duration"):
                duration = int(float(data["duration"]))
            if data.get("title"):
                self.medianame = data["title"]
        return video_id,duration
        
    def get_danmu_by_mat(self, cna, mat : int, danmulist : list):
        comments = []
        api_url = "https://acs.youku.com/h5/mopen.youku.danmu.list/1.0/"
        tm = str(int(time.time() * 1000))
        msg = {
            "ctime": tm,
            "ctype": 10004,
            "cver": "v1.0",
            "guid": cna,
            "mat": mat,
            "mcount": 1,
            "pid": 0,
            "sver": "3.1.0",
            "type": 1,
            "vid": self.vid}
        msg_b64encode = base64.b64encode(json.dumps(msg, separators=(',', ':')).encode("utf-8")).decode("utf-8")
        msg.update({"msg":msg_b64encode})
        msg.update({"sign":yk_msg_sign(msg_b64encode)})
        #只要有Cookie的_m_h5_tk和_m_h5_tk_enc就行
        tk_enc = get_tk_enc()
        if tk_enc is None:
            return
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Cookie":";".join([k + "=" + v for k, v in tk_enc.items()]),
            "Referer": "https://v.youku.com"
        }
        headers.update(chrome)
        t = str(int(time.time() * 1000))
        data = json.dumps(msg, separators=(',', ':'))
        params = {
            "jsv":"2.5.6",
            "appKey":"24679788",
            "t":t,
            "sign":yk_t_sign(tk_enc["_m_h5_tk"][:32], t, "24679788", data),
            "api":"mopen.youku.danmu.list",
            "v":"1.0",
            "type":"originaljson",
            "dataType":"jsonp",
            "timeout":"20000",
            "jsonpIncPrefix":"utility"
        }
        try:
            r = requests.post(api_url, params=params, data={"data":data}, headers=headers, timeout=5).content.decode("utf-8")
        except Exception as e:
            print("youku danmu request failed.", e)
            return "once again"
        jsondata = json.loads(json.loads(r)["data"]["result"],strict = False)["data"]["result"]
        for item in jsondata:
            newitem = {'tp':item['playat'],'msg':item['content']}         
            danmulist.append(newitem)
        return

    
if __name__ == '__main__':
    r = input('请输入youku视频网页地址：\n')
    dm = youku_danmu(r)
    dm.get_danmu_by_url('f:\\py')
    #danmu = youku_danmu('https://v.youku.com/v_show/id_XNTEzMTc4NjIxMg==.html?spm=a2ha1.14919748_WEBHOME_GRAY.drawer9.d_zj2_2&s=aefa99985ae94504ab68&scm=20140719.apircmd.29071.show_aefa99985ae94504ab68')
    #danmu.get_danmu_by_url('youku.json')
