import requests
import json


# 请求html文本
def getHtmlText(url, code='UTF-8'):
    trytime = 5
    while trytime > 0:
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400',
            }
            r = requests.get(url, headers=header, timeout=5)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            print("get获取失败,重连中")
            trytime -= 1



# 获取微博用户信息
def getUserInfo(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(uid)
    Infomation = json.loads(getHtmlText(url))
    UserInfo = {}
    UserInfo['id'] = Infomation['data']['userInfo']['id']
    UserInfo['name'] = Infomation['data']['userInfo']['screen_name']
    UserInfo['gender'] = '女' if Infomation['data']['userInfo']['gender'] == 'f' else '男'
    UserInfo['statuses_count'] = Infomation['data']['userInfo']['statuses_count']
    UserInfo['desc'] = Infomation['data']['userInfo']['description']
    UserInfo['fans_count'] = Infomation['data']['userInfo']['followers_count']
    UserInfo['follow_count'] = Infomation['data']['userInfo']['follow_count']
    # with open('./UserInfo.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(UserInfo, ensure_ascii=False))
    return UserInfo


# 输出用户基本信息，用于在爬取数据或其他时候方便的输出查看用户信息
def printUserInfo(UserInfo):
    print('id:{}\t微博名:{}\t性别:{}\t发微博数:{}\t粉丝数:{}\t关注数:{}'
          .format(UserInfo['id'],
                    UserInfo['name'],
                    UserInfo['gender'],
                    UserInfo['statuses_count'],
                    UserInfo['fans_count'],
                    UserInfo['follow_count']
                 )
          )