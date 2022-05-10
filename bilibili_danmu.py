import requests
import re
import json
import bs4
import random

class bilibili_danmu(object):
    def __init__(self, url):
        self.url = url
        self.infos = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        
    def get_danmu_by_url(self):
        self.get_cid()
        if len(self.infos) == 0:
            return None
        danmudata = []
        for info in self.infos:
            name,arr = self.get_danmu(info)
            if name != '' or arr != None:
                danmudata.append({'title':name,'data':arr})
        return danmudata
        
    def get_cid(self):
        m = re.search(r'(?<=av)\w+', self.url)
        if m:
            self.get_av_cid(m.group(0))
            return
        m = re.search(r'(?<=BV)\w+', self.url)
        if m:
            self.get_bv_cid(m.group(0))
            return
        m = re.search(r'(?<=ep)\w+', self.url)
        if  m:
            self.get_ep_cid(m.group(0))
            return
        m = re.search(r'(?<=ss)\w+', self.url)
        if  m:
            self.get_ss_cid(m.group(0))
            return
        m = re.search(r'(?<=md)\w+', self.url)
        if  m:
            self.get_md_cid(m.group(0))

    def get_danmu(self,info):
        danmu_url = "https://comment.bilibili.com/{}.xml".format(info['cid'])
        danmu_list = []
        jsonout = None
        medianame = ''
        res = requests.get(danmu_url, headers=self.headers)
        if res.status_code == 200:
            bs = bs4.BeautifulSoup(res.content.decode('UTF-8','ignore'),'html.parser')
            selector = bs.find_all('d')
            for item in selector:
                pstr = item.get('p')
                psplit = pstr.split(',')
                if len(psplit) > 0:
                    time = int(float(psplit[0]) * 1000)
                    newitem = {'tp':time,'msg':item.text}
                    danmu_list.append(newitem)
            random.shuffle(danmu_list)
            jsonout = {'danmu_type':'bilibili','danmu':danmu_list}
            info['medianame'] = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "_", info['medianame'])
            medianame = info['medianame']
        return medianame,jsonout

    def get_av_cid(self,avid):
        searchurl = 'http://api.bilibili.com/x/web-interface/view?aid=' + avid
        res = requests.get(searchurl, headers=self.headers)
        if res.status_code == 200:
            jsondata = json.loads(res.text, strict = False)
            if jsondata and jsondata['code'] == 0:
                self.infos.append({'medianame':jsondata['data']['title'],'cid':jsondata['data']['cid']})
                
    def get_bv_cid(self,bvid):
        searchurl = 'https://api.bilibili.com/x/web-interface/view?bvid=BV' + bvid
        res = requests.get(searchurl, headers=self.headers)
        if res.status_code == 200:
            jsondata = json.loads(res.text, strict = False)
            if jsondata and jsondata['code'] == 0:
                self.infos.append({'medianame':jsondata['data']['title'],'cid':jsondata['data']['cid']})
    
    def get_ep_cid(self,epid):
        searchurl = 'http://api.bilibili.com/pgc/view/web/season?ep_id=' + str(epid)
        print(searchurl)
        res = requests.get(searchurl, headers=self.headers)
        if res.status_code == 200:
            jsondata = json.loads(res.text, strict = False)
            if jsondata and jsondata['code'] == 0:
                episodes = jsondata['result']['episodes']
                for item in episodes:
                    n = re.search(r'(?<=bilibili.com/bangumi/play/ep)\w+', item["share_url"])
                    if n and n.group(0) == epid:
                        self.infos.append({'medianame':item['share_copy'],'cid':item['cid']})
                        
    
    def get_ss_cid(self,ssid):
        searchurl = 'http://api.bilibili.com/pgc/view/web/season?season_id=' + str(ssid)
        res = requests.get(searchurl, headers=self.headers)
        if res.status_code == 200:
            jsondata = json.loads(res.text, strict = False)
            if jsondata and jsondata['code'] == 0:
                episodes = jsondata['result']['episodes']
                for item in episodes:
                    self.infos.append({'medianame':item['share_copy'],'cid':item['cid']})

    def get_md_cid(self,mdid):
        searchurl = 'http://api.bilibili.com/pgc/review/user?media_id=' + str(mdid)
        res = requests.get(searchurl, headers=self.headers)
        if res.status_code == 200:
            jsondata = json.loads(res.text, strict = False)
            if jsondata and jsondata['code'] == 0:
                season_id = jsondata['result']['media']['season_id']
                self.get_ss_cid(season_id)

    def save(self, path, content):
        with open("{}.json".format(name), "a", encoding="utf-8")as f:
            f.write(json.dumps(content, ensure_ascii=False, indent=4))
            print("保存成功")

    def run(self):
        # 6 提取
        end = self.get_danmu(res_danmu, item)
        # 7 保存
        self.save(self.name, end)
        print("程序结束")

