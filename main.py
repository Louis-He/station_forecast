#NOAA-GFS
#https://node.windy.com/forecast/v2.1/gfs/43.663/-79.399?source=detail
#EC
#https://node.windy.com/forecast/v2.1/ecmwf/43.663/-79.399?setup=summary&includeNow=true&source=hp
import sys
import matplotlib as mpl
import datetime
import dateutil
mpl.use('Agg')

import color
from area import *
import os
import math
import pygrib
import json
import urllib.request
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
from mpl_toolkits.basemap import Basemap, cm, shiftgrid
from matplotlib import gridspec
from matplotlib import ticker, dates
import time

mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'

from apscheduler.schedulers.blocking import BlockingScheduler

def getData(org,lon,lat):
    if org == 'GFS':
        data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/gfs/' + str(lat) +'/' + str(lon) + '?source=detail').read()
    if org == 'EC':
        #data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/ecmwf/' + str(lat) +'/' + str(lon) + '?setup=summary&includeNow=true&source=hp').read()
        data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/ecmwf/' + str(lat) + '/' + str(
            lon) + '?source=detail').read()
    record = data.decode('UTF-8')
    data = json.loads(record)

    '''
    for i in range(0,len(data)):
        station.append(data[i]['station']['city'])
        province.append(data[i]['station']['province'])
        code.append(data[i]['station']['code'])
        time.append(data[i]['publish_time'])
        T.append(data[i]['temperature'])
        day1day.append(float(data[i]['detail'][0]['day']['weather']['temperature']))
        day1night.append(data[i]['detail'][0]['night'])
        day2day.append(float(data[i]['detail'][1]['day']['weather']['temperature']))
        day2night.append(data[i]['detail'][1]['night'])

        day1dayweather.append(int(data[i]['detail'][0]['day']['weather']['img']))
        day2dayweather.append(int(data[i]['detail'][1]['day']['weather']['img']))
    '''
    return data

def getdetail(org, lon,lat):
    if org == 'GFS':
        data = urllib.request.urlopen('https://node.windy.com/forecast/meteogram/gfs/' + str(lat) +'/' + str(lon)).read()
    if org == 'EC':
        data = urllib.request.urlopen('https://node.windy.com/forecast/meteogram/ecmwf/' + str(lat) +'/' + str(lon)).read()
    record = data.decode('UTF-8')
    data = json.loads(record)
    return data

def getgroundT(source,JSON):
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    T = JSON['data']['temp']
    for i in range(0,len(T)):
        T[i] = T[i] - 273.15

    return T

def analyze(source,JSON):
    global date
    global HI
    global LOW
    #print(JSON)
    #'NOAA-GFS' OR 'ECMWF-HRES'
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    daily = JSON['summary']
    print(daily)
    for i in daily:
        daymax = daily[i]['tempMax']
        daymin = daily[i]['tempMin']
        print(i + '\tHI:' + str(round(daymax - 273.15, 1)) + '°C, LOW:' + str(round(daymin - 273.15, 1)) + '°C')
        date.append(int(i[5:7]+i[8:10]))
        HI.append(daymax-273.15)
        LOW.append(daymin-273.15)

    detaildata = JSON['data']

    TS = []
    T = []
    snow = []
    pp = []
    wind = []
    for i in detaildata['temp']:
        T.append(i - 273.15)
    for i in detaildata['ts']:
        TS.append(i)
    for i in detaildata['snow']:
        snow.append(i)
    for i in detaildata['mm']:
        pp.append(i)
    for i in detaildata['wind']:
        wind.append(i)
    print(pp)

    graph(source,TS,T,pp)

def analyzedetailT(source,JSON):
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    T1000 = JSON['data']['temp-1000h']
    T950 = JSON['data']['temp-950h']
    T900 = JSON['data']['temp-900h']
    T850 = JSON['data']['temp-850h']
    T800 = JSON['data']['temp-800h']
    T700 = JSON['data']['temp-700h']
    T600 = JSON['data']['temp-600h']
    T500 = JSON['data']['temp-500h']
    T400 = JSON['data']['temp-400h']
    T300 = JSON['data']['temp-300h']
    T200 = JSON['data']['temp-200h']

    T750 = []
    T650 = []
    T550 = []
    T450 = []
    T350 = []
    T250 = []
    count = 0
    for i in T800:
        T1000[count] -= 273.15
        T950[count] -= 273.15
        T900[count] -= 273.15
        T850[count] -= 273.15
        T800[count] -= 273.15
        T700[count] -= 273.15
        T600[count] -= 273.15
        T500[count] -= 273.15
        T400[count] -= 273.15
        T300[count] -= 273.15
        T200[count] -= 273.15
        T750.append((T700[count]+T800[count])/2.0)
        T650.append((T600[count] + T700[count]) / 2.0)
        T550.append((T500[count] + T600[count]) / 2.0)
        T450.append((T400[count] + T500[count]) / 2.0)
        T350.append((T300[count] + T400[count]) / 2.0)
        T250.append((T200[count] + T300[count]) / 2.0)
        count += 1

    print('T analyzed.')
    return [T1000,T950,T900,T850,T800,T750,T700,T650,T600,T550,T500,T450,T400,T350,T300,T250,T200]

