import pyodbc


WUDEBIT = "DSN=wudebit;UID=sa;pwd=wuitghxx"
def Select_vip_code(phone):
    try:
        conn = pyodbc.connect(WUDEBIT,autocommit=True)
        cursor = conn.cursor()
        card_str=''
        for row in cursor.execute("select vip_card from guest WHERE mobile ='%s' or wokephone='%s' or homephone='%s'"%(phone,phone,phone)):#循环查询 卡号是否被禁用
            #print(row[0])
            count =cursor.execute("select state from vip_client WHERE code='%s'"% row[0]).fetchone()[0]
            #print(count)
            if count=='ı²│ú':#vip卡正常,执行查询积分
                ret=Select_vip_integral(row[0],conn)
                if ret:
                    card_str = card_str + ret
                else:
                    card_str = card_str + '卡号:%s  积分:0.00'%row[0]
            if card_str!='':
                return card_str
        return '没有查询到该电话号码'
    finally:
        cursor.close()
        conn.close()

#¢¹Ë├禁用  ı²│ú正常

def Select_vip_integral(code,conn=None):
    #global conn
    conn_state=conn
    if conn_state!=None:
        cursor = conn.cursor()
    else:
        conn = pyodbc.connect(WUDEBIT, autocommit=True)
        cursor = conn.cursor()
    # ==
    try:
        count = cursor.execute('''
          SELECT ACCOUNT_integral.CARD_ID,
			GUEST.ID,
			GUEST.NAME,
			GUEST.BIRTHDAY,
			GUEST.MANAGER,
			GUEST.MOBILE,
			GUEST.EMAIL,
			GUEST.CLIENT_TYPE,
         GUEST.HOMEPHONE,
			GUEST.POSTCODE,
			GUEST.ADDRESS,
			SUM(case when (ACCOUNT_integral.billid = "自动积分" or ACCOUNT_integral.resume = "消费积分") Then ACCOUNT_integral.SUM_PRICE * ACCOUNT_integral.STATE else 0 end) AS SUM_PRICE,
			SUM(ACCOUNT_integral.INTEGRAL * ACCOUNT_integral.STATE) AS INTEGRAL,
			sum(case when account_integral.state = 1 then account_integral.integral else 0 end) as zjjf,
			SUM(case when ACCOUNT_integral.state = -1 Then ACCOUNT_integral.integral else 0 end) as fljf,
			count(distinct convert(char(10),busdate,102) + isnull(receipt,"")) as jfcs,
         GUEST.BIRTHDAY,
         SUM(case when ACCOUNT_integral.state = -1 Then ACCOUNT_integral.SUM_PRICE else 0 end) AS return_PRICE,
			vip_client.startdate,
			vip_client.stopdate,
			isnull(mag_card.card_face,vip_client.code) as card_face
    FROM ACCOUNT_integral,GUEST,vip_client,mag_card
	WHERE ( account_integral.card_id = "%s")  and  vip_client.code=account_integral.card_id
			and vip_client.guest_id=guest.id
			and vip_client.code*=mag_card.id
GROUP BY ACCOUNT_integral.CARD_ID,
			GUEST.ID,
			GUEST.NAME,
			GUEST.BIRTHDAY,
			GUEST.MANAGER,
			GUEST.MOBILE,
			GUEST.EMAIL,
			GUEST.CLIENT_TYPE,
         GUEST.HOMEPHONE,
			GUEST.POSTCODE,
			GUEST.ADDRESS,
         GUEST.BIRTHDAY,
			vip_client.startdate,
			vip_client.stopdate,
			isnull(mag_card.card_face,vip_client.code)
 having SUM(ACCOUNT_integral.INTEGRAL * ACCOUNT_integral.STATE)>=-99999999.00 and SUM(ACCOUNT_integral.INTEGRAL * ACCOUNT_integral.STATE)<=99999999.00
        '''%(code)).fetchone()[12]
        return '卡号:%s  积分:%.2f' % (code,count)
    except:
        return False
    finally:
        if conn_state != None:
            cursor.close()
        else:
            cursor.close()
            conn.close()
