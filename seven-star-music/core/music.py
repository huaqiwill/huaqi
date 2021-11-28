"""
@ File-Name: music.py
@ Author: Cunfu Peng
@ Create-Date: 2021/11/08
@ Last-Update: 2021/11/24
@ Version: 1.2
"""

import requests, json, csv
from bs4 import BeautifulSoup


class Utils:
    def durationToString(duration: int):
        """
        将整数的duration转换为字符串，以（分：秒）的形式返回
        """
        duration = int(duration / 1000)
        sec = duration % 60
        min = int((duration - sec) / 60)
        sec = "00" + str(sec)
        min = "00" + str(min)
        sec = sec[sec.__len__() - 2 :]
        min = min[min.__len__() - 2 :]
        return min + ":" + sec


"""
Recommond类
SongInfo类
Utils类
"""

"""
@ Class-Name: KuGou
@ Author: Cunfu Peng
@ Date: 2021/11/08
@ Last-Edit-Time: 2021/11
@ Version: 1.2
"""



class KuGou:
    pass




"""
@ Class-Name: QQ
@ Author: Cunfu Peng
@ Date: 2021/11/08
@ Last-Edit-Time: 2021/11
@ Version: 1.2
"""


class QQ:
    pass


"""
@ Class-Name: KuWo
@ Author: Cunfu Peng
@ Date: 2021/11/08
@ Last-Edit-Time: 2021/11
@ Version: 1.2
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

class KuWo:
    def get_recommond():
        url = "http://www.kuwo.cn/rankList"
        global headers
        requests.get(url,headers=headers)

    def get_songlist():
        pass
    
    def single_search():
        pass
    
    def get_childlist():
        pass





"""
@ Class-Name: Netease
@ Author: Cunfu Peng
@ Date: 2021/11/08
@ Last-Edit-Time: 2021/11
@ Version: 1.2
"""
"""
编码

from urllib.parse import quote
text = quote(text, 'utf-8')

解码

from urllib.parse import unquote
text = unquote(text, 'utf-8')
"""

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/95.0.4638.69 Safari/537.36",
}

class Netease:
    """
    net_recommond_dic = {
    "飙升榜": "https://music.163.com/discover/toplist?id=19723756",
    "新歌榜": "https://music.163.com/discover/toplist?id=3779629",
    "原创榜": "https://music.163.com/discover/toplist?id=2884035",
    "热歌榜": "https://music.163.com/discover/toplist?id=3778678"
    }
    """

    def get_recommoned(
        url: str = "https://music.163.com/discover/toplist?id=3778678",
    ) -> list:
        # url = "https://music.163.com/discover/toplist?id=3778678"
        global headers
        html = requests.get(url, headers=headers).content
        # tree = etree.HTML(rst).xpath("@id=song-list-pre-cache/textarea/text()")
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8").find(
            attrs={"id": "song-list-pre-data"}
        )
        return json.loads(soup.get_text())

        """
        rst_songlist = net_music().get_recommoned()
        duration = rst_songlist[0]["duration"]
        name =  rst_songlist[0]["name"]
        id = rst_songlist[0]["id"]

        albumn =  rst_songlist[0]["album"]
        albumn_picurl = albumn["picUrl"]
        albumn_id = albumn["id"]
        albumn_name = albumn["name"]

        artists =  rst_songlist[0]["artists"]
        artists_id = artists[0]["id"]
        artists_name = artists[0]["id"]
        """

    # 获取歌单
    def get_songlist(cat: str = "全部", page: int = 1):
        """
        cat = [
            "全部",
            {"语种":["日语","韩语","欧美","粤语"]},
            {"风格":["流行","摇滚","民谣","民族","电子","爵士","乡村","古典","古风"]},
            {"场景":["清晨","夜晚","学习","工作","旅行","散步","酒吧"]},
            {"情感":["怀旧","清新","浪漫","治愈","伤感","思念"]},
            {"主题":["KTV","影视原声","校园","经典","翻唱","游戏"]}
        ]
        """

        url = "https://music.163.com/discover/playlist"
        page *= 35
        params = {"order": "hot", "cat": cat, "limit": "35", "offset": str(page)}

        global headers
        html = requests.get(url, headers=headers, params=params).content

        # 方法一，解析了再返回  测试使用
        # soups = BeautifulSoup(html,"html.parser",from_encoding="utf-8").find(attrs={"id":"m-pl-container"}).find_all("li")
        # print(soups.__len__())
        # for soup in soups:
        #     img = soup.find("img")
        #     img = img.get("src")
        #     name = soup.find("a")
        #     href = name.get("href")
        #     title = name.get("title")
        #     print(title)

        # 方法二：在外部使用正则解析 优点：速度更快
        soups = (
            BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            .find(attrs={"id": "m-pl-container"})
            .find_all("li")
        )

        return soups

    # 单曲搜索
    def single_search(name: str, song_num: int = 100) -> list:
        url = (
            'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={"'
            + name
            + '"}'
            "&type=1&offset=0&total=true&limit=" + str(song_num)
        )

        data = requests.get(url, headers=headers).json()["result"]["songs"]

        """
        id = data[0]["id"]
        name = data[0]["name"]
        alias = data[0]["alias"]
        duration = data[0]["duration"]

        artists = data[0]["artists"]
        artists_id = artists[0]["id"]
        artists_name = artists[0]["name"]

        album = data[0]["album"]
        album_id = album["id"]
        album_picId = album["picId"]
        album_name = album["name"]
        """

        return data

    # 获取歌单中的歌曲信息
    def get_childlist(url: str):
        # url = "https://music.163.com/playlist?id=6733647208"
        global headers
        html = requests.get(url=url, headers=headers).content
        soups = (
            BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            .find(attrs={"class": "f-hide"})
            .find_all("a")
        )

        # for soup in soups:
        #     href = soup.get("href")
        #     title = soup.get_text()

        return soups

    # 获取音乐歌词
    def get_musicLrc_byId(song_id: str):
        br = "96000"
        # 通过urls获取歌词
        url = "http://music.163.com/api/song/media?id={0}".format(song_id)
        rst = requests.get(url).json()["lyric"]
        return rst

    # 获取音乐地址
    def get_musicUrl_byId(song_id: str):
        url = "http://music.163.com/song/media/outer/url?id={0}.mp3".format(song_id)
        return url

    # 通过音乐url获取音乐资源并写到文件
    def get_musicSource_byUrl(song_url: str, file_name: str) -> bool:
        """
        此处详细注释：
        1. 音乐通过GET外链，返回状态码为302
        2. 从Response Headers中获取Location的值才是真正的音乐地址
        3. GET新的链接

        为什么Python可以通过修改Headers就直接爬取到资源？
            因为其内部对其使用了重定向。
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        rst = requests.get(song_url, headers=headers).content
        # print(rst["Location"])
        with open(file_name, mode="wb") as f:
            f.write(rst)
        return True

    def get_album_picUrl_byPicId(pic_id: str):
        # 暂未实现该方法

        return pic_id


