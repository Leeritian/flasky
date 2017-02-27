


from bs4 import BeautifulSoup
import requests
import re
import threading
import warnings
warnings.filterwarnings("ignore")

import re
def chromeCookie(cookie):
    result = re.split(';',cookie)
    cookies={}
    for i in result:
        name,value = i.strip().split('=',1)
        cookies[name] = value
    return cookies

def chromeHeader(header):
    header = header.split('\n')
    headers={}
    for h in header:
        name,value = h.strip().split(':',1)
        headers[name] = value
    return headers


class zodlib():
    __slots__ = ('name')    
    url = 'https://zodgame.us/forum.php?mod=forumdisplay&fid=13&page='
    cookie = {'TvTn_2132_lastcheckfeed': '203789%7C1476506511', 'TvTn_2132_st_t': '203789%7C1476606200%7Caa322ed33c011f5b51d0813a67acd403', 'TvTn_2132_checkpm': '1', 'TvTn_2132_saltkey': 'dUqu3RhF', 'TvTn_2132_st_p': '203789%7C1476605630%7C9288012b0c625e72dd724a2253da3de0', 'Hm_lpvt_ec02b01ca32261f907a08f5dad923293': '1476606198', 'TvTn_2132_forum_lastvisit': 'D_32_1476507118D_13_1476606200', 'TvTn_2132_sendmail': '1', 'TvTn_2132_lastact': '1476606202%09home.php%09spacecp', 'TvTn_2132_lastvisit': '1474887385', 'TvTn_2132_auth': '9a16mQduk2sKoUUv2x8W%2FCl%2FdopA3KA4Pk%2B8%2BrKCDMpwJnI4303p0g7XvHfjMK2hZ19vKiwKlYDt5LBVPMmGEp1CwK8', 'TvTn_2132_myrepeat_rr': 'R0', 'TvTn_2132_viewid': 'tid_140481', 'TvTn_2132_nofavfid': '1', 'Hm_lvt_ec02b01ca32261f907a08f5dad923293': '1475256732,1476506407,1476553716,1476604495', 'TvTn_2132_smile': '4D1', 'TvTn_2132_ulastactivity': '1476605606%7C0'}
    really_page=[]
    lost_page=[]
    finished = False
    
    def __init__(self,name):
        self.name=name

    def requestThreeTimes(self,url,timeout,times=3):
        cookie=self.cookie
        try:
            r=requests.get(url,verify=False,cookies=cookie,timeout=timeout)
#        except requests.exceptions.ReadTimeout:
        except Exception:
            if times > 0:
                times = times - 1
                return self.requestThreeTimes(url,timeout,times)
            else:
                return None
        return r
        
    def pachong(self,page):
        url=self.url
        cookie=self.cookie
        pattern=re.compile(self.name,re.I)
        finished=self.finished
        really_page=self.really_page
        
        r = self.requestThreeTimes(url+str(page),timeout=5)
        if not r:
            return

        bs = BeautifulSoup(r.text,'html.parser')
        table = bs.find_all('th')
        for i in range(0,len(table)):#遇到1竟然为空
            title = table[i].find_all('a')
            try:
                name = title[2]
            except IndexError:
                continue
            if re.findall(pattern, name.text):
                print(name)
                print(page)
                really_page.append(page)
                break
        print(str(page)+'页没有找到')

    def run(self,page):
        page_n=page
        thr = [threading.Thread(target=self.pachong,args=(page,)) for page in range(0,page_n)]
        for t in thr:
            t.start()
            print('go')
        for x in thr:
            t.join()
            print('this one finished')
        return self.really_page
'''
if __name__ =='__main__':
    zod = zodlib('兰斯')
    x = zod.run(50)
    print(x)
'''
