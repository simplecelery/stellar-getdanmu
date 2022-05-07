import importlib
import re
import iqiyi_danmu
import qq_danmu
import youku_danmu
import mgtv_danmu
import bilibili_danmu


def get_danmu(url,path):
    match = re.match("[\s\S]+?mgtv.com", url)
    danmu = None
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
        return danmu.get_danmu_by_url(path)
    return ""
    
    
    
if __name__ == "__main__":
    r = input('请输入视频网页地址：\n')
    get_danmu(r,'')