def analyzedetailRH(source,JSON):
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    RH1000 = JSON['data']['rh-1000h']
    RH950 = JSON['data']['rh-950h']
    RH900 = JSON['data']['rh-900h']
    RH850 = JSON['data']['rh-850h']
    RH800 = JSON['data']['rh-800h']
    RH700 = JSON['data']['rh-700h']
    RH600 = JSON['data']['rh-600h']
    RH500 = JSON['data']['rh-500h']
    RH400 = JSON['data']['rh-400h']
    RH300 = JSON['data']['rh-300h']
    RH200 = JSON['data']['rh-200h']

    RH750 = []
    RH650 = []
    RH550 = []
    RH450 = []
    RH350 = []
    RH250 = []
    count = 0
    for i in RH800:
        RH750.append((RH700[count] + RH800[count])/2.0)
        RH650.append((RH600[count] + RH700[count]) / 2.0)
        RH550.append((RH500[count] + RH600[count]) / 2.0)
        RH450.append((RH400[count] + RH500[count]) / 2.0)
        RH350.append((RH300[count] + RH400[count]) / 2.0)
        RH250.append((RH200[count] + RH300[count]) / 2.0)
        count += 1

    print('RH analyzed.')
    return [RH1000,RH950,RH900,RH850,RH800,RH750,RH700,RH650,RH600,RH550,RH500,RH450,RH400,RH350,RH300,RH250,RH200]

def analyzedetailwindV(source,JSON):
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    WV1000 = JSON['data']['wind_v-1000h']
    WV950 = JSON['data']['wind_v-950h']
    WV900 = JSON['data']['wind_v-900h']
    WV850 = JSON['data']['wind_v-850h']
    WV800 = JSON['data']['wind_v-800h']
    WV700 = JSON['data']['wind_v-700h']
    WV600 = JSON['data']['wind_v-600h']
    WV500 = JSON['data']['wind_v-500h']
    WV400 = JSON['data']['wind_v-400h']
    WV300 = JSON['data']['wind_v-300h']
    WV200 = JSON['data']['wind_v-200h']

    WV750 = []
    WV650 = []
    WV550 = []
    WV450 = []
    WV350 = []
    WV250 = []
    count = 0
    for i in WV800:
        WV750.append((WV700[count] + WV800[count]) / 2.0)
        WV650.append((WV600[count] + WV700[count]) / 2.0)
        WV550.append((WV500[count] + WV600[count]) / 2.0)
        WV450.append((WV400[count] + WV500[count]) / 2.0)
        WV350.append((WV300[count] + WV400[count]) / 2.0)
        WV250.append((WV200[count] + WV300[count]) / 2.0)
        count += 1

    print('WV analyzed.')
    return [WV1000,WV950,WV900,WV850,WV800,WV750,WV700,WV650,WV600,WV550,WV500,WV450,WV400,WV350,WV300,WV250,WV200]

def analyzedetailwindU(source,JSON):
    model = JSON['header']['model']
    reftime = JSON['header']['refTime']
    WU1000 = JSON['data']['wind_u-1000h']
    WU950 = JSON['data']['wind_u-950h']
    WU900 = JSON['data']['wind_u-900h']
    WU850 = JSON['data']['wind_u-850h']
    WU800 = JSON['data']['wind_u-800h']
    WU700 = JSON['data']['wind_u-700h']
    WU600 = JSON['data']['wind_u-600h']
    WU500 = JSON['data']['wind_u-500h']
    WU400 = JSON['data']['wind_u-400h']
    WU300 = JSON['data']['wind_u-300h']
    WU200 = JSON['data']['wind_u-200h']

    WU750 = []
    WU650 = []
    WU550 = []
    WU450 = []
    WU350 = []
    WU250 = []
    count = 0
    for i in WU800:
        WU750.append((WU700[count] + WU800[count])/2.0)
        WU650.append((WU600[count] + WU700[count]) / 2.0)
        WU550.append((WU500[count] + WU600[count]) / 2.0)
        WU450.append((WU400[count] + WU500[count]) / 2.0)
        WU350.append((WU300[count] + WU400[count]) / 2.0)
        WU250.append((WU200[count] + WU300[count]) / 2.0)
        count += 1

    print('WU analyzed.')
    return [WU1000,WU950,WU900,WU850,WU800,WU750,WU700,WU650,WU600,WU550,WU500,WU450,WU400,WU350,WU300,WU250,WU200]

