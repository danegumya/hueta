import matplotlib.pyplot as plt
import numpy as np

db=open('case_dataset.csv',encoding='utf8')
db.readline()
db1=open('dictionary_games_category.csv',encoding='utf8')

age_gender=['14-20m','21-30m','31-40m','41-50m','51-60m','>=61m','14-20f','21-30f','31-40f','41-50f','51-60f','>=61f']
data={}
for i in age_gender:
    data[i]=[0,0,0,{},0,0,0,0,0,0,0,0,0,0,0]
tpeople=0
data_games={}
interests_data={'14-30':{},
                '50+':{}}
for game in db1.readlines():
    z=list(game.split(','))
    data_games[z[0]]=z[1][:-1]
tmoney=0
tgame=0
tgamead=0
gpeople=0
ttsg=0

for user in db.readlines():
    user=list(user.split(';'))
    for i in range(len(user)):
        f=0
        if user[i] == '':
            user[i] = '0'
        for j in user[i]:
            if j not in '0123456789,.':
                f=1
        if f == 0:
            user[i]=float(user[i])
    rofls,country,age,gender,friends,heavy_plat,plat_arr,days_vk,ts_vk,days_feed,ts_feed,days_clips,ts_clips,days_video,ts_video,days_msg,ts_msg,days_games,ts_games,games_money_app,games_money_ad,total_money,games,cluster,interests= user[0],user[1],user[2],user[3],user[4],user[5],user[6],user[7],user[8],user[9],user[10],user[11],user[12],user[13],user[14],user[15],user[16],user[17],user[18],user[19],user[20],user[21],user[22],user[23],user[24]

    total_money=float(total_money)


    if (days_vk < 2 and ts_vk < 300) or (age<14) or (age>80) or friends>10000 or days_vk >30  or days_video > 30 or days_clips > 30 or days_games > 30 or days_msg > 30 or days_feed > 30 or ts_vk > 86400 or ts_games > 86400 or ts_msg > 86400 or ts_feed > 86400 or ts_clips > 86400 or ts_video > 86400 or gender not in [1,2]  or (games_money_ad+games_money_app) > total_money :
        continue
    tpeople += 1
    tmoney += total_money
    tgame += games_money_app
    tgamead += games_money_ad
    def get_age_label(age):
        if age <=20:
            return '14-20'
        elif age <= 30:
            return '21-30'
        elif age <= 40:
            return '31-40'
        elif age <= 50:
            return '41-50'
        elif age <= 60:
            return '51-60'
        else:
            return '>=61'

    age_label = get_age_label(age)
    gender_label = 'm' if gender == 2 else 'f'

    key = f"{age_label}{gender_label}"
    if interests != '[]':
        zv = list(interests.split(','))
        for i in range(len(zv)):
            zv[i] = zv[i].replace('[','')
            zv[i]=zv[i].replace(']','')
            zv[i]=zv[i].replace('\n','')
        for i in range(len(zv)):
            if zv[i] == '':
                continue
            if age >= 14 and age <= 30:
                if zv[i] in interests_data['14-30'].keys():
                    interests_data['14-30'][zv[i]] += 1
                else:
                    interests_data['14-30'][zv[i]] = 1
            elif age >= 50:
                if zv[i] in interests_data['50+'].keys():
                    interests_data['50+'][zv[i]] += 1
                else:
                    interests_data['50+'][zv[i]] = 1

    data[key][0] += 1
    data[key][1] += ts_video
    data[key][2] += ts_clips
    if games != '{}':
        gpeople+=1
        ttsg+=ts_games
        data[key][13]+=1
        rofls = list(games.split(','))
        rofls[0]=rofls[0][1:]
        rofls[-1]=rofls[-1][:-1]
       # print(rofls)
        for i in range(len(rofls)):
            x=data_games[rofls[i][0:rofls[i].index(':')]]
            y=rofls[i][rofls[i].index(':')+1:]
           # print(x,y)
            if x in data[key][3].keys():
                data[key][3][x]+=int(y)
            else:
                data[key][3][x]=int(y)
    data[key][4] += games_money_app
    data[key][5] += games_money_ad
    data[key][6] += ts_vk
    data[key][7] += ts_games

for key in data.keys():
    data[key][8] = round(data[key][4]/data[key][13],3)
    data[key][9] = round(data[key][5]/data[key][13],3)
    data[key][10] = round(data[key][6]/data[key][0],3)
    data[key][11] = round(data[key][7] / data[key][13], 3)
    data[key][12] = round((data[key][4]+data[key][5]) / data[key][13], 3)
    data[key][14] = round(data[key][7]/data[key][0],3)

for i in data.keys():
    z = {key: round(value / data[i][13],3) for key, value in data[i][3].items()}
    z = dict(sorted(z.items(), key=lambda item: item[1])[-10:])
    print(i + ' ' + str(z))

for i in interests_data.keys():
    z1 = dict(sorted(interests_data[i].items(), key=lambda item: item[1])[-10:])
    print(i + ': ' + str(z1))

plt.style.use('_mpl-gallery')

keys = list(data.keys())

print('Суммарная выручка не по категориям: ',tmoney)
print('Суммарная нерекламная выручка не по категориям: ',tgame)
print('Суммарная рекламная выручка не по категориям', tgamead)
print('Средняя выручка тотал без категорий: ', round(tmoney/tpeople,3))
print('Средняя выручка по рекламе без категорий: ', round(tgamead/gpeople,3))
print('Средняя выручка не по рекламе без категорий: ',round(tgame/gpeople,3))
print('Люди играющие: ', gpeople)
print('Люди: ',tpeople)
print('Среднее время в играх среди игроков: ', round(ttsg/gpeople,3))

values = np.array(list(data.values()))
n_groups = len(keys)

index = np.arange(n_groups)
bar_width = 0.6

metric_names = ['Количество пользователей в возрастной группе', 'Суммарное время в видео', 'Суммарное время в клипах',',metricname', 'Суммарная нерекламная выручка', 'Суммарная рекламная выручка', 'Суммарное время в ВК', 'Суммарное время в играх', 'Средняя нерекламная выручка', 'Средняя рекламная выручка','Среднее время в ВК', 'Среднее время в играх среди игроков', 'Средняя суммарная выручка в играх', 'Среднее время в играх среди всех пользователей']

for i in range(len(metric_names)):
    if i == 3:
        continue
    plt.figure(figsize=(12, 6))
    metric_values = values[:, i]
    plt.bar(index, metric_values, bar_width, color='c')

    plt.xlabel('Группы')
    plt.ylabel('Значения')
    plt.title(metric_names[i])
    plt.xticks(index, keys, rotation=45)

    plt.tight_layout()
    plt.show()

plt.rcParams['font.family'] = 'DejaVu Sans'
x = [2, 5, 8]
y = [2, 6, 7]
colors = ['#8024C0', '#FF3985', '#0077FF']
labels = [
    'Увеличение рекламного оборота',
    'Внедрение геймификации и реклама через блоггеров-инфлюенсеров',
    'Геймификация и интеграция B2B-сегмента'
]

plt.figure(figsize=(8, 6))
for i in range(len(x)):
    plt.scatter(x[i], y[i], color=colors[i], label=labels[i])

plt.xlim(0, 10)
plt.ylim(10, 0)

plt.xlabel('Эффективность от внедрения')
plt.ylabel('Сложность реализации')

plt.xticks(range(0, 11, 1))
plt.yticks(range(0, 11, 1))

plt.legend()
plt.tight_layout()
plt.show()