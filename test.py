import requests
import json
vipcode='333333' #vip卡号
r=requests.get(url='http://127.0.0.1:5000/api/HfoMgEeRKSPUWuIiN0qvApj9nJ/vip/query_Counters/%s'%vipcode)
ret=json.loads(r.text)
print('  '.join(ret['zgname']))