def analyzealert(source,data):
    # data: [lon, lat, T, dew, pp, snow, rain, pressure, wind, windgust, rh, ticks, newdates, reftime]
    # analyze rain alert (blue: >10mm/3hr; yellow: >20mm/3hr; red: >50mm/3hr)
    lon = data[0]
    lat = data[1]
    ticks = data[11]
    newdates = data[12]

    rainalert = []
    for i in data[6]:
        subindex = 0
        if i >= 50.0:
            subindex = 3
        elif i >= 20.0:
            subindex = 2
        elif i >= 10.0:
            subindex = 1
        else:
            subindex = 0
        rainalert.append(subindex)

    # analyze snow alert (blue: >2mm/3hr; yellow: >4mm/3hr; red: >8mm/3hr)
    snowalert = []
    for i in data[5]:
        subindex = 0
        if i >= 8.0:
            subindex = 3
        elif i >= 4.0:
            subindex = 2
        elif i >= 2.0:
            subindex = 1
        else:
            subindex = 0
        snowalert.append(subindex)

    # analyze T alert (blue: >30C or < 0C; yellow: >35C or < -4C; red: >37C or < -8)
    highTalert = []
    lowTalert = []
    for i in data[2]:
        subindex = 0
        if i >= 37.0:
            subindex = 3
        elif i >= 35.0:
            subindex = 2
        elif i >= 30.0:
            subindex = 1
        else:
            subindex = 0
        highTalert.append(subindex)

    for i in data[2]:
        subindex = 0
        if i <= -8.0:
            subindex = 3
        elif i <= -4.0:
            subindex = 2
        elif i <= 0.0:
            subindex = 1
        else:
            subindex = 0
        lowTalert.append(subindex)

    # analyze wind alert[gust] (blue: >10.8mm; yellow: >17.2; red: >24.5)
    windalert = []
    for i in data[8]:
        subindex = 0
        if i >= 24.5:
            subindex = 3
        elif i >= 17.2:
            subindex = 2
        elif i >= 10.8:
            subindex = 1
        else:
            subindex = 0
        windalert.append(subindex)

    if lon < 0:
        lon = -1 * lon
        LON = 'W'
    else:
        LON = 'E'

    if lat < 0:
        lat = -1 * lat
        LAT = 'S'
    else:
        LAT = 'N'

    fig = plt.figure(figsize=(10, 11), dpi=200)

    gs = gridspec.GridSpec(5, 1, height_ratios=[1, 1, 1, 1, 1])
    gs.update(wspace=0.1, hspace=0.1)

    ax0 = plt.subplot(gs[0])
    plt.title('Weather variables Forecast @ Louis-He\n' + 'Forecast Location:' + str(lon) + LON + ', ' + str(
        lat) + LAT + '\n' + 'Model:' + source + ' Init time: ' + data[13] + ' UTC', loc='left', fontsize=11)
    x = np.arange(1, len(rainalert) + 1, 1)
    plt.ylabel('Rainstorm Risk')
    ax0.bar(x, rainalert, color='r')
    for a, b in zip(x, rainalert):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.ylim(0, 3)
    ax0.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax1 = plt.subplot(gs[1])
    plt.ylabel('Snowstorm Risk')
    ax1.bar(x, snowalert, color = 'r')
    for a, b in zip(x, snowalert):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.ylim(0, 3)
    ax1.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax2 = plt.subplot(gs[2])
    plt.ylabel('Heatwave Risk')
    ax2.bar(x, highTalert, color='r')
    for a, b in zip(x, highTalert):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.ylim(0, 3)
    ax2.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax3 = plt.subplot(gs[3])
    plt.ylabel('Coldwave Risk')
    ax3.bar(x, lowTalert, color='r')
    for a, b in zip(x, lowTalert):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.ylim(0, 3)
    ax3.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax4 = plt.subplot(gs[4])
    plt.ylabel('Windy Risk')
    ax4.bar(x, windalert, color='r')
    for a, b in zip(x, windalert):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.ylim(0, 3)
    ax4.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    plt.savefig('website/static/images/A_' + source + '_' + str(lon) + LON + str(lat) + LAT +'.png')

    return True

def dailygraph():
    global date
    global HI
    global LOW
    plt.figure()
    #DEBUG PUROSE ONLY!
    #print(date)
    plt.plot(date, HI, label="Hi",color="red",linewidth=2)
    plt.plot(date, LOW, label="Low", color="blue", linewidth=2)
    plt.xlabel("Date")
    plt.ylabel("Temperature(°C)")
    plt.title("Temprerature forecast in Toronto")
    #plt.savefig("/root/web/static/easyplot.png")
    plt.show()

def graph(source, list, values1, values2):
    timeseq = []
    datelist = []
    '''
    start = datetime.datetime(int(time.strftime('%y', time.localtime(list[0] / 1000.0 - 4 * 60 * 60))),
                              int(time.strftime('%m', time.localtime(list[0] / 1000.0 - 4 * 60 * 60))),
                              int(time.strftime('%d', time.localtime(list[0] / 1000.0 - 4 * 60 * 60))),
                              int(time.strftime('%H', time.localtime(list[0] / 1000.0 - 4 * 60 * 60))))
    end = datetime.datetime(int(time.strftime('%y', time.localtime(list[len(list)-1] / 1000.0 - 4 * 60 * 60))),
                              int(time.strftime('%m', time.localtime(list[len(list)-1] / 1000.0 - 4 * 60 * 60))),
                              int(time.strftime('%d', time.localtime(list[len(list)-1] / 1000.0 - 4 * 60 * 60))),
                              int(time.strftime('%H', time.localtime(list[len(list)-1] / 1000.0 - 4 * 60 * 60))))
    delta = datetime.timedelta(days = 1/8)
    dates = mdate.drange(start, end, delta)
    '''
    for i in range(0,len(list)):
        datelist.append(list[i])
        datelist[i] = time.strftime('%d%H', time.localtime(list[i] / 1000.0 - 4 * 60 * 60))
        timeseq.append(i*3)
    print('DATELIST = ' + str(datelist))
    #dates = [datetime.datetime.strptime(elem, '%d %H') for elem in datelist]

    fig = plt.figure()
    '''

    # 获取当前的坐标
    ax = plt.gca()
    # 使用plot_date绘制日期图像
    ax.plot_date(dates, values1, linestyle="-", marker=".")

    # 设置日期的显示格式
    date_format = mdate.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_format)

    # 日期的排列根据图像的大小自适应
    fig.autofmt_xdate()

    plt.show()
    '''

    ax1 = fig.add_subplot(111)
    ax1.plot(timeseq, values1, 'r')
    ax1.set_ylabel('Temperature(C)')
    #plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%m-%d %H'))

    ax2 = ax1.twinx()  # this is the important function
    ax2.bar(timeseq, values2)
    ax2.set_ylabel('3 hours Precipitation(mm)')
    ax2.set_ylim([0, 30])

    ax1.xaxis.set_major_locator(MultipleLocator(12))
    if source == 'EC':
        plt.title('Toronto Weather Forecast for next 120 hours\n Model: ECMWF; Predict time from ' +
                  time.strftime('20%y-%m-%d %H:00', time.localtime(list[0] / 1000.0 - 4 * 60 * 60)))

    #plt.savefig("/root/web/static/detailplot.png")
    #plt.plot_date(dates, values)
    #plt.xticks(timeseq, datelist, size='small', rotation=30)

