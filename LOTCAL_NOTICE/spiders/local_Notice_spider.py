import scrapy
from lxml import etree
from ..items import LotcalNoticeItem
import requests
import pymysql
class LocalNoticeSpiderSpider(scrapy.Spider):
    list = LotcalNoticeItem()
    name = 'local_Notice_spider'
    allowed_domains = ['ccgp.gov.cn']
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=2&buyerName=&projectId=&pinMu=0&bidType=&dbselect=bidx&kw=&start_time=2020%3A08%3A28&end_time=2020%3A08%3A28&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
    # url_word = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=2&buyerName=&projectId=&pinMu=0&bidType=&dbselect=bidx&kw=&start_time=2020%3A{}%3A{}&end_time=2020%3A{}%3A{}&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
    # start_y = str(input('请输入开始查询月份：'))
    # start_r = str(input('请输入开始的日期：'))
    # end_y = str(input('请输入结束查询月份：'))
    # end_r = str(input('请输入结束的日期：'))
    # start_time = int(input('请输入开始查询时间（只需要输入时）：'))
    # end_time = int(input('请输入结束查询时间（只需要输入时）：'))
    # url = url_word.format(start_y,start_r,end_y,end_r)
    # db = pymysql.connect('127.0.0.1','root','123456','gonGao',charset='utf8')
    # cursor = db.cursor()
    def start_requests(self):
        page = self.get_page()
        pa = 0
        #计算全部有多少页
        if int(page) % 20 != 0:
            pa += 1
        for x in range(1,int(page)+1):
            if x % 20 ==0:
                pa +=1
        for i in range(1,pa+1):
            url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&bidSort=2&buyerName=&projectId=&pinMu=0&bidType=&dbselect=bidx&kw=&start_time=2020%3A08%3A28&end_time=2020%3A08%3A28&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
            #拼链接
            url_ = url.format(i)
            # 传入全部链接
            yield scrapy.Request(
                url=url_,
                callback=self.parse
            )
    # start_urls = ['http://search.ccgp.gov.cn/']
    def parse(self, response):
        html = response.text
        one_xp = '//ul[@class = "vT-srch-result-list-bid"]/li/a/@href'
        name_xp = '//ul[@class = "vT-srch-result-list-bid"]/li/a/text()'
        time_name_ = '//ul[@class = "vT-srch-result-list-bid"]/li/span/text()'
        html_xp = etree.HTML(html)
        # 获取详细公告链接
        one_url = html_xp.xpath(one_xp)
        # 获取公告全部名称
        name = html_xp.xpath(name_xp)
        # 获取一级公告时间、采集人、单位
        time_name = html_xp.xpath(time_name_)
        i = 0
        for p in time_name:
            #将数据分开
            time_name_mechan = p.split('|')
            #找到有效数据
            if len(time_name_mechan) ==3:
                # 获取每个公告名称
                Name = name[i].strip()
                # i += 1
                # 获取每个公告时间
                time = time_name_mechan[0].strip()
                # 获取每个公告采购人
                purchase = time_name_mechan[1].strip()
                # 获取每个公告单位
                mechan = time_name_mechan[2].strip()
                purchase.split('：')
                # L = {'name':Name,'time':time,purchase.split('：')[0]:purchase.split('：')[1],'mechan':mechan}
                # self.list['one_list'] = L
                #匹配公告时间
                if int(time[11:13])>=16 and int(time[11:13])<18:
                    #遍历详细公告链接
                    # for p in one_url:
                    p = one_url[i]
                    # my = self.cursor.execute("select * from gonGaourl WHERE url = %s",[p])
                    # if my:
                    #     print('爬取过了')
                    #     continue
                    # else:
                    #     self.cursor.execute("insert into gonGaourl values (%s)", [p])
                    #     self.db.commit()
                    L = {'name': Name, 'time': time, purchase.split('：')[0]: purchase.split('：')[1],
                         'mechan': mechan}

                    yield scrapy.Request(
                        url=p,
                        callback=self.two_parse,
                        meta={'L':L},
                        encoding='UTF-8'
                    )

                    # self.db.close()
                    # self.cursor.close()
                else:
                    pass
                i += 1
    def two_parse(self,response):
        l1 = []
        html = response.text
        html_xp = etree.HTML(html)
        #循环所以需要的数据的节点
        for i in range(2,100):
            pa = html_xp.xpath('//tr['+str(i)+']/td/b/text()')
            prge = pa[0] if pa else '456'
            #找到中止循环节点
            if str(prge.strip()) == '联系人及联系方式：':
                #中止循环
                break
            else:
                #如果存在第3个节点那就需要爬取4个节点
                if html_xp.xpath('//div[@class = "table"]//tr[' + str(i) + ']/td[3]/text()'):
                    name = html_xp.xpath('//div[@class = "table"]//tr[' + str(i) + ']/td[1]/text()')
                    text = html_xp.xpath('//div[@class = "table"]//tr[' + str(i) + ']/td[2]/text()')
                    time_name = html_xp.xpath('//div[@class = "table"]//tr[' + str(i) + ']/td[3]/text()')
                    time = html_xp.xpath('//div[@class = "table"]//tr[' + str(i) + ']/td[4]/text()')
                    # 获取详细公告内容名称
                    name = name[0] if name else None
                    # 获取详细公告信息
                    text = text[0] if text else None
                    #时间名称
                    time_name = time_name[0] if time_name else None
                    #获取时间
                    time = time[0] if time else None
                    L = {name:text}
                    L1 ={time_name:time}
                    l1.append(L)
                    l1.append(L1)
                else:
                    name = html_xp.xpath('//div[@class = "table"]//tr['+ str(i) +']/td[1]/text()')
                    text = html_xp.xpath('//div[@class = "table"]//tr['+ str(i) +']/td[2]/text()')
                    # 获取详细公告内容名称
                    name = name[0] if name else None
                    # 获取详细公告信息
                    text = text[0] if text else None
                    # name2 = name[0] if name else None
                    L2 = {name:text}
                    l1.append(L2)
        # print(1)
        self.list['one_list'] = response.meta['L']
        self.list['list'] = l1
        yield self.list

    def get_page(self):
        url = self.url
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        html = requests.get(url=url, headers=headers)
        html.encoding ='UTF-8'
        html = html.text
        html = etree.HTML(html)
        #获取全部数据的数量
        page = html.xpath('/html/body/div[5]/div[1]/div/p[1]/span[2]/text()')
        return page[0]