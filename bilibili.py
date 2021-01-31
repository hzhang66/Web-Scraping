# query the famouse bilibili video website uploader's fans' following list to find the fans' interest distribution

import requests
import re
import json
import time


def query_followings(up_id):
    """
    parameter up_id: uper's id
    return: following list
    """
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Referer': "https://space.bilibili.com/%s/#/fans/follow" % up_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }

    followings_list = list()

    for page in range(1, 6):
        params = {
            "vmid": str(up_id),
            "pn": str(page),
            "ps": "20",
            "order": "desc",
            "jsonp": "jsonp",
            "callback": "__jp5",
        }

        response = requests.get(
            'https://api.bilibili.com/x/relation/followings', params=params, headers=headers)

        followings = ''.join(re.findall(r'__jp\d+\((.*)\)', response.text))
        jfollowings = json.loads(followings)

        if not jfollowings['data']['list']:
            break

        for following in jfollowings['data']['list']:
            following_short = following.get('mid')
            #{
            #    'mid': following.get('mid'),
            #    'uname': following.get('uname'),
            #    'sign': following.get('sign')
            #}
            followings_list.append(following_short)
        time.sleep(5)

    return followings_list


def query_fans(up_id):
    """
    parameter up_id: uper's ID
    return: fans' list
    """
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://space.bilibili.com/%s/fans/fans" % up_id,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    }

    fans_list = list()

    for page in range(1, 6):  # at most 5 pages
        params = {
            "vmid": str(up_id),
            "pn": str(page),
            "ps": "20",
            "order": "desc",
            "jsonp": "jsonp",
            "callback": "__jp10",
        }

        response = requests.get(
            'https://api.bilibili.com/x/relation/followers', params=params, headers=headers)

        fans = ''.join(re.findall(r'__jp\d+\((.*)\)', response.text))
        jfans = json.loads(fans)

        if not jfans['data']['list']:
            break

        for fan in jfans['data']['list']:
            fan_short = {
                'mid': fan.get('mid'),
                'uname': fan.get('uname'),
                'sign': fan.get('sign')
            }
            fans_list.append(fan_short)
        time.sleep(5)

    return fans_list


if __name__ == '__main__':
    
    fans_list = query_fans(474647832)    # query fans' list at firs
    following_list1=[]
    for fan in fans_list:
        following_list1.append(query_followings(fan['mid']))    # then query  every fan's following list
        #print(following_list1)
        
        time.sleep(5)


following_list0=following_list1[:]

following_list0=sum(following_list0,[])



dict_x = {}
for item in list:
    dict_x[item] = list.count(item)


dict= sorted(dict_x.items(), key=lambda d:d[1], reverse = True)[0:10]

#run

if __name__ == '__main__':
    
    fans_list = query_fans(uploader[1])
    following_list1=[]
    for fan in fans_list:
        following_list1=following_list1+query_followings(fan['mid'])
        
        time.sleep(5)



if __name__ == '__main__':
    
    
    fans_list = query_fans(uploader[2])
    following_list2=[]
    for fan in fans_list:
        following_list2=following_list2+query_followings(fan['mid'])

        time.sleep(5)



if __name__ == '__main__':
    
    
    fans_list = query_fans(uploader[3])
    following_list3=[]
    for fan in fans_list:
        following_list3=following_list3+query_followings(fan['mid'])
        
        time.sleep(5)



if __name__ == '__main__':
    
    
    fans_list = query_fans(uploader[4])
    following_list4=[]
    for fan in fans_list:
        following_list4=following_list4+query_followings(fan['mid'])
        
        time.sleep(5)



if __name__ == '__main__':
    
    
    fans_list = query_fans(uploader[5])
    following_list5=[]
    for fan in fans_list:
        following_list5=following_list5+query_followings(fan['mid'])
        
        time.sleep(5)

if __name__ == '__main__':
    
    
    fans_list = query_fans(uploader[6])
    following_list6=[]
    for fan in fans_list:
        following_list6=following_list6+query_followings(fan['mid'])
        
        time.sleep(5)

following_list=following_list0+following_list1+following_list2+following_list3+following_list4+following_list5+following_list6



dict_x = {}
for item in following_list:
    dict_x[item] = following_list.count(item)
dict= sorted(dict_x.items(), key=lambda d:d[1], reverse = True)





uploader=[474647832,429714179,86189745,412442395,12990499,355969965,403854231]
dict[0:70]





import pandas as pd


writerCSV=pd.DataFrame(columns=['id','frequency'],data=dict)
writerCSV.to_csv('./bilibili.csv',encoding='utf-8')

