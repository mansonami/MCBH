from flask import jsonify
from flask_login import login_required
from . import api
import random
import string

from ..models import Wxsetting
from bot.models.wumis import Vip_query_Counters

@api.route('/createtoken',methods=['post'])
@login_required
def createtoken():
    token = ''.join([(string.ascii_letters + string.digits)[x] for x in random.sample(range(0, 62), 26)])
    que=Wxsetting().get()
    que.Apitoken=token
    que.save()
    return jsonify({
        'text':token
    })

@api.route('/<string:token>/vip/query_Counters/<string:code>')
def get_xml(token,code):
    if len(code)!=6:
        return jsonify({
            'Error': 'invalid Vip code'
        })
    if not Wxsetting().GetApitoken()['Apitoken']==token:
        return jsonify({
            'Error': 'invalid token'
        })
    return jsonify({
        'zgname':Vip_query_Counters(code)
    })




