from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider,RadioButtons
import time

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
mode = 'by_tier'
Win_Ratio = []
Pick_Rate = []
Ban_Rate = []
champion_list = []
KDA_list = []
pc_list = []
pp_list = []
pw_list = []
for c in clist:
    champion_list.append(c.text)
for v in value_list:
    if count % 3 == 0:
        Win_Ratio.append(float(v.text.replace('%', '')))
    elif count % 3 == 1:
        Pick_Rate.append(float(v.text.replace('%', '')))
    elif count % 3 == 2:
        KDA_list.append(float(v.text.replace(':1', '')))
    count += 1
by_tier_list = [champion_list, Win_Ratio, Pick_Rate, KDA_list]
for pc in position_champion:
    pc_list.append(pc.text)
count = 0
for pv in position_value_list:
    if count % 3 == 0:
        pp_list.append(float(pv.text.replace('%', '')))
    elif count % 3 == 1:
        pw_list.append(float(pv.text.replace('%', '')))
    elif count % 3 == 2:
        Ban_Rate.append(float(pv.text.replace('%', '')))
    count += 1
by_position_list = [pc_list, pp_list, pw_list, Ban_Rate]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3,left=0.3) #调整子图间距

axcolor = 'lightgoldenrodyellow'
cc = plt.axes([0.025, 0.5, 0.2, 0.15], facecolor=axcolor)
radio = RadioButtons(cc, ('by_tier', 'by_position'), active=0)

om2 = plt.axes([0.25, 0.1, 0.6, 0.03], facecolor=axcolor)
om1 = plt.axes([0.25, 0.15, 0.6, 0.03], facecolor=axcolor)

som1 = Slider(om1, 'by_tier', 1, 8, valinit=1, valstep=1)
som2 = Slider(om2, 'by_position', 1, 5, valinit=1, valstep=1)
metal_list = ['全體', '菁英', '大師', '鑽石', '白金', '金牌', '銀牌', '銅牌']
road_list = ['上路', '打野', '中路', '下路', '輔助']

def update(val):
    index = np.arange(3)
    bar_width = 0.2
    ax.clear()
    ax.set_xticks(range(3))
    # global A, B, C
    if mode == 'by_tier':
        s = int(som1.val)
        win = (Win_Ratio[s*1-1], Win_Ratio[s*2-1], Win_Ratio[s*3-1])
        pick = (Pick_Rate[s*1-1], Pick_Rate[s*2-1], Pick_Rate[s*3-1])
        kda = (KDA_list[s*1-1], KDA_list[s*2-1], KDA_list[s*3-1])
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
        ax.set_xticklabels([champion_list[s * 1 - 1], champion_list[s * 2 - 1], champion_list[s * 3 - 1]])
        ax.set_xlabel(metal_list[s-1])
    elif mode == 'by_position':
        s = int(som2.val)
        pp = (pp_list[s * 1 - 1], pp_list[s * 2 - 1], pp_list[s * 3 - 1])
        pw = (pw_list[s * 1 - 1], pw_list[s * 2 - 1], pw_list[s * 3 - 1])
        ban = (Ban_Rate[s * 1 - 1], Ban_Rate[s * 2 - 1], Ban_Rate[s * 3 - 1])
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
        ax.set_xticklabels([pc_list[s * 1 - 1], pc_list[s * 2 - 1], pc_list[s * 3 - 1]])
        ax.set_xlabel(road_list[s - 1])
    createLabels(A)
    createLabels(B)
    createLabels(C)
    ax.set_title(f'OPGG 排行 {mode}')
    fig.canvas.draw_idle()

def change_mode(label):
    global mode
    mode = label
    update(None)

def createLabels(data):
    for item in data:
        height = item.get_height()
        ax.text(
            item.get_x()+item.get_width()/2.,
            height*1.05,
            '%d' % int(height),
            ha = "center",
            va = "bottom",
        )


som1.on_changed(update)
som2.on_changed(update)
radio.on_clicked(change_mode)
update(None)
plt.rcParams['font.sans-serif']=['MingLiu']
plt.show()