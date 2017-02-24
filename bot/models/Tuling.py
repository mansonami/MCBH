#coding=utf8

import requests, json

def get_response(msg,**kwargs):

    url = 'http://www.tuling123.com/openapi/api'
    payloads = {
        'key':'09dfa38598e741b4b18552dd1f3f46bc',
        'info': msg,
        'userid': kwargs['FromUserName'][1:32]
    }
    try:
        r = json.loads(requests.post(url, data = payloads).text)
    except:
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000): return
    if r['code'] == 100000: # 文本类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 200000: # 链接类
        return '\n'.join([r['text'].replace('<br>','\n'), r['url']])
    elif r['code'] == 302000: # 新闻类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['article'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 308000: # 菜谱类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['name'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 313000: # 儿歌类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 314000: # 诗词类
        return '\n'.join([r['text'].replace('<br>','\n')])

if __name__ == '__main__':
    ret=get_response('用法')
    pass
