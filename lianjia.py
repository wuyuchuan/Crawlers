"""
@Purpose:抓取链家网信息
@Author:Wuyu Chuan
@Date:2020/9/2
"""
import requests
from lxml import etree
import openpyxl
from fake_useragent import UserAgent
import random

# 创建了一个空列表
list_data = []

ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent':ua.random
}

def crawler(url):
    response = requests.get(url=url,headers=headers).content.decode('utf-8')
    html = etree.HTML(response)

    # 获取楼盘名称
    lp_name = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-name"]/a/text()')
    # 获取楼盘类型 住宅/别墅/写字楼
    lp_type = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-name"]/span[@class="resblock-type"]/text()')
    # 获取楼盘状态 在售/售罄
    lp_status = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-name"]/span[@class="sale-status"]/text()')
    # 获取楼盘所在区域
    lp_quyu = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-location"]/span[1]/text()')
    # 获取楼盘所在片区
    lp_pianqu = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-location"]/span[2]/text()')
    # 获取楼盘详细地址
    lp_address = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-location"]/a/text()')
    # 获取楼盘 建筑面积
    lp_area = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-area"]/span/text()')
    # 获取楼盘总价（不太准确）
    lp_price = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-price"]/div[2]/text()')
    # 获取楼盘单价 （元/平方米）
    lp_unit = html.xpath('//ul[@class="resblock-list-wrapper"]/li//div[@class="resblock-price"]/div[@class="main-price"]/span[1]/text()')

    # 将上述获得的数据对应的元素放在一起
    for name,type,status,quyu,pianqu,address,area,price,unit in zip(lp_name,lp_type,lp_status,lp_quyu,lp_pianqu,lp_address,lp_area,lp_price,lp_unit):
        info = [name,type,status,quyu,pianqu,address,area,price,unit]
        list_data.append(info)

# 产生48页的URL
urls = ['https://jn.fang.lianjia.com/loupan/pg{}/'.format(i) for i in range(1,49)]

# 迭代
for url in urls:
    crawler(url)

# 写入excle文件
wb = openpyxl.Workbook()
ws = wb.active
ws.title = '济南楼盘'

for i in list_data:
    ws.append(i)

wb.save('济南楼盘.xlsx')