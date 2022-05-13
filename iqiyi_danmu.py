import requests
import zlib
import re
import random
import json
from bs4 import BeautifulSoup

def randomUn(n):
    s = pow(10,n-1)
    e = pow(10,n)-1
    res = random.random() *(e - s) + s
    return res

class iqiyi_danmu():
    def __init__(self, url):
        self.url = url
        self.medianame = ''
        self.tvID = ''
        self.albumID = ''
        self.channelId = ''
        self.duration = ''

    def get_danmu_by_url(self):
        self.get_danmu_config()
        print('1------------')
        print(self.tvID)
        danmudata = []
        if self.tvID == '':
            return danmudata
        jsonlist = []
        self.get_danmu(jsonlist)
        random.shuffle(jsonlist)
        jsonout = {'danmu_type':'iqiyi','danmu':jsonlist}
        self.medianame = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "_", self.medianame)
        #outfile = path + '\\iqiyi_[' + self.medianame + ']_' + self.tvID + '.json'
        #with open(outfile,"w", encoding='utf8') as f:
        #    json.dump(jsonout,f,sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        danmudata.append({'title':self.medianame,'data':jsonout})
        return danmudata

    def get_danmu_config(self):
        self.medianame = ''
        self.tvID = ''
        self.albumID = ''
        self.channelId = ''
        self.duration = ''
        r = requests.get(self.url)
        if r.status_code == 200:
            try:
                self.medianame = re.findall(":page-info=[\s\S]+?\S+\"tvName\":\"(.*?)\"",r.text)[0]
                self.tvID = re.findall(r"param\['tvid'\] = \"(\d+)\"",r.text)[0]
                self.albumID = re.findall(r"param\['albumid'\] = \"(\d+)\"",r.text)[0]
                self.channelId = re.findall(r"param\['channelID'\] = \"(\d+)\"",r.text)[0]
                self.duration = re.findall(":video-info=[\s\S]+?\S+\"duration\":(\d+)",r.text)[0]
            except:
                paramstr = re.findall("window.Q.PageInfo.playPageInfo=(.+?);",r.text)
                if len(paramstr) > 0:
                    jsonstr = paramstr[0]
                    Jsondata = json.loads(jsonstr)
                    if (Jsondata):
                        self.medianame = Jsondata['name']
                        self.tvID = str(Jsondata['tvId'])
                        self.albumID = Jsondata['albumId']
                        self.channelId = Jsondata['channelId']
                        durationstr = Jsondata['duration']
                        durationstrlist = durationstr.split(':')
                        dorationval = 0
                        for item in durationstrlist:
                            val = int(item)
                            dorationval = dorationval * 60 + val
                        self.duration = str(dorationval)
        return

    def get_danmu(self,jsonlist):
        ##getting danmu
        page = int(self.duration) // (60 * 5) + 1
        for i in range(1, page + 1):
            rn = "0.{}".format(randomUn(16)) 
            url = 'https://cmts.iqiyi.com/bullet/{}/{}/{}_300_{}.z?rn={}&business=danmu&is_iqiyi=true&is_video_page=true&tvid={}&albumid={}&categoryid={}&qypid=01010021010000000000'.format(
                self.tvID[-4:-2],self.tvID[-2:],self.tvID,i,rn,self.tvID,self.albumID,self.channelId)
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    res = zlib.decompress(r.content)
                except:
                    ##!!!!!!fault in getting zip
                    print('!!!!!!fault in getting zip')
                    print(url)
                    print(r.content[100:1000])
                    continue
                res = res.decode('utf-8')
                compile = re.compile("(<bulletInfo>[\s\S]*?</bulletInfo>)")
                danmu_list = compile.findall(res)
                for danmu in danmu_list:
                    danmu_json = {}
                    content_list = re.findall(">(\S*?)</",danmu)
                    try:
                        if content_list[1] != '0':
                            #danmu_json["contentId"] = content_list[0] + '#'#'#'用于防止数字在csv中被省化
                            danmu_json["msg"] = content_list[1]
                            #danmu_json["parentId"] = content_list[2]
                            danmu_json["tp"] = int(content_list[3]) * 1000
                            #danmu_json["font"] = content_list[4]
                            #danmu_json["color"] = content_list[5]
                            #danmu_json["opacity"] = content_list[6]
                            #danmu_json["position"] = content_list[7]
                            #danmu_json["background"] = content_list[8]
                            #danmu_json["contentType"] = content_list[9]
                            #danmu_json["isReply"] = content_list[10]
                            #danmu_json["likeCount"] = content_list[11]
                            #danmu_json["plusCount"] = content_list[12]
                            #danmu_json["dissCount"] = content_list[13]
                            #danmu_json["senderAvatar"] = content_list[14]
                            #danmu_json["uid"] = content_list[15]
                            #danmu_json["udid"] = content_list[16]
                            #if len(content_list) > 17:
                            #    danmu_json["name"] = content_list[17]
                            #else:
                            #    danmu_json["name"] = " "
                            jsonlist.append(danmu_json)
                    except:
                        ## !!!!fault in danmu_json
                        print('!!!!fault in danmu_json')
                        print(danmu_json)