from PIL import Image,ImageDraw,ImageFont
import random
import time
import bot.models._Fcunction
from config import BALANCE_BABLE_IMG_PATH,TEMPORARY_PATH

def Get_R_G_B(r,g,b):
    return r + g*256 + b*256*256

def Get_image_bill_balance(title,datemin,datemax,list_str,fromname,printdate=time.strftime("%Y-%m-%d %H:%M:%S")):
    im = Image.open(BALANCE_BABLE_IMG_PATH)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\msyh.ttf", 12)
    font1 = ImageFont.truetype("C:\\WINDOWS\\Fonts\\msyh.ttf", 12)
    # 设置供应商名称
    draw.ink = Get_R_G_B(0, 0, 255)
    draw.text([115, 87],title, font=font)
    # 对账开始结束时间
    draw.text([154, 110], datemin, font=font)
    draw.text([335, 110], datemax, font=font)
    # 表格打印时间
    draw.text([583, 110],printdate, font=font)
    sell_all = 0  # 销售总金额
    sell_bill = 0  # 扣点后总金额
    cost_all = 0  # 费用总金额
    for i in range(len(list_str)):

        row = list_str[i]
        # 销售金额   X=180
        # 扣率  X=122
        # 扣点后金额   X=385
        # None
        # 扣费名称  X=519
        # 扣费金额  X=745
        # Y起点150 ,每级+22
        # 扣点金额  X=290
        Y = 22
        X = 770
        if row[0] != None:
            row[0]='%s'%row[0]
            row[1] = '%s' % row[1]
            row[2] = '%s' % row[2]
            if row[4]!='None':
                row[4] = '%s' % row[4]
                row[5] = '%s' % row[5]
            # 金额
            draw.ink = Get_R_G_B(0, 0, 255)
            draw.text([180, 150 + Y * i], row[0], font=font)
            draw.text([122, 150 + Y * i], row[1], font=font)
            draw.text([290, 150 + Y * i], '%.2f' % (float(row[0]) - float(row[2])), font=font)
            draw.text([385, 150 + Y * i], row[2], font=font)
            # 扣费名称
            draw.ink = Get_R_G_B(0, 0, 0)
            if row[4]!= 'None':
                draw.text([519, 150 + Y * i], bot.models._Fcunction.Decode_text(row[4]), font=font1)
                # 扣费金额
                draw.ink = Get_R_G_B(255, 0, 0)
                draw.text([X - len(row[5] * 5), 150 + Y * i], row[5], font=font)
                # 总金额计算
                cost_all = cost_all + float(row[5])
            sell_all = sell_all + float(row[0])
            sell_bill = sell_bill + float(row[2])
        else:
            if row[4]!='None':
                row[4] = '%s' % row[4]
                row[5] = '%s' % row[5]
                draw.ink = Get_R_G_B(0, 0, 0)
                draw.text([519, 150 + Y * i], bot.models._Fcunction.Decode_text(row[4]), font=font1)
                # 扣费金额
                draw.ink = Get_R_G_B(255, 0, 0)
                draw.text([X - len(row[5] * 5), 150 + Y * i], row[5], font=font)
                cost_all = cost_all + float(row[5])

    draw.ink = Get_R_G_B(0, 0, 255)
    draw.text([180, 502], '%.2f' % sell_all, font=font)
    draw.text([280, 502], '%.2f' % (sell_all - sell_bill), font=font)
    draw.text([380, 502], '￥%.2f' % sell_bill, font=font)
    draw.text([380, 525], '￥%.2f' % (sell_bill - cost_all), font=font)
    draw.ink = Get_R_G_B(255, 0, 0)
    draw.text([740, 502], '￥%.2f' % cost_all, font=font)
    path=r'%s\%s%s.png'%(TEMPORARY_PATH,fromname[1:10],random.randint(1,200))
    im.save(path, 'png')
    return path



def Create_rank_png():
    blank = Image.new("RGB", [200, 850], "white")
    draw = ImageDraw.Draw(blank)
    # 边框
    draw.line([0, 0, 200, 0], fill=10)
    draw.line([0, 849, 200, 849], fill=10)
    draw.line([0, 0, 0, 850], fill=10)
    draw.line([199, 0, 199, 850], fill=10)
    draw.line([0, 50, 200, 50], fill=10)

    for i in range(1, 40):
        draw.line([0, 50 + i * 20, 200, 50 + i * 20], fill=10)

    draw.line([150, 50, 150, 850], fill=10)
    del draw
    blank.save(r'\img\rank.png')

# def Sale_rank(title,*a,*b):
#     pass

# def Sale_rank_png(title,a,b):
#     if os.path.exists('temporary\%s.png'%title):
#         if datetime.date.today()!=title:
#             return 'temporary\%s.png' % title
#     im = Image.open('img/rank.png')
#     draw = ImageDraw.Draw(im)
#     # ========
#     font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simhei.TTF", 16)
#     draw.ink = 255 + 0+0
#     draw.text([3,20],title, font=font)
#     #========
#     font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\simhei.ttf", 12)
#     draw.ink = 0+0+0
#     for i in range(len(a) - 1):
#         #draw.ink = 255 + i * 9 + i * 9
#         draw.text([5, 55 + i * 20], a[i], font=font)
#         draw.text([170, 55 + i * 20], '%s' % b[i], font=font)
#     del draw
#     #im.save('temporary\%s.jpeg'%title)
#     im.save('temporary\%s.png'%title, 'png', quality=95)
#     return 'temporary\%s.png'%title

#
# if __name__=='__mian__':
#