def getverticalweather(inlon,inlat,insource):
    source = insource
    # lon = -79.399
    # lat = 43.663
    try:
        lon = float(inlon)
        lat = float(inlat)
    except:
        return False

    iodata = getdetail(source, lon, lat)
    #grounddata = getData(source, lon, lat)
    hourspoint = iodata['data']['hours']

    for i in range(0, len(hourspoint)):
        hourspoint[i] = hourspoint[i] / 1000.0

    dates = [time.strftime('%d%Hz', time.localtime(ts)) for ts in hourspoint]
    newdates = []
    ticks = []
    count = 1
    for i in dates:
        if count % 2 == 0:
            newdates.append(i)
            ticks.append(count)
        count += 1
    print(dates)

    print('DATA RECEIVED.')
    Tdata = analyzedetailT(source, iodata)
    RHdata = analyzedetailRH(source, iodata)
    WVdata = analyzedetailwindV(source, iodata)
    WUdata = analyzedetailwindU(source, iodata)

    if lon < 0:
        lon = -1 * lon
        LON = 'W'
    else:
        LON = 'E'

    if lat < 0:
        lat = -1 * lat
        LAT = 'S'
    else:
        LAT = 'N'

    xmax = len(Tdata[0])
    deltay = -50
    x = np.arange(1, xmax + 1, 1)
    y = np.arange(1000, 150, deltay)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(13, 7), dpi=200)

    gs = gridspec.GridSpec(1, 2, width_ratios=[40, 1])
    gs.update(wspace=0.05, hspace=0.045)
    ax0 = plt.subplot(gs[0])

    plt.title('Weather variables Forecast @ Louis-He\n' + 'Forecast Location:' + str(lon) + LON + ', ' + str(
        lat) + LAT + '\n' + 'Model:' + iodata['header']['model'] + ' Init time: ' + iodata['header'][
                  'refTime'] + ' UTC', loc='left', fontsize=11)
    #ax0.add_axes([0.1, 0.1, 0.8, 0.78])
    levels = np.arange(-52, 36, 4)
    CS = ax0.contour(X, Y, Tdata, levels, linewidths=0.5, colors='R')
    plt.ylabel('hpa')
    norm = mpl.colors.Normalize(vmin=0, vmax=100)
    ax0.clabel(CS, inline=1, fontsize=10, fmt='%.0f')
    ax0.invert_yaxis()
    y1 = mpl.colors.LinearSegmentedColormap('my_colormap', color.rh, 256)
    ax0.contourf(X, Y, RHdata, cmap=y1, norm=norm)
    ax0.barbs(X, Y, WUdata, WVdata, length=4.5,
              sizes=dict(emptybarb=0, spacing=0.2, height=0.5), barb_increments=dict(half=2, full=4, flag=20),
              linewidth=0.35, color='black')
    #ax0.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    ax0.set_xlim(1, count - 1)
    ax0.set_ylim(1000, 200)

    ax1 = plt.subplot(gs[1])
    #ax2 = ax0.add_axes([0.92, 0.11, 0.018, 0.77])
    cbar = mpl.colorbar.ColorbarBase(ax1, cmap=y1, norm=norm, orientation='vertical', drawedges=False)
    cbar.ax.set_ylabel('%', size=8)
    cbar.set_ticks(np.linspace(0, 100, 11))
    cbar.set_ticklabels(('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'))

    '''
    ax2 = plt.subplot(gs[2])
    x = np.arange(1, len(getgroundT(source, grounddata)) + 1, 1)
    y = getgroundT(source, grounddata)
    plt.ylabel('°C')
    ax2.plot(x, y, 'r-', label='Temperature')
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)
    '''
    plt.savefig('website/static/images/V_' + insource + '_' + str(lon) + LON + str(lat) + LAT +'.png')

    return True
    # analyze(source, iodata)
    # dailygraph()

