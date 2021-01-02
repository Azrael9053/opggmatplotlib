from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.widgets import Slider,RadioButtons
import requests

token = '填你自己的token'
browser = webdriver.Chrome('./chromedriver')
browser.get('https://tw.op.gg/')
html = browser.page_source
browser.quit()
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
clist = soup.find_all('td', class_='index-champion-table__cell index-champion-table__cell--champion')
value_list = soup.find_all('td', class_='index-champion-table__cell index-champion-table__cell--value')
position_champion = soup.find_all('div', class_='index-champion-position__name')
position_value_list = soup.find_all('div', class_='index-champion-position-stats__value')
count = 0
mode = 'by_tier' #選擇路線或牌位的模式
Win_Ratio = [] #按照路線的勝率
Pick_Rate = [] #按照路線的選角率
Ban_Rate = [] #按照路線的Ban角率
champion_list = [] #按照路線的英雄list
KDA_list = [] #按照牌位的KDA
pc_list = [] #按照牌位的英雄list
pp_list = [] #按照牌位的選角率
pw_list = [] #按照牌位的勝率

#取按照路線的英雄的名稱出來建list
for c in clist:
    champion_list.append(c.text)
print(champion_list)

#分別建立勝率 選角率 KDA的list
for v in value_list:
    if count % 3 == 0:
        Win_Ratio.append(float(v.text.replace('%', '')))
    elif count % 3 == 1:
        Pick_Rate.append(float(v.text.replace('%', '')))
    elif count % 3 == 2:
        KDA_list.append(float(v.text.replace(':1', '')))
    count += 1
by_tier_list = [champion_list, Win_Ratio, Pick_Rate, KDA_list]

#取按照牌位的英雄的名稱出來建list
for pc in position_champion:
    pc_list.append(pc.text)
print(pc_list)
count = 0

#分別建立選角率 勝率 BAN角的list
for pv in position_value_list:
    if count % 3 == 0:
        pp_list.append(float(pv.text.replace('%', '')))
    elif count % 3 == 1:
        pw_list.append(float(pv.text.replace('%', '')))
    elif count % 3 == 2:
        Ban_Rate.append(float(pv.text.replace('%', '')))
    count += 1
by_position_list = [pc_list, pp_list, pw_list, Ban_Rate]

#建立子圖物件
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3,left=0.3) #调整子图间距

axcolor = 'lightgoldenrodyellow'
cc = plt.axes([0.025, 0.5, 0.2, 0.15], facecolor=axcolor) #按鈕位置
radio = RadioButtons(cc, ('by_tier', 'by_position'), active=0) #建立按鈕物件

#選擇條的位置
om2 = plt.axes([0.25, 0.1, 0.6, 0.03], facecolor=axcolor)
om1 = plt.axes([0.25, 0.15, 0.6, 0.03], facecolor=axcolor)

#建立選擇條的物件
som1 = Slider(om1, 'by_tier', 1, 8, valinit=1, valstep=1)
som2 = Slider(om2, 'by_position', 1, 5, valinit=1, valstep=1)

metal_list = ['全體', '菁英', '大師', '鑽石', '白金', '金牌', '銀牌', '銅牌']
road_list = ['上路', '打野', '中路', '下路', '輔助']

#畫圖
def update(val, **attrs):
    index = np.arange(3)
    bar_width = 0.2
    ax.clear()
    ax.set_xticks(range(3))
    # global A, B, C
    #按照牌位的模式
    if mode == 'by_tier':
        #取選擇條的值
        if attrs == {}:
            s = int(som1.val)
        else:
            s = attrs['num']
        win = (Win_Ratio[s*3-3], Win_Ratio[s*3-2], Win_Ratio[s*3-1])
        pick = (Pick_Rate[s*3-3], Pick_Rate[s*3-2], Pick_Rate[s*3-1])
        kda = (KDA_list[s*3-3], KDA_list[s*3-2], KDA_list[s*3-1])
        A = ax.bar(index,
                    win,
                    bar_width)
        B = ax.bar(index + 0.2,
                    pick,
                    bar_width)
        C = ax.bar(index + 0.4,
                    kda,
                    bar_width)
        ax.legend([A, B, C], ['Win Ratio (%)', 'Pick Rate (%)', 'KDA'])
        ax.set_xticklabels([champion_list[s*3-3], champion_list[s*3-2], champion_list[s * 3 - 1]])
        ax.set_xlabel(metal_list[s-1])

    #按照路線的模式
    elif mode == 'by_position':
        #取選擇條的值
        if attrs == {}:
            s = int(som2.val)
        else:
            s = attrs['num']
        pp = (pp_list[s*3-3], pp_list[s*3-2], pp_list[s*3-1])
        pw = (pw_list[s*3-3], pw_list[s*3-2], pw_list[s*3-1])
        ban = (Ban_Rate[s*3-3], Ban_Rate[s*3-2], Ban_Rate[s*3-1])
        A = ax.bar(index,
                   pp,
                   bar_width)
        B = ax.bar(index + 0.2,
                   pw,
                   bar_width)
        C = ax.bar(index + 0.4,
                   ban,
                   bar_width)
        ax.legend([A, B, C], ['Pick Rate (%)', 'Win Ratio (%)', 'Ban Rate (%)'])
        ax.set_xticklabels([pc_list[s*3-3], pc_list[s*3-2], pc_list[s*3-1]])
        ax.set_xlabel(road_list[s - 1])
    createLabels(A)
    createLabels(B)
    createLabels(C)
    ax.set_title(f'OPGG 排行 {mode}')
    fig.canvas.draw_idle() #刷新圖表

#改變模式
def change_mode(label):
    global mode
    mode = label
    update(None)

#顯示圖表的數值
def createLabels(data):
    for item in data:
        height = item.get_height()
        ax.text(
            item.get_x()+item.get_width()/2.,
            height*1.02,
            '%d' % int(height),
            ha = "center",
            va = "bottom",
        )

def linenotify(token, msg, path):
    headers = {
        'Authorization':'Bearer ' + token
    }

    payload = {'message':msg}
    files = {'imageFile':open(path, 'rb')}
    r = requests.post('https://notify-api.line.me/api/notify',
                      headers = headers, params = payload, files = files)
    print(r.status_code)
    return r.status_code

plt.rcParams['font.sans-serif']=['MingLiu']

for rd in ['by_tier', 'by_position']:
    if rd == 'by_tier':
        for ss in range(1,9):
            mode = rd
            update(None, num=ss)
            plt.savefig(f'test{ss}.jpg')
    else:
        for ss in range(1,6):
            mode = rd
            update(None, num=ss)
            plt.savefig(f'test{ss+8}.jpg')

mode = 'by_tier'

for i in range(1, 13):
    image_path = f'test{i}.jpg'
    if i < 9:
        m = 'by_tier'
    else:
        m = 'by_position'
    message = 'OPGG 排行' + m
    linenotify(token, message, image_path)

#如果選擇條有調整的話就執行update函式
som1.on_changed(update)
som2.on_changed(update)

#如果選擇模式的按鈕調整就執行change_mode函式
radio.on_clicked(change_mode)

#初始化 先畫圖
update(None)
plt.show()