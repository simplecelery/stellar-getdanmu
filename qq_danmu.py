import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
import bs4
import csv
import random

class qq_danmu():
    def __init__(self, url):
        self.url = url
        self.duration = 0
        self.vid = ''
        self.medianame = ''
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    def get_danmu_by_url(self):
        danmudata = []
        self.get_vid()
        if self.vid == '':
            return danmudata
        tid = self.get_tid()
        if tid == '':
            return danmudata
        jsonlist = []
        self.get_danmu(tid,jsonlist)
        random.shuffle(jsonlist)
        jsonout = {'danmu_type':'qq','danmu':jsonlist}
        self.medianame = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "_", self.medianame)
        #outfile = path + '\\qq_[' + self.medianame + ']_' + str(tid) + '.json'
        #with open(outfile,"w", encoding='utf8') as f:
        #    json.dump(jsonout,f,sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        danmudata.append({'title':self.medianame,'data':jsonout})
        return danmudata

    def get_vid(self):
        #getting lid,cid,vid
        res = requests.get(self.url,verify=False)
        if res.status_code == 200:
            bs = bs4.BeautifulSoup(res.content.decode('UTF-8','ignore'),'html.parser')
            jsonstr = ''
            for item in bs.find_all('script'):
                data = re.findall(r"var VIDEO_INFO = (.+)",item.text)
                if len(data) > 0:
                    jsonstr = data[0]
                    break
            if jsonstr == '':
                return
            jsondata = json.loads(jsonstr)
            self.vid = jsondata['vid']
            self.duration = int(jsondata['duration']) 
            self.medianame = jsondata['title']
            
    def get_tid(self):
        #getting targetid
        vid = self.vid
        print("getting targetid")
        url = 'https://access.video.qq.com/danmu_manage/regist?vappid=97767206&vsecret=c0bdcbae120669fff425d0ef853674614aa659c605a613a4&raw=1'
        headers = {
            'User-Agent':"PostmanRuntime/7.19.0",
            'Postman-Token':'ecb9a8ff-480b-4c63-af22-da18d327375d',
            'Host':'access.video.qq.com',
            'Content-Type':'application/json',
            'Accept':'*/*',
            'Cache-Control':'no-cache',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive'
            }
        payload ={"wRegistType":2,"vecIdList":[vid],"wSpeSource":0,"bIsGetUserCfg":1,"mapExtData":{vid:{"strCid":"wu1e7mrffzvibjy","strLid":""}}}
        r=requests.post(url,headers=headers,data=json.dumps(payload))
        id_compile = re.compile("targetid=([\d]*)&vid")
        targetid = id_compile.findall(r.text)
        return targetid[0]

    def get_danmu(self,targetid,jsonlist):
        timestamp = 0
        while timestamp < self.duration:
            url = 'http://mfm.video.qq.com/danmu?target_id={}&timestamp={}'.format(targetid,timestamp)
            timestamp = timestamp + 30
            res = requests.get(url,verify=False)
            if res.status_code == 200:
                jsondata = json.loads(res.text, strict=False)
                if jsondata:
                    for item in jsondata['comments']:
                        tp = int(item['timepoint']) * 1000
                        newitem = {'tp':tp,'msg':item['content']}
                        jsonlist.append(newitem)
            

if __name__ == '__main__':
    r = input('请输入qq视频网页地址：\n')
    dm = qq_danmu(r)
    dm.get_danmu_by_url('f:\\py')