def getgroundweather(inlon,inlat,insource):
    source = insource
    # lon = -79.399
    # lat = 43.663
    try:
        lon = float(inlon)
        lat = float(inlat)
    except:
        return False

    #iodata = getdetail(source, lon, lat)
    grounddata = getData(source, lon, lat)
    hourspoint = grounddata['data']['ts']

    for i in range(0, len(hourspoint)):
        hourspoint[i] = hourspoint[i] / 1000.0

    dates = [time.strftime('%d%Hz', time.localtime(ts)) for ts in hourspoint]
    newdates = []
    ticks = []
    count = 1
    for i in dates:
        if count % 2 == 0:
            newdates.append(i)
            ticks.append(count)
        count += 1
    print(dates)

    print('DATA RECEIVED.')
    T = grounddata['data']['temp']
    dew = grounddata['data']['dewPoint']
    pp = grounddata['data']['mm']
    snow = grounddata['data']['snowPrecip']
    rain = []
    pressure = grounddata['data']['pressure']
    wind = grounddata['data']['wind']
    windgust = grounddata['data']['gust']
    rh = grounddata['data']['rh']

    Tdata = []
    Pdata = []
    dewdata = []
    for i in T:
       Tdata.append(i - 273.15)
    for i in dew:
       dewdata.append(i - 273.15)
    for i in pressure:
       Pdata.append(i / 100)
    for i in range(0,len(pp)):
        rain.append(pp[i] - snow[i])

    # execute analyze automatic alert
    analyzealert(insource, [lon, lat, Tdata, dew, pp, snow, rain, pressure, wind, windgust, rh, ticks, newdates, grounddata['header'][
                  'refTime']])


    if lon < 0:
        lon = -1 * lon
        LON = 'W'
    else:
        LON = 'E'

    if lat < 0:
        lat = -1 * lat
        LAT = 'S'
    else:
        LAT = 'N'

    fig = plt.figure(figsize=(10, 11), dpi=200)

    gs = gridspec.GridSpec(5, 1, height_ratios=[2, 1, 1, 1, 1])
    gs.update(wspace=0.05, hspace=0.045)
    ax0 = plt.subplot(gs[0])
    plt.title('Weather variables Forecast @ Louis-He\n' + 'Forecast Location:' + str(lon) + LON + ', ' + str(
        lat) + LAT + '\n' + 'Model:' + grounddata['header']['model'] + ' Init time: ' + grounddata['header'][
                  'refTime'] + ' UTC', loc='left', fontsize=11)
    x = np.arange(1, len(Tdata) + 1, 1)
    plt.ylabel('Temperature & dew(°C)')
    ax0.plot(x, Tdata, 'r-', label='Temperature')
    ax0.plot(x, dewdata, 'b-', label='Dew')
    for a, b in zip(x, Tdata):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    ax0.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax1 = plt.subplot(gs[1])
    plt.ylabel('Rain/Snow(mm)')
    ax1.bar(x, rain, color = 'b')
    ax1.bar(x, snow, bottom = rain,  color='#AAAAAA')
    for a, b in zip(x, pp):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)

    if max(pp) < 5.0:
        plt.ylim(0, 5)
    else:
        plt.ylim(0, max(pp) * 1.1)

    ax1.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax2 = plt.subplot(gs[2])
    plt.ylabel('Humidity(%)')
    ax2.plot(x, rh, 'g-', label='Humidity')
    for a, b in zip(x, rh):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    ax2.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax3 = plt.subplot(gs[3])
    plt.ylabel('10m Wind(m/s)')
    ax3.plot(x, wind, 'r-', label='Wind')
    for a, b in zip(x, wind):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    ax3.set_xticks([])
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    ax4 = plt.subplot(gs[4])
    plt.ylabel('Pressure(hPa)')
    ax4.plot(x, Pdata, 'b-', label='Pressure')
    ax4.set_xticks([])

    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)

    plt.savefig('website/static/images/G_' + insource + '_' + str(lon) + LON + str(lat) + LAT +'.png')

    return True
    # analyze(source, iodata)
    # dailygraph()

