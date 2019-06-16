import time
import random
import matplotlib.pyplot as plt

from spiderUtils import *

# 获取某条微博转发用户的信息
def getRelayUsers(mid, num):
    Users = []
    for page in range(1, 25000):
        url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.format(mid, page)
        data = json.loads(getHtmlText(url))
        if data['ok'] == 0 or num <= 0:
            return Users
        for relayUser in data['data']['data']:
            UserInfo = dict()
            # 因为在这个页面已经提供了用户的详细信息，就不再通过另一个api来获取用户信息
            UserInfo['id'] = relayUser['user']['id']
            UserInfo['name'] = relayUser['user']['screen_name']
            UserInfo['gender'] = '女' if relayUser['user']['gender'] == 'f' else '男'
            UserInfo['statuses_count'] = relayUser['user']['statuses_count']
            UserInfo['desc'] = relayUser['user']['description']
            UserInfo['fans_count'] = relayUser['user']['followers_count']
            UserInfo['follow_count'] = relayUser['user']['follow_count']
            printUserInfo(UserInfo)
            Users.append(UserInfo)
            num -= 1

        # 别爬太快，会封ip
        time.sleep(random.uniform(0.5, 1))
        with open('./relayUsersData_cache.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(Users, ensure_ascii=False))
    return Users




if __name__ == '__main__':
    # 蔡徐坤2019.5.7某条微博
    mid = '4369316738673069'



    try:
        with open('./relayUsersData.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = getRelayUsers(mid, 10000)
        print(data)
        with open('./relayUsersData.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

    # 假粉转发比例
    fans_fake = 0
    fans_real = 0
    for fansInfo in data:
        if fansInfo['statuses_count'] <= 15 and fansInfo['fans_count'] <= 10:
            fans_fake += 1
        else:
            fans_real += 1

    name_list = ['假转发流量', '真转发流量']
    num_list = [fans_fake, fans_real]
    colors = ['gray', 'red']
    # 圆形
    plt.figure(1, figsize=(6, 6))
    # 决定分割部分，及其与其它部分之间的间距
    expl = [0, 0.1]
    plt.pie(x=num_list, explode=expl, labels=name_list, autopct='%3.1f %%', colors=colors, shadow=True)
    plt.rcParams['font.sans-serif'] = ['YouYuan']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()