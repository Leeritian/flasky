# version 0.1
# 个人练习用
# 依赖弹幕分析 视频的精彩部分
# 此版本暂不支持历史弹幕，及分P弹幕，分P弹幕的弹幕地址为CID+1
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

av = 11181699
class danmu_spider():
    aurl = 'http://www.bilibili.com/video/av'
    curl = 'http://comment.bilibili.com/%s.xml'

    def __init__(self, av):
        self.av = av
        self.html = requests.get(self.aurl + str(self.av))
        self.soup = BeautifulSoup(self.html.text, 'html.parser')
        script=self.soup.find_all('script')[14]
        ppp=re.compile(r'cid=\d+')
        self.cid = re.search(ppp,script.text).group(0).split('=')[1]
        self.danmus = requests.get(self.curl%self.cid).text.split(r'</d>')
        

    def danmu_fenbu_show(self):
        import numpy as np
        import matplotlib.pyplot as plt
        fenbu=[]
        for danmu in self.danmus[1:]:
            time = danmu[8:].split(',')[0]
#            data = danmu.split('>')[1]
            try:
#        time=int((float(time))/10)
                fenbu.append(float(time))
#        fenbu.append((time,data))
            except Exception:
                pass
        danmu_fenbu = np.array(self.fenbu)
        plt.hist(danmu_fenbu,round(max(fenbu)/10))
        plt.show()

    def show_topN(self,n):
        fenbu=[]
        for danmu in self.danmus[1:]:
            time = danmu[8:].split(',')[0]

#            data = danmu.split('>')[1]
            try:#删掉前20s的弹幕
                time=int((float(time))/10)
                if time < 2:
                    continue
                fenbu.append(float(time))
#        fenbu.append((time,data))
            except Exception:
                pass
        c = Counter()
        for i in fenbu:
            c[i]+=1
        dlist = c.most_common()
        dlist.sort(key = lambda x:x[1],reverse=True)
        top_n = c.most_common(n)

        for top in top_n:
            print('%d---%d s have %d danmu'%(top[0]*10,(top[0]+1)*10,top[1]))

#todo: 弹幕中抢第一的无意义弹幕占了重比例，所以要进行弹幕清洗

if __name__ =='__main__':
    av = 11181699
    test = danmu_spider(av)

