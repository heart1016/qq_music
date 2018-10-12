import requests
import json
import asyncio
import aiohttp
from lxml import etree
from pyquery import PyQuery as pq
import os
import base64
from random import random
from time import time

class ProgressBar(object):

    def __init__(self, file_name, total):
        super().__init__()
        self.file_name = file_name
        self.count = 0
        self.prev_count = 0
        self.total = total
        self.end_str = '\r'

    def __get_info(self):
        return 'Progress: {:6.2f}%, {:8.2f}MB, [{:.100}]'\
            .format(self.count/self.total*100, self.total/1024/1024, self.file_name)

    def refresh(self, count):
        self.count += count
          # Update progress if down size > 10k
        if (self.count - self.prev_count) > 10240:
            self.prev_count = self.count
            print(self.__get_info(), end=self.end_str)
          # Finish downloading
        if self.count >= self.total:
            self.end_str = '\n'
            print(self.__get_info(), end=self.end_str)


def download_file(file_name, file_url):
    #guid = int(random() * 2147483647) * int(time() * 1000) % 10000000000
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Cookie': 'qqmusic_fromtag=85;qqmusic_uin=2418090286;qqmusic_key=B900BBEF65F56D7FFDC18A105976CC14011CC52E2013B01CE7C859DDD903B7D9;wxopenid= ;wxrefresh_token= ;downkey=123455789abcdefaaee',
        'Referer': '111.202.98.148'
    }
    response = requests.get(url=file_url, stream=True, headers=headers)
    length = int(response.headers.get('Content-Length'))
    file_path = os.path.join('song', file_name)
    if os.path.exists(file_path) and os.path.getsize(file_path) == length:
        return True
    else:
        progress = ProgressBar(file_path, length)
    with open(file_path, 'wb') as f:
        for check in response.iter_content(1024):
            f.write(check)
            progress.refresh(len(check))
        return False

