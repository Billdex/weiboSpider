import requests
import json
import matplotlib.pyplot as plt

from spiderUtils import *

def getFansList(uid, num):
    page = 1
    fansNum = 0
    FansList = dict()
    FansList['userInfo'] = getUserInfo(uid)
    print('userInfo:{}\t{}\t{}'.format(FansList['userInfo']['id'], FansList['userInfo']['name'], FansList['userInfo']['gender'],))
    FansList['fans'] = []
    while page:
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&since_id={}'.format(uid, page)
        list = json.loads(getHtmlText(url))
        if list['ok'] == 0 or fansNum >= num:
            return FansList

        for fansitem in list['data']['cards'][-1]['card_group']:
            fansId = fansitem['user']['id']
            FansList['fans'].append(getUserInfo(fansId))
            fansNum += 1
            print('fans{}\tInfo:\t{}\t{}\t{}'.format(fansNum,
                                                     FansList['fans'][-1]['id'],
                                                    FansList['fans'][-1]['name'],
                                                    FansList['fans'][-1]['gender']))
        with open('./fansDataCache.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(FansList, ensure_ascii=False))
        page += 1


if __name__ == '__main__':
    # 是柠檬呀柠檬呀
    # uid = '1972174013'
    # 蔡徐坤
    uid = '1776448504'
    #
    #
    try:
        with open('./fansData.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = getFansList(uid, 25000)
        with open('./fansData.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

    # 男女比例饼状图
    # male_count = 0
    # female_count = 0
    # print(data)
    # for fansInfo in data['fans']:
    #     if fansInfo['gender'] == '男':
    #         male_count += 1
    #     else:
    #         female_count += 1
    #
    # name_list = ['男', '女']
    # num_list = [male_count, female_count]
    # colors = ['lightblue', 'pink']
    # # 圆形
    # plt.figure(1, figsize=(6, 6))
    # # 决定分割部分，及其与其它部分之间的间距
    # expl = [0, 0.1]
    # plt.pie(x=num_list, explode=expl, labels=name_list, autopct='%3.1f %%', colors=colors, shadow=True)
    # plt.rcParams['font.sans-serif'] = ['YouYuan']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.show()

    # 粉丝的个人粉丝情况
    # name_list = ['0-15', '15-50', '50-100', '100-200', '>200']
    # num_list = [0, 0, 0, 0, 0]
    # for fansInfo in data['fans']:
    #     if fansInfo['fans_count'] < 15:
    #         num_list[0] += 1
    #     elif fansInfo['fans_count'] < 50:
    #         num_list[1] += 1
    #     elif fansInfo['fans_count'] < 100:
    #         num_list[2] += 1
    #     elif fansInfo['fans_count'] < 200:
    #         num_list[3] += 1
    #     else:
    #         num_list[4] += 1
    # plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
    # plt.savefig('./粉丝的个人粉丝数.png')
    # plt.show()

    # 粉丝的关注情况
    # name_list = ['0-15', '15-50', '50-100', '100-200', '>200']
    # num_list = [0, 0, 0, 0, 0]
    # for fansInfo in data['fans']:
    #     if fansInfo['follow_count'] < 15:
    #         num_list[0] += 1
    #     elif fansInfo['follow_count'] < 50:
    #         num_list[1] += 1
    #     elif fansInfo['follow_count'] < 100:
    #         num_list[2] += 1
    #     elif fansInfo['follow_count'] < 200:
    #         num_list[3] += 1
    #     else:
    #         num_list[4] += 1
    # plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
    # plt.savefig('./粉丝关注数情况.png')
    # plt.show()

    # 粉丝的发微博的情况
    name_list = ['0-15', '15-40', '40-80', '80-150', '>150']
    num_list = [0, 0, 0, 0, 0]
    for fansInfo in data['fans']:
        if fansInfo['follow_count'] < 15:
            num_list[0] += 1
        elif fansInfo['follow_count'] < 40:
            num_list[1] += 1
        elif fansInfo['follow_count'] < 80:
            num_list[2] += 1
        elif fansInfo['follow_count'] < 150:
            num_list[3] += 1
        else:
            num_list[4] += 1
    plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
    plt.savefig('./粉丝发微博数的情况.png')
    plt.show()

    # 假粉比例
    # fans_fake = 0
    # fans_real = 0
    # print(data)
    # for fansInfo in data['fans']:
    #     if fansInfo['statuses_count'] <= 15 and fansInfo['fans_count'] <= 10:
    #         fans_fake += 1
    #     else:
    #         fans_real += 1
    #
    # name_list = ['假粉丝', '真粉丝']
    # num_list = [fans_fake, fans_real]
    # colors = ['gray', 'red']
    # # 圆形
    # plt.figure(1, figsize=(6, 6))
    # # 决定分割部分，及其与其它部分之间的间距
    # expl = [0, 0.1]
    # plt.pie(x=num_list, explode=expl, labels=name_list, autopct='%3.1f %%', colors=colors, shadow=True)
    # plt.rcParams['font.sans-serif'] = ['YouYuan']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.show()