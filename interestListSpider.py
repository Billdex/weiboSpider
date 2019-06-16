import requests
import re
import json
import networkx as nx
import matplotlib.pyplot as plt

from spiderUtils import *


# 获取用户关注列表
def getInterestList(uid, num):
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&page=1'.format(uid)
    data = json.loads(getHtmlText(url))
    intertestList = []
    cardlist = data['data']['cards']
    for cards in cardlist:
        if 'title' in cards and (cards['title'] == '她的全部关注' or '他的全部关注'):
            i = 0
            for card in cards['card_group']:
                if i < num:
                    person = {}
                    person['id'] = card['user']['id']
                    intertestList.append(person)
                    i += 1
    # with open('./interestList.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(intertestList, ensure_ascii=False))
    return intertestList


# 深搜获取多层用户信息及用户关注列表
def deepSearchList(list, uid, floor, num):
    if floor == 0:
        # print(list.keys())
        if uid in list.keys():
            print('{}有重复'.format(uid))
            return list
        else:
            # print(list.keys())
            # print(uid in list.keys())
            list[str(uid)] = dict()
            list[uid]['userInfo'] = getUserInfo(uid)
            print('{}\t{}\t{}\t{}'.format(uid, list[uid]['userInfo']['name'], list[uid]['userInfo']['gender'],
                                          list[uid]['userInfo']['desc']))
            return list
    elif uid in list.keys() and 'interestList' in list[uid].keys():
        # print('interestList' in list[uid].keys())
        print('{}有重复'.format(uid))
        return list
    else:
        list[str(uid)] = dict()
        list[uid]['userInfo'] = getUserInfo(uid)
        list[uid]['interestList'] = getInterestList(uid, num)
        print('{}\t{}\t{}\t{}'.format(uid, list[uid]['userInfo']['name'],
                                      list[uid]['userInfo']['gender'],
                                      list[uid]['userInfo']['desc']))
        i = 0
        for interestList in list[uid]['interestList']:
            if i < num:
                list = deepSearchList(list, str(interestList['id']), floor - 1, num)
                # with open('./list.json', 'w', encoding='utf-8') as f:
                #     f.write(json.dumps(list, ensure_ascii=False))
                i += 1
        return list


# 画出关注人的人物关系图
def drawRelationGraph(dataList):
    G = nx.DiGraph()
    node_size_list = dict()
    node_color_list = dict()
    for person in dataList:
        G.add_node(dataList[person]['userInfo']['name'])
        node_size_list[dataList[person]['userInfo']['name']] = 0
        node_color_list[dataList[person]['userInfo']['name']] = 'lightblue' if dataList[person]['userInfo'][
                                                                               'gender'] == '男' else 'pink'
    for person in dataList:
        if 'interestList' in dataList[person].keys():
            for interest in dataList[person]['interestList']:
                print('{} -> {}'.format(person, interest['id']))
                G.add_edge(dataList[person]['userInfo']['name'],
                           dataList[str(interest['id'])]['userInfo']['name'])
                node_size_list[dataList[str(interest['id'])]['userInfo']['name']] += 1
    nx.draw(G,
            pos=nx.spring_layout(G),
            with_labels=True,
            node_size=[i * i * 200 + 100 for i in list(node_size_list.values())],
            node_color=[i for i in list(node_color_list.values())],
            width=0.2,
            font_size=8)
    plt.rcParams['font.sans-serif'] = ['YouYuan']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()




if __name__ == '__main__':
    # 头顶戴朵花
    # uid = '1913880370'
    # sven_shi
    # uid = '2382064902'
    # 史前怪物嗷呜
    # uid = '5565609898'
    # 张家界事儿
    # uid = '6000209884'
    # 是柠檬呀柠檬呀
    uid = '1972174013'

    try:
        with open('./interestList.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = dict()
    data = deepSearchList(data, uid, 3, 5)
    with open('./interestList.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
    print(data)
    print(len(data))
    drawRelationGraph(data)

