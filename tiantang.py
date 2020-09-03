"""
@Purpose 爬取天堂网图片
@Author WuYu Chuan
@Date 2020/9/3
"""
import requests
import random
from fake_useragent import UserAgent
from lxml import etree
import time


class Crawler():
    def __init__(self):
        # 初始化url地址
        self.url = 'https://www.ivsky.com/bizhi/1920x1200//index_{}.html'
        # 随机获得header
        ua = UserAgent(verify_ssl=False)
        for i in range(1,50):
            self.headers = {
                'User-Agent':ua.random
            }

    def get_oneLevel(self,url):
        oneResponse = requests.get(url=url,headers=self.headers).content.decode('utf-8')
        html = etree.HTML(oneResponse)
        oneNodes = html.xpath('//ul[@class="ali"]//li/div//a//@href')
        for node in oneNodes:
            twoUrl = "https://www.ivsky.com"+node
            self.get_twoLevel(twoUrl)

    def get_twoLevel(self,twoUrl):
        twoResponse = requests.get(url=twoUrl,headers=self.headers).content.decode('utf-8')
        html = etree.HTML(twoResponse)
        nodes = html.xpath('//ul[@class="pli"]//li/div//a//@href')
        for node in nodes:
            threeUrl = "https://www.ivsky.com" + node
            self.get_threeLevel(threeUrl)

    def get_threeLevel(self,threeUrl):
        threeResponse = requests.get(url=threeUrl,headers=self.headers).content.decode('utf-8')
        html = etree.HTML(threeResponse)
        urlNodes = html.xpath('//img[@id="imgis"]/@src')
        nameNodes = html.xpath('//img[@id="imgis"]/@alt')
        for name in nameNodes:
            pass
        for img in urlNodes:
            imgUrl = "https:/"+img[1:]
            photoResponse = requests.get(url=imgUrl,headers=self.headers).content
            filename = "E:\\photo\\" + name[:-5]+img[-6:]
            with open(filename, 'wb') as f:
                f.write(photoResponse)
                print("%s下载成功" % filename)

    def main(self):
        for i in range(1,4):
            url = self.url.format(i)
            self.get_oneLevel(url)
            time.sleep(random.randint(1,3))
            print("第%d提取成功！！！" % i)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.main()

