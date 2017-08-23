# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from zhihu_user.items import ZhihuUserItem



class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_user = 'ytian'
    query = 'data[*].answer_count,articles_count,description,gender,follower_count,is_followed,is_following'
    offset = 0
    limit = 20
    start_url = 'https://www.zhihu.com/api/v4/members/{url_token}/followees?include={query}&offset={offset}&limit={limit}'

    item_num = 0        #一共爬取的总数
    followees = []      #xxx用户的关注们。
    #重写方法，提交请求
    def start_requests(self):
        yield Request(self.start_url.format(url_token = self.start_user, query = self.query, offset = self.offset, limit = self.limit))

    # 处理响应对象
    def parse(self, response):


        #返回item
        ##################################################

        # 将json数据转为字典类型
        result = json.loads(response.text)

        #item对象赋值
        for i in xrange(len(result['data'])):
            # 实例化item对象
            item = ZhihuUserItem()
            item['name'] = result['data'][i]['name']
            item['gender'] = '男' if(result['data'][i]['gender'] == 1) else '女'
            item['headline'] = result['data'][i]['headline']
            item['url_token'] = result['data'][i]['url_token']
            item['answer_count'] = result['data'][i]['answer_count']
            item['articles_count'] = result['data'][i]['articles_count']
            item['follower_count'] = result['data'][i]['follower_count']
            item['description'] = result['data'][i]['description']

            # 已爬取的用户总数
            self.item_num += 1
            if self.item_num > 300:
                exit()


            #提示信息
            print '~' * 50
            print '第%d个用户信息' % self.item_num

            #将XXX的关注添加进其列表
            self.followees.append(item['url_token'])

            #返回item供pipeline处理
            yield item


        #构建新请求
        ##################################################
        self.offset += 20
        totals = result['paging']['totals']
        # 如果其关注未爬完，继续
        if self.offset < totals:
            yield Request(self.start_url.format(url_token = self.start_user, query = self.query, offset = self.offset, limit = self.limit))

        # 若爬完，便遍历其关注，作为爬取对象
        else:
            for followee in self.followees:
                yield Request(self.start_url.format(url_token = followee, query = self.query, offset = self.offset, limit = self.limit))

            # 当XXX所有的关注爬取后，置为空
            self.followees = []