def getairrelated(inlon,inlat):
    try:
        float(inlon)
        float(inlat)
    except:
        return False

    lat = round(float(inlat) * 4) / 4
    if float(inlon) < 0:
        lon = round((360 + float(inlon)) * 4) / 4
    else:
        lon = round(float(inlon) * 4) / 4

    hours = ['000', '006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072', '078',
             '084',
             '090', '096', '102', '108', '114', '120']



    #data need:
    mslp = []
    rh_2m = []
    AV_850 = [] # absolute vorticity
    wind_10m = []
    VS_850 = [] # vertical speed
    PBL = [] # planetary Boundary Layer
    RT = [] # reverse T
    SWI = []

    path = '/root/GFS/rawfile/'
    files = os.listdir(path)
    for i in range(0,len(hours)):
        for file in files:
            if file[-3:] == hours[i]:
                subSWI = 0
                # read in files
                grbs = pygrib.open(path + file)

                MSLP_layer = grbs.select(name='MSLP (Eta model reduction)')[0]
                if hours[i] == '000':
                    # define the initial forecast hour
                    analysistime = MSLP_layer.analDate
                    fcit = analysistime.timetuple()  # time.struct_time
                    formatfcit = time.strftime('%Hz %m %d %Y', fcit)  # formatted initial time
                    timestampfcit = time.mktime(fcit)  # timestamp of initial time

                    fcst = MSLP_layer.forecastTime  # integer
                    formatvalid = time.strftime('%Hz %m %d %Y',
                                                time.localtime(timestampfcit + fcst * 60 * 60))  # formatted validtime


                data, lats, lons = MSLP_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                mslp.append(float(data)/1000)
                del MSLP_layer

                if float(data) <= 1030 and float(data) >= 1010:
                    subSWI += 1

                RH_layer = grbs.select(name='2 metre relative humidity')[0]
                data, lats, lons = RH_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                rh_2m.append(float(data))
                del RH_layer
                if float(data) >= 90:
                    subSWI += 5
                elif float(data) >= 80:
                    subSWI += 4
                elif float(data) >= 70:
                    subSWI += 3
                elif float(data) >= 60:
                    subSWI += 2
                elif float(data) >= 40:
                    subSWI += 1

                AV_layer = grbs.select(name='Absolute vorticity')[20]
                data, lats, lons = AV_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                AV_850.append(float(data))
                del AV_layer
                if float(data) <= 0.00002:
                    subSWI += 5

                U_10m_layer = grbs.select(name='10 metre U wind component')[0]
                V_10m_layer = grbs.select(name='10 metre V wind component')[0]
                data, lats, lons = U_10m_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                data2, lats, lons = V_10m_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                w = math.sqrt(float(data) * float(data) + float(data2) * float(data2))
                wind_10m.append(w)
                del U_10m_layer, V_10m_layer, data2
                if w <= 2:
                    subSWI += 4
                elif w <= 3:
                    subSWI += 3
                elif w <= 4:
                    subSWI += 1
                del w

                VS_850_layer = grbs.select(name='Vertical velocity')[15]
                data, lats, lons = VS_850_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                VS_850.append(float(data))
                del VS_850_layer
                if float(data) <= 0.2:
                    subSWI += 2

                PBL_layer = grbs.select(name='Planetary boundary layer height')[0]
                data, lats, lons = PBL_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                PBL.append(float(data))
                del PBL_layer
                if float(data) <= 300:
                    subSWI += 4
                elif float(data) <= 800:
                    subSWI += 2
                elif float(data) <= 1500:
                    subSWI += 1

                #find reverse T layer
                T850_layer = grbs.select(name='Temperature')[25]
                T850, lats, lons = T850_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                del T850_layer
                T925_layer = grbs.select(name='Temperature')[27]
                T925, lats, lons = T925_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                del T925_layer
                T1000_layer = grbs.select(name='Temperature')[30]
                T1000, lats, lons = T1000_layer.data(lat1=lat, lat2=lat, lon1=lon, lon2=lon)
                del T1000_layer

                if T850>T925 or T925>T1000 or T850>T1000:
                    subSWI += 3

                SWI.append(subSWI)
                print('[analyze complete]-file: ' + file)

    fig = plt.figure(figsize=(10, 9), dpi=200)

    gs = gridspec.GridSpec(5, 1, height_ratios=[2, 1, 1, 1, 1])
    gs.update(wspace=0.05, hspace=0.045)
    ax0 = plt.subplot(gs[0])
    plt.title('Air quality related Variables Forecast @ Louis-He\n' + 'Forecast Location:' + str(lon) + ', ' + str(
        lat) + '\n' + 'Model: GFS, Init time: ' + formatfcit, loc='left', fontsize=11)
    x = np.arange(1, len(mslp) + 1, 1)
    plt.ylabel('SWI(no unit)')
    ax0.plot(x, SWI, 'r-', label='SWI')
    for a, b in zip(x, SWI):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    ax0.set_xticks([])
    plt.xticks(x, hours, rotation=30)
    plt.grid(True)

    ax1 = plt.subplot(gs[1])
    plt.ylabel('wind(m/s)')
    ax1.plot(x, wind_10m, 'b-', label='wind')
    for a, b in zip(x, wind_10m):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    ax1.set_xticks([])
    plt.xticks(x, hours, rotation=30)
    plt.grid(True)

    ax2 = plt.subplot(gs[2])
    plt.ylabel('PBLH(m)')
    ax2.plot(x, PBL, 'g-', label='PBLH')
    for a, b in zip(x, PBL):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    ax2.set_xticks([])
    plt.xticks(x, hours, rotation=30)
    plt.grid(True)

    plt.xticks(x, hours, rotation=30)
    plt.grid(True)

    plt.savefig('website/static/images/E_GFS_' + str(lon) + 'E' + str(lat) + 'N' + '.png')
    print('Air related plot complete')
    return True

