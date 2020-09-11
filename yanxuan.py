"""
@Purpose：爬取网易严选文胸评价数据
@Author：WuYu Chuan
@Date:2020/9/11
"""

import requests
import json

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

#想获得评论数据，首先获取产品id
def getItemId():
    # 定义请求参数 page:第几页  size:每页展示多少个产品ID  keyword:搜索关键字
    params_id = {
        'page':1,
        'size':40,
        'keyword':'文胸'
    }
    # 通过开发者工具抓包可以确定 产品id由此链接返回  定义访问地址
    url_id = 'https://you.163.com/xhr/search/search.json'

    # get请求获得json数据，并将json数据转换成python数据类型
    response = requests.get(url=url_id,headers=headers,params=params_id)
    itemIds = json.loads(response.content.decode('utf-8'))
    dateIds = itemIds['data']['directly']['searcherResult']['result']
    listIds = []
    # 获得产品id并将其返回
    for ids in dateIds:
        id = ids['id']
        listIds.append(id)
    return listIds

# 拿到产品id后，通过产品id获取评论数据
def getCommentData(itemId):
    listCom = []
    # 通过开发者工具抓包 可以确定评论数据由此链接返回
    url_pl = 'https://you.163.com/xhr/comment/listByItemByTag.json'
    # 定义请求参数 size:每页多少条评论  page:第几页  itemId:产品id
    for i in range(1,3):
        params_pl = {
            'size':20,
            'page':i,
            'itemId':itemId
        }
        # get请求返回json数据，并将结果转换成python数据类型
        response_pl = requests.get(url=url_pl,headers=headers,params=params_pl)
        commentData = json.loads(response_pl.content.decode('utf-8'))
        commentList = commentData['data']['commentList']
        for comments in commentList:
            info = {
                'size':comments['skuInfo'][0],
                'color':comments['skuInfo'][1],
                'comment':comments['content']
            }
            listCom.append(info)
        print('产品ID:%d,第%d页评价爬取成功！' %(itemid,i))

    return listCom

# 调用方法，并将结果写入本地文件
itemIds = getItemId()
for itemid in itemIds:
    result = getCommentData(itemid)
    for res in result:
        f = open('./comment.txt','a+',encoding='utf-8')
        f.write(res['size']+',')
        f.write(res['color']+',')
        f.write("评价:"+res['comment']+'\n')
        f.close()