def mapmid():
    url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid=2405963402&format=jsonp&g_tk=1925068772&jsonpCallback=playlistinfoCallback&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&song_begin=0&song_num=30'
    headers = {
        'authority': 'c.y.qq.com',
        'method': 'G',
        'path': '/splcloud/fcgi-bin/fcg_musiclist_getmyfav.fcg?dirid=201&dirinfo=1&g_tk=368405133&jsonpCallback=MusicJsonCallback3773956251153032&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie':'RK=v+HSxU5PGX; ptcz=17e3eacf682afd33b90f60d360778ccc68e654bada5bb65f335efc6a492f3ead; pgv_pvi=9761964032; pgv_pvid=2532527580; eas_sid=P1Y581u3a2B3D7E164Y5M8f2o4; tvfe_boss_uuid=c837ea95128d2c3f; ts_uid=3470501600; o_cookie=1521324101; pac_uid=1_1521324101; ptui_loginuin=2418090286; pt2gguin=o2418090286; pgv_info=ssid=s5340469438; pgv_si=s5681572864; _qpsvr_localtk=0.023101170318901243; uin=o2418090286; skey=@NOcUSQMnt; ptmbsig=184e9bcc5b672d757fabe6e1a9ec6d32385c801fcacb8517683218829047512aecc3d17f4fe5fd34; p_uin=o2418090286; pt4_token=AC2AlYDghnFTHPB-zkya4WzmOH*LHocmW9INqo*8UoU_; p_skey=rFhOTK4nNq5MKLbAl1Yj1-eL4j7QKD8kFxqBlEwBFFg_; ts_refer=ui.ptlogin2.qq.com/cgi-bin/mibao_vry%3Ftarget%3D2%26jump_login%3D0%26uin%3D2418090286%26pt_mbkey%3Dbc911da2affa42abaa7f04402d0c410ccbf58e7f6051a; yqq_stat=0; player_exist=1; yq_playschange=0; yq_playdata=; qqmusic_fromtag=66; yq_index=0; yplayer_open=1; ts_last=y.qq.com/n/yqq/playlist/2405963402.html',
        'dnt': '1',
        'referer': 'https://y.qq.com/portal/profile.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }
    json_dict = requests.get(url=url, headers=headers).text
    json_dict = json_dict[21:len(json_dict)-1]
    json_dict = json.loads(json_dict)
    i = 0
    while True:
        for key in json_dict['cdlist'][0]['songlist']:
            ss ='https://y.qq.com/n/yqq/song/{}.html'.format(key['songmid'])
            print(ss)
            print(i,key['songname'],key['songmid'], key['albummid'])
            print(key['size128']/1024/1024,key['size320']/1024/1024,key['sizeflac']/1024/1024)
            yinyue = YinYue(ss, key['songmid'], key['albummid'])
            yinyue.get_name()
            a = yinyue.get_params()
            if a:
                continue
            yinyue.get_quality()
            yinyue.download_music()
            yinyue.download_pic()
            yinyue.download_lrc()
            #a = yinyue.download_music()
            #if a:
            #    print('flac file already download:', key['songname'])
            #p = yinyue.download_pic()
            #if p:
            #    print('pic file already download:', key['songname'])
            i+=1
            url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid=2405963402&format=jsonp&g_tk=1925068772&jsonpCallback=playlistinfoCallback&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&song_begin={}&song_num=30'.format(i)
            json_dict = requests.get(url=url, headers=headers).text
            json_dict = json_dict[21:len(json_dict)-1]
            json_dict = json.loads(json_dict)
        if json_dict['cdlist'][0]['songnum'] == i:
            break



class YinYue:

    def __init__(self, url, mid, mmid):
        #guid = int(random() * 2147483647) * int(time() * 1000) % 10000000000
        self.music_url = url  # 音乐的url
        self.music_id = mid  # 音乐的ID
        self.music_mid = mmid
        self.music_download_url = None  # 最终音乐的下载地址
        self.music_name = None
        self.file_name = "C400%s.m4a" % mid
        self.vkey = None  # 加密的参数
        self.params = None  # 提交的参数
        self.music_pic_url = 'http://y.gtimg.cn/music/photo_new/T002R800x800M000{}.jpg?max_age=2592000'.format(self.music_mid)
        self.guid = str('B5B8F37B3F1CDE728CFA1574AC9F5751')
        headers = {
            'authority': 'u.y.qq.com',
            'method':'GET',
            'path': '/cgi-bin/musicu.fcg?callback=getplaysongvkey18973624437935088&g_tk=935211093&jsonpCallback=getplaysongvkey18973624437935088&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%22{}%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22{}%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%222418090286%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A2418090286%2C%22format%22%3A%22json%22%2C%22ct%22%3A20%2C%22cv%22%3A0%7D%7D'.format(self.guid, self.guid, self.music_id),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'RK=v+HSxU5PGX; ptcz=17e3eacf682afd33b90f60d360778ccc68e654bada5bb65f335efc6a492f3ead; pgv_pvi=9761964032; pgv_pvid=2532527580; eas_sid=P1Y581u3a2B3D7E164Y5M8f2o4; tvfe_boss_uuid=c837ea95128d2c3f; ts_uid=3470501600; o_cookie=1521324101; pac_uid=1_1521324101; ptui_loginuin=2418090286; pt2gguin=o2418090286; pgv_info=ssid=s3748524266; pgv_si=s4441048064; qqmusic_fromtag=66; _qpsvr_localtk=0.2075125874706547; uin=o2418090286; skey=@MRFVIIr03; p_uin=o2418090286; pt4_token=08u5pXziyaNWE4jbA9BczIRgdl4gBfJ*Ett8OYHDrr8_; p_skey=1wYixwOM2wk2UiTdjnWrBsqiz*Oo1Ku-WJHwNwnGwO0_; ts_refer=ui.ptlogin2.qq.com/cgi-bin/mibao_vry%3Ftarget%3D2%26jump_login%3D0%26uin%3D2418090286%26pt_mbkey%3Db7d3a9a25933340d60a27c7bde529535f7cfba88f721a; yqq_stat=1; ptmbsig=3953bb3e0261d89210263982c8e62fd449137ecd423c06b590071986dbfebc3e26b065495093383d; player_exist=1; yq_playschange=0; yq_playdata=1; ts_last=y.qq.com/portal/player.html; yplayer_open=1; yq_index=1',
            'dnt':'1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        self.headers = headers

    def get_name(self):  # 获取歌曲的名字
        resp = requests.get(url=self.music_url)
        resp.encoding = 'utf-8'
        html = etree.HTML(resp.text)
        dl_list = html.xpath('/html/body/div[2]/div[1]/div/div[1]/h1')
        for i in dl_list:
                #print(i.xpath('./@href')[0])
            self.music_name = i.text
            print(self.music_name)

        #name = html.xpath('/html/body/div[2]/div[1]/div/div[1]/h1/')

        #doc = pq(response)
        #self.music_name = doc('title').text().split('-')[0]     # 歌曲的名字
        #self.music_name = name

    def get_params(self):   # 获取加密的vkey
        #self.params = self.music_url[self.music_url.rindex(
        #    '/') + 1:self.music_url.rindex('.')]  # 获取音乐的ID
        #print(self.params)
        #params_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=' + \
        #    self.music_id + '&filename=C400' + self.music_id + '.m4a&guid='+ self.guid + '&subcode=0'  # 加密参数的url
        params_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey8128059057776289&g_tk=935211093&jsonpCallback=getplaysongvkey8128059057776289&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%22{}%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22{}%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%222418090286%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A2418090286%2C%22format%22%3A%22json%22%2C%22ct%22%3A20%2C%22cv%22%3A0%7D%7D'.format(self.guid, self.guid, self.music_id)
        #print(params_url)
        response = requests.get(params_url, verify=False, headers=self.headers).text  # 访问加密的网址
        #response = json.loads(response)
        re = response[32:len(response)-1]
        rr = json.loads(re)
        #self.vkey = response['data']['items'][0]['vkey']  # 加密的参数
        #print(rr['req_0']['data']['midurlinfo'][0]['vkey'])
        print('**********')
        print(rr['req_0']['data']['midurlinfo'][0]['vkey'])
        print('**********')
        self.vkey = rr['req_0']['data']['midurlinfo'][0]['vkey']
        if self.vkey == '':
            print('no vkey ')
            with open('no.log', 'a+') as f:
                f.write(self.music_name)
                f.write('\t')
                f.write(self.music_url)
                f.write('\n')


            return True


    def get_quality(self):  # 获取不同品质的url
        #quality_id = input('请输入1-5(默认最高)')
        index_music_url = 'http://dl.stream.qqmusic.qq.com/{}' + self.music_id + \
			'.{}?vkey=' + self.vkey + '&guid=B5B8F37B3F1CDE728CFA1574AC9F5751' + '&uin=0&fromtag=53'
        #url = 'http://dl.stream.qqmusic.qq.com/%s?' % self.file_name
        #index_music_url = url + \
        #    'vkey=%s&guid=%s&fromtag=30' % (self.vkey, self.guid)
        #print(index_music_url)
        music_type = {
            'C400': 'm4a',
            'M500': 'mp3',
            'M800': 'mp3',
			'O600': 'ogg',
            #'M800': 'mpe',
            #'A000': 'ape',
            'F000': 'flac'
        }  # m4a, mp3普通, mp3高, ape, flac
        music_urls = []  # 下载音乐的地址
        for k, v in music_type.items():
            music_url = index_music_url.format(k, v)
            music_urls.append(music_url)
        self.get_url(music_urls)

    def get_url(self, music_urls):  # 用协程判断是否存在不同音乐品质的url
        print(music_urls)
        result = []

        async def get(url):
            session = aiohttp.ClientSession()
            response = await session.get(url)
            status_code = response.status
            # session.close()
            return status_code

        async def request(url):
            response = await get(url)
            if response == 200:
                result.append(url)
        tasks = [asyncio.ensure_future(request(url)) for url in music_urls]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        if len(result):
            result.sort()
            #print(self.music_url)
            print('**********')
            print(result)
            print('**********')
            self.music_download_url = result[-2]    # 默认下载最高品质
            print(self.music_download_url)
            with open('playlist.log', 'a+') as f:
                f.write(self.music_name)
                f.write('\n')
        else:
            with open('log.text', 'a+') as f:
                f.write(self.music_url)
                f.write('\n')
    '''
    def download_music(self):   # 音乐的下载
        if self.music_download_url != None:
            response = requests.get(url=self.music_download_url,stream=True)
            length = int(response.headers.get('Content-Length'))
            print(length)
            a = self.music_name + '.flac'
            print(a)
            if os.path.exists(a) and os.path.getsize(a) == length:
                print('if')
                return True
            else:
                print('else')
                progress = ProgressBar(self.music_name, length)
                with open(self.music_name+'.flac', 'wb') as f:
                    for check in response.iter_content(1024):
                        f.write(check)
                        progress.refresh(len(check))
                return False
    def download_pic(self):
        response = requests.get(url=self.music_pic_url, stream=True)
        length = int(response.headers.get('Content-Length'))
        print(length)
        a = self.music_name + '.jpg'
        print(a)
        if os.path.exists(a) and os.path.getsize(a) == length:
            print('if')
            return True
        else:
            print('else')
            progress = ProgressBar(self.music_name, length)
            with open(self.music_name+'.jpg', 'wb') as f:
                for check in response.iter_content(1024):
                    f.write(check)
                    progress.refresh(len(check))
            return False
    '''
    def download_music(self):
        name = self.music_name + '.mp3'
        a = download_file(name, self.music_download_url)
        if a:
            print('mp3 file already download:', name)

    def download_pic(self):
        name = self.music_name + '.jpg'
        a = download_file(name, self.music_pic_url)
        if a:
            print('pic file already download:', name)

    def download_lrc(self):
        #url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid={}&callback=jsonp1&g_tk=1742329486&jsonpCallback=jsonp1&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(self.music_id)
        url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=753738303&songmid='+ self.music_id
        """
        headers = {
            'authority': 'c.y.qq.com',
            'method': 'GET',
            'path': '/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid={}&callback=jsonp2&g_tk=1742329486&jsonpCallback=jsonp1&loginUin=2418090286&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(self.music_id),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'RK=v+HSxU6PGX; ptcz=17e3eacf682afd33b90f60d360778ccc68e654bada5bb65f335efc6a492f3ead; pgv_pvi=9761964032; pgv_pvid=2532527580; eas_sid=P1Y581u3a2B3D7E164Y5M8f2o4; tvfe_boss_uuid=c837ea95128d2c3f; ts_uid=3470501600; o_cookie=1521324101; pac_uid=1_1521324101; ptui_loginuin=2418090286; pt2gguin=o2418090286; ts_refer=ui.ptlogin2.qq.com/cgi-bin/mibao_vry%3Ftarget%3D2%26jump_login%3D0%26uin%3D2418090286%26pt_mbkey%3Dc2e0a0cc1eb380d288341e615ecc9b49e613d0fc51b36; luin=o2418090286; lskey=00010000a653ba390223e5364977b3a5d1b44559b69850088e52bd8d15270d83190ee844da59c6a7350ba227; pgv_si=s4856638464; pgv_info=ssid=s2049708135; player_exist=1; qqmusic_fromtag=66; yq_index=0; yplayer_open=1; yqq_stat=0; ts_last=y.qq.com/n/yqq/song/{}.html'.format(self.music_id),
            'dnt': '1',
            'referer': 'https://y.qq.com/n/yqq/song/{}.html'.format(self.music_id),
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        """
        headers = {
            "Referer": "https://y.qq.com/portal/player.html",
            "Cookie": "skey=@LVJPZmJUX; p",
        }
        lrc_data = requests.get(url=url, stream=True, headers=headers)
        lrc_dict = json.loads(lrc_data.text[18:-1])
        if 'lyric' in lrc_dict:
            lrc_data = base64.b64decode(lrc_dict['lyric'])
            lrc_name = self.music_name + '.lrc'
            file_path = os.path.join('song', lrc_name)
            if os.path.exists(file_path):
                print('lrc file already download:', lrc_name)
            else:
                with open(file_path, 'ab') as f:
                    f.write(lrc_data)
                    #print(bytes.decode(lrc_data))
                if lrc_dict.get('trans'):
                    lrc_data = base64.b64decode(lrc_dict['trans'])
                    #print(bytes.decode(lrc_data))
                    with open(file_path, 'ab') as f:
                        f.write(lrc_data)
        else:
            print('no lrc')


if __name__ == '__main__':
    mapmid()
    '''
    yinyue = YinYue('https://y.qq.com/n/yqq/song/001a7BRb4W66eQ.html')
    yinyue.get_name()
    yinyue.get_params()
    yinyue.get_quality()
    yinyue.download_music()
    '''