def plotmap(filetime, areatype, color, line, barb, contourfcolor, linecolor):
    # color: (T)T_2m, T_925, T_850, T_700, T_500, T_200, T_100
    # color: (W)W_10m, Wind_925, Wind_850, Wind_500, Wind_200, Wind_100, Gust_10m
    # color: (G)G_925, GPH_850, GPH_700, GPH_500, GPH_200, GPH_100
    # color: (R)R_2m, RH_925, RH_850, RH_700, RH_500, RH_200, RH_100
    # color: Haines Index, MSLP, Surface lifted index:K, Precipitable water, Total Cloud Cover, Convective available potential energy
    name = ''

    # plot the diagram of selected element
    # set boundary through areatype
    boundary = ''
    tmpstr = 'boundary=' + areatype
    ldict = locals()
    exec(tmpstr, globals(), ldict)
    boundary = ldict['boundary']
    # print(boundary)

    # read in files
    grbs = pygrib.open('/root/GFS/rawfile/' + filetime)
    # extract data from grib file
    # FOR COLOUR
    if color[:4] == 'T_2m':
        colorlabel = 'Temperature(℃)'
        name += '2m Temperature'
        C = grbs.select(name='2 metre temperature')[0].values
        C = C - 273.15
        min = -40
        max = 40
        bar = 21
    elif color[:1] == 'T':
        colorlabel = 'Temperature(℃)'
        grb = grbs.select(name='Temperature')
        if color[2:] == '925':
            name += '925hPa Temperature'
            C = grb[27].values
            min = -44
            max = 36
            bar = 21
        if color[2:] == '850':
            name += '850hPa Temperature'
            C = grb[25].values
            min = -50
            max = 30
            bar = 21
        if color[2:] == '700':
            name += '700hPa Temperature'
            C = grb[22].values
            min = -55
            max = 25
            bar = 21
        if color[2:] == '500':
            name += '500hPa Temperature'
            C = grb[18].values
            min = -70
            max = 10
            bar = 21
        if color[2:] == '200':
            name += '200hPa Temperature'
            C = grb[12].values
            min = -80
            max = 0
            bar = 21
        if color[2:] == '100':
            name += '100hPa Temperature'
            C = grb[10].values
            min = -90
            max = -10
            bar = 21
        C = C - 273.15
        del grb
    elif color[:5] == 'W_10m':
        colorlabel = 'Wind(m/s)'
        print ("hsw is lkx's pet pig.\n")
        name += '10m Wind Speed'
        C1 = grbs.select(name='10 metre U wind component')[0]
        C2 = grbs.select(name='10 metre V wind component')[0]
        C = np.power(np.power(C1.values, 2) + np.power(C2.values, 2), 1/2)
        min = 0
        max = 40
        bar = 11
        del C1, C2
    elif color[:1] == 'W':
        colorlabel = 'Wind(m/s)'
        grb1 = grbs.select(name='U component of wind')
        grb2 = grbs.select(name='V component of wind')
        if color[2:] == '925':
            name += '925hPa Wind Speed'
            C1 = grb1[28]
            C2 = grb2[28]
            min = 0
            max = 50
            bar = 11
        if color[2:] == '850':
            name += '850hPa Wind Speed'
            C1 = grb1[26]
            C2 = grb2[26]
            min = 0
            max = 70
            bar = 11
        if color[2:] == '700':
            name += '700hPa Wind Speed'
            C1 = grb1[23]
            C2 = grb2[23]
            min = 0
            max = 80
            bar = 21
        if color[2:] == '500':
            name += '500hPa Wind Speed'
            C1 = grb1[19]
            C2 = grb2[19]
            min = 0
            max = 90
            bar = 21
        if color[2:] == '200':
            name += '200hPa Wind Speed'
            C1 = grb1[13]
            C2 = grb2[13]
            min = 0
            max = 90
            bar = 21
        if color[2:] == '100':
            name += '100hPa Wind Speed'
            C1 = grb1[11]
            C2 = grb2[11]
            min = 0
            max = 100
            bar = 26
        C = np.power(np.power(C1.values, 2) + np.power(C2.values, 2), 1 / 2)
        del C1, C2
        del grb1, grb2
    elif color[:1] == 'G':
        colorlabel = 'Geopotential height(dagpm)'
        grb = grbs.select(name='Geopotential Height')
        if color[2:] == '925':
            name += '925hPa Geopotential height'
            C = grb[27].values
            min = 560
            max = 960
            bar = 11
        if color[2:] == '850':
            name += '850hPa Geopotential height'
            C = grb[25].values
            min = 1200
            max = 1600
            bar = 11
        if color[2:] == '700':
            name += '700hPa Geopotential height'
            C = grb[22].values
            min = 2800
            max = 3200
            bar = 11
        if color[2:] == '500':
            name += '500hPa Geopotential height'
            C = grb[18].values
            min = 5200
            max = 6000
            bar = 21
        if color[2:] == '200':
            name += '200hPa Geopotential height'
            C = grb[12].values
            min = 10900
            max = 12900
            bar = 11
        if color[2:] == '100':
            name += '100hPa Geopotential height'
            C = grb[10].values
            min = 15000
            max = 17000
            bar = 21
        del grb
    # FOR BARB
    if barb == 'none':
        pass
    else:
        grb1 = grbs.select(name='U component of wind')
        grb2 = grbs.select(name='V component of wind')
        if barb == '925':
            name += ', 925hPa Wind(barb)'
            u = grb1[28].values
            v = grb2[28].values
        if barb == '850':
            name += ', 850hPa Wind(barb)'
            u = grb1[26].values
            v = grb2[26].values
        if barb == '700':
            name += ', 700hPa Wind(barb)'
            u = grb1[23].values
            v = grb2[23].values
        if barb == '500':
            name += ', 500hPa Wind(barb)'
            u = grb1[19].values
            v = grb2[19].values
        if barb == '200':
            name += ', 200hPa Wind(barb)'
            u = grb1[13].values
            v = grb2[13].values
        if barb == '100':
            name += ', 100hPa Wind(barb)'
            u = grb1[11].values
            v = grb2[11].values

    # define longitude and latitude
    Temperature = grbs.select(name='Temperature')[25]
    lats, lons = Temperature.latlons()
    lats = (lats.T)[0]
    lons = lons[0]

    # define the initial forecast hour
    analysistime = Temperature.analDate
    fcit = analysistime.timetuple()  # time.struct_time
    formatfcit = time.strftime('%Hz %m %d %Y', fcit)  # formatted initial time
    timestampfcit = time.mktime(fcit)  # timestamp of initial time

    fcst = Temperature.forecastTime  # integer
    formatvalid = time.strftime('%Hz %m %d %Y',
                                time.localtime(timestampfcit + fcst * 60 * 60))  # formatted validtime
    del Temperature

    # generatre basemap
    m = Basemap(llcrnrlon=boundary[0], llcrnrlat=boundary[1], urcrnrlon=boundary[2], urcrnrlat=boundary[3],
                projection='lcc', lat_0=boundary[4], lon_0=boundary[5], resolution='l', area_thresh=100)
    lon, lat = np.meshgrid(lons, lats)
    x, y = m(lon, lat)

    fig = plt.figure(figsize=(10, 7), dpi=150)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color('none')

    # generate legend

    norm = mpl.colors.Normalize(min, max)

    # c=plt.contourf(x, y, rt, 750, cmap=my_cmap, norm=norm)
    cmap_user = plt.cm.bwr
    boundary = ''
    tmpstr = 'cmap_user=plt.cm.' + contourfcolor
    ldict = locals()
    exec(tmpstr, globals(), ldict)
    cmap_user = ldict['cmap_user']
    m.contourf(x, y, C, 20, cmap = cmap_user, norm = norm)  # ,norm=norm cmaps.temp_19lev NCV_jaisnd
    #d = m.contour(x, y, subT, 110, colors='red', linewidths=0.6, levels=0)
    #d1 = m.contour(x, y, subMSLP, 70, colors='whitesmoke', linewidths=0.5)  # , alpha=0.6
    #plt.clabel(d, inline=True, fmt='%.0f', fontsize=2)
    #plt.clabel(d1, inline=True, fmt='%.0f', colors='whitesmoke', fontsize=2)  # alpha=0.6,

    if barb != 'none':
        skip = slice(None, None, 5)
        # m.streamplot(x, y, u, v, linewidth=0.25, density=4, color='black', arrowsize=0.4, arrowstyle='->')
        m.barbs(x[skip, skip], y[skip, skip], u[skip, skip], v[skip, skip], length=3.5,
                sizes=dict(emptybarb=0, spacing=0.2, height=0.5), barb_increments=dict(half=2, full=4, flag=20),
                linewidth=0.2, color='black')

    # additional geoinfomation
    if areatype == 'CN':
        m.readshapefile('geo/cnhimap', 'states', drawbounds=True, linewidth=0.5, color='black')


    plt.title('GFS' + name + '\nlnit:' + formatfcit + ' Forecast Hour[' + str(
        fcst) + '] valid at ' + formatvalid + '\n@myyd & Louis-He',
              loc='left', fontsize=11)
    m.drawparallels(np.arange(0, 65, 10), labels=[1, 0, 0, 0], fontsize=8, linewidth=0.5, color='dimgrey',
                    dashes=[1, 1])
    m.drawmeridians(np.arange(0., 360., 10), labels=[0, 0, 0, 1], fontsize=8, linewidth=0.5, color='dimgrey',
                    dashes=[1, 1])
    m.drawcoastlines(linewidth=0.5)
    m.drawstates(linewidth=0.4, color='dimgrey')
    # m.readshapefile('/mnt/c/Users/10678/Desktop/GFS/shp/cnhimap', 'states', drawbounds=True, linewidth=0.5, color='black')
    ax2 = fig.add_axes([0.88, 0.11, 0.018, 0.77])
    cbar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_user, norm=norm, orientation='vertical', drawedges=False)
    cbar.set_ticks(np.linspace(min, max, bar))
    cbar.ax.set_ylabel(colorlabel, size=8)  # Temperature(℃)
    cbar.ax.tick_params(labelsize=8)
    # Temperature(℃)

    name = name.replace(' ','_')
    # GFS 10m Wind and 2m Air Temperature\nlnit:00z Nov 04 2017 Forecast Hour[36] valid at 12z Sun,Nov 05 2017 6-hour #ERA Interim 850hpa Wind speed and Temperature & 500hpa Geopotential Height#Streamlines
    plt.savefig('website/static/images/M_GFS_' + areatype + name + '-' + filetime + '.png', bbox_inches='tight')

    # delete plot for memory
    del fig
    plt.cla
    plt.clf()
    plt.close(0)
    del m, lon, lat, lons, lats, cbar, ax, ax2, x, y, analysistime, fcit, formatfcit, timestampfcit, fcst, formatvalid


    return False
source = 'EC'

nargs=len(sys.argv)
skip=False
for i in range(1,nargs):
   if not skip:
      arg=sys.argv[i]
      #print ("INFO: processing",arg)
      if arg == "--lon":
         if i != nargs-1:
            lon = sys.argv[i+1]
            skip = True
      elif arg == "--lat":
         if i != nargs-1:
            lat = sys.argv[i+1]
            skip = True
      elif arg == "--source":
         if i != nargs-1:
            source = sys.argv[i+1]
            skip = True
      elif arg == "--type":
          if i != nargs - 1:
              plottype = sys.argv[i + 1]
              skip = True
      elif arg == "--time":
          if i != nargs - 1:
              filetime = sys.argv[i + 1]
              skip = True
      elif arg == "--contourf":
          if i != nargs - 1:
              contourf = sys.argv[i + 1]
              skip = True
      elif arg == "--contour":
          if i != nargs - 1:
              contour = sys.argv[i + 1]
              skip = True
      elif arg == "--barb":
          if i != nargs - 1:
              barb = sys.argv[i + 1]
              skip = True
      elif arg == "--contourfcolor":
          if i != nargs - 1:
              contourfcolor = sys.argv[i + 1]
              skip = True
      elif arg == "--contourcolor":
          if i != nargs - 1:
              contourcolor = sys.argv[i + 1]
              skip = True
      elif arg == "--area":
          if i != nargs - 1:
              area = sys.argv[i + 1]
              skip = True
      else:
         print ("ERR: unknown arg:",arg)
   else:
      skip=False

date = []
HI = []
LOW = []
#getgroundweather(-79.40, 43.67, 'EC')
#getweather(121.44, 31.25)
#getverticalweather(lon, lat, source)
if plottype == 'vertical':
    getverticalweather(lon, lat, source)
elif plottype == 'ground':
    getgroundweather(lon, lat, source)
elif plottype == 'air':
    getairrelated(lon, lat)
elif plottype == 'map':
    plotmap(filetime, area, contourf, contour, barb, contourfcolor, contourcolor)
'''
sched = BlockingScheduler()
sched.add_job(getweather, 'interval', seconds = 3 * 60 * 60)
sched.start()
'''