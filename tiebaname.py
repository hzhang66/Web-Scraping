import requests
import json
import re
from lxml import etree
import csv

class TiebaSpider:
    def __init__(self, tieba_name,csv_writer):


        self.tieba_name = tieba_name
        self.start_url = "http://tieba.baidu.com/f?kw=" + tieba_name + "&pn=0"
        self.part_url = "http://tieba.baidu.com"
        self.headers = {
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        self.csv_writer = csv_writer

    def save_content_list(self, content_list):
        file_path = self.tieba_name + ".txt"
        with open(file_path, "a", encoding="utf-8") as f:
            # iterate list and write in individually
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")

    def parse_url(self, url):
        # print(url)
        toggle = False
        curr_pagen = int(re.findall(r'&pn=(\d+)', url)[0])
        # construct the url if the next page
        next_pagen = re.sub(r'&pn=(\d+)', r'&pn={}'.format(curr_pagen + 50), url)
        print(next_pagen.split('pn=')[1])
        if int(next_pagen.split('pn=')[1]) > 450:
            return False,False
        # sent  request
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=self.headers, timeout=20,verify=False)
        html_str = response.content.decode()
        # use re to get all the img_url
        img_url_list = re.findall('bpic *= *"([^"]+)', html_str)

        title_list = re.findall('<a rel=\"noreferrer\" href=(.*?)</a>', html_str)
        content_list = []
        for title in title_list:
            toggle = True
            item = {}
            # extract the content of the title
            title_temp = re.search(">(.*?)<", title + "<")
            titles = list(title_temp.groups())[0]
            # extract the content of href
            href_temp = re.search("\"(.*?)\"", title)

            href = self.part_url + list(href_temp.groups())[0]  #joint
            # Parse detail page data
            result_data = self.parse_detaile_index(href)


            # Add the result data to a list

            for information in result_data:
                if information.get('attention_list')[0] != '该用户没有关注的吧':
                    print(information.get('attention_list'))

                    self.csv_writer.writerow([information.get('attention_list')])


        self.save_content_list(content_list)
        return toggle, next_pagen
    # Detailed page parsing
    def parse_detaile_index(self,url):
        """

        :param url: the detailed page of the keyword list
        :return:  return users' name and url
        """
        # print('URL',url)
        requests.packages.urllib3.disable_warnings()
        response  = requests.get(url,headers=self.headers,verify = False)
        doc = etree.HTML(response.text)
        up =doc.xpath('//*[@id="j_p_postlist"]/div[1]/div[2]/ul/li[1]/div/a/@href')
        url_list = []
        if up:
            up = 'https://tieba.baidu.com' +up[0]
            url_list.append(up)

        final = doc.xpath('//*[@id="j_p_postlist"]/div[last()]/div[2]/ul/li[1]/div/a/@href')
        if final:
            final = 'https://tieba.baidu.com' +final[0]
            url_list.append(final)

        get_back= []
        for up_url in url_list:
            result = self.get_attention(up_url)
            get_back.append(result)
        print('数据上传',get_back)
        return get_back
 
    def get_attention(self,url):
        """

        :param url: detailed information of users' name
        :return: return the user's following bar and the related URL
        """

        response = requests.get(url,headers=self.headers,verify=  False)
        doc = etree.HTML(response.text)
        result = doc.xpath('//*[@id="forum_group_wrap"]/a')
        attention_list= []
        # get the following  bar
        for li in result:
            attention_list.append(''.join(li.xpath('./span[1]/text()')))
        # if no following bar, return NONE
        if not attention_list:
            attention_list = ['该用户没有关注的吧']
        # user's name
        name = ''.join(doc.xpath('//*[@id="userinfo_wrap"]/div[2]/div[2]/span/text()'))

        return {'up_detail_url':url,'attention_list':attention_list,'name':name}


    def run(self):
        toggle, next_url = self.parse_url(self.start_url)
        while toggle:
            # at most 10 pages
            if toggle and next_url:
                toggle, next_url = self.parse_url(next_url)

if __name__ == '__main__':
    name = '测试'
    f = open(f'file/{name}.csv', 'w+', encoding='utf-8-sig', newline='')
    # write in csv file
    headers = ['用户关注的吧'] #'用户关注的吧' means the user's following bar
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)

    tieba_spider = TiebaSpider("荒野乱斗",csv_writer) #"荒野乱斗" is a game called Supercell
    tieba_spider.run()


import csv
import re
tieba=[]
reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
with open('tieba.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tieba=tieba+row
tieba=tieba[1:]

name=[]
for i in tieba:
    item=re.split(r',',i)
    name=name+item
    
tiebaname=[]
for i in name:
    item=re.sub(reg, '', i)
    tiebaname=tiebaname+[item]
    
writerCSV=pd.DataFrame(columns=['tiebaname'],data=tiebaname)
writerCSV.to_csv('./tiebaname.csv',encoding='gbk')
