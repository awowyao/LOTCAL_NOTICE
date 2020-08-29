# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LotcalNoticePipeline:
    def process_item(self, item, spider):
        print(item)
        return item


import pymysql
from .settings import *
class process_mysql_oage:
    def open_spider(self,spider):
        self.db = pymysql.connect(MySQL_HOME,MySQL_USER,MySQL_PWD,MySQL_DATABASE,charset='utf8')
        self.cursor = self.db.cursor()
        self.total = 0
    def process_item(self, item, spider):
        L = []
        for p in item['list']:
            # 获取键keys()、值values()、键值items()
            for k, i in p.items():
                if k == '采购项目名称':
                    L.append(i)
                if k == '品目':
                    L.append(i)
                if k == '公告时间':
                    L.append(i)
        self.cursor.execute("insert into test values (%s,%s,%s)",L)
        self.db.commit()
        self.total +=1
        print('已完成%d条数据' % self.total)
        return item
    def close_spider(self,spider):
        print('一共有%d条数据'% self.total)
        self.db.close()
        self.cursor.close()



class process_txt_oage:
    def open_spider(self,spider):
        self.f = open('abc.txt','w')
        print('这是open')
        self.total = 0
    def process_item(self, item, spider):
        L = []
        for p in item['list']:
            # 获取键keys()、值values()、键值items()
            for k, i in p.items():
                P1 = str(k) + ':' + str(i)
                L.append(P1)
        sj = '\n'.join(L)
        self.f.write(sj+'\n')
        self.total += 1
        print('已完成%d条数据' % self.total)
        return item
    def close_spider(self,spider):
        print('一共有%d条数据' % self.total)
        self.f.close()
        print('这是clcose')