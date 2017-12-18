#NOAA-GFS
#https://node.windy.com/forecast/v2.1/gfs/43.663/-79.399?source=detail
#EC
#https://node.windy.com/forecast/v2.1/ecmwf/43.663/-79.399?setup=summary&includeNow=true&source=hp
import sys
import matplotlib as mpl
import datetime
import dateutil
mpl.use('Agg')

import json
import urllib.request
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
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

def getweather(inlon,inlat,insource):
    global date
    global HI
    global LOW
    source = insource
    # lon = -79.399
    # lat = 43.663
    try:
        lon = float(inlon)
        lat = float(inlat)
    except:
        return False

    iodata = getdetail(source, lon, lat)
    grounddata = getData(source, lon, lat)
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

    gs = gridspec.GridSpec(2, 2, width_ratios=[40, 1], height_ratios=[2.5, 1])
    gs.update(wspace=0.05, hspace=0.045)
    ax0 = plt.subplot(gs[0])

    plt.title('Weather variables Forecast @ Louis-He\n' + 'Forecast Location:' + str(lon) + LON + ', ' + str(
        lat) + LAT + '\n' + 'Model:' + iodata['header']['model'] + ' Init time: ' + iodata['header'][
                  'refTime'] + ' UTC', loc='left', fontsize=11)
    #ax0.add_axes([0.1, 0.1, 0.8, 0.78])
    levels = np.arange(-50, 35, 2)
    CS = ax0.contour(X, Y, Tdata, levels, linewidths=0.35, colors='B')
    plt.ylabel('hpa')
    norm = mpl.colors.Normalize(vmin=0, vmax=100)
    ax0.clabel(CS, inline=1, fontsize=7, fmt='%.0f')
    ax0.invert_yaxis()
    ax0.contourf(X, Y, RHdata, cmap=cm.PuBu, norm=norm)
    ax0.barbs(X, Y, WUdata, WVdata, length=4,
              sizes=dict(emptybarb=0, spacing=0.2, height=0.5), barb_increments=dict(half=2, full=4, flag=20),
              linewidth=0.25, color='black')
    ax0.set_xticks([])
    ax0.set_xlim(1, count - 1)
    ax0.set_ylim(1000, 200)

    ax1 = plt.subplot(gs[1])
    #ax2 = ax0.add_axes([0.92, 0.11, 0.018, 0.77])
    cbar = mpl.colorbar.ColorbarBase(ax1, cmap=cm.PuBu, norm=norm, orientation='vertical', drawedges=False)
    cbar.ax.set_ylabel('%', size=8)
    cbar.set_ticks(np.linspace(0, 100, 10))
    cbar.set_ticklabels(('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'))

    ax2 = plt.subplot(gs[2])
    x = np.arange(1, len(getgroundT(source, grounddata)) + 1, 1)
    y = getgroundT(source, grounddata)
    plt.ylabel('°C')
    ax2.plot(x, y, 'r-', label='Temperature')
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    plt.xticks(ticks, newdates, rotation=30)
    plt.grid(True)
    plt.savefig('website/static/images/' + insource + '_' + str(lon) + LON + str(lat) + LAT +'.png')

    return True
    # analyze(source, iodata)
    # dailygraph()

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
      else:
         print ("ERR: unknown arg:",arg)
   else:
      skip=False

date = []
HI = []
LOW = []
#getweather(121.44, 31.25)
getweather(lon, lat, source)
'''
sched = BlockingScheduler()
sched.add_job(getweather, 'interval', seconds = 3 * 60 * 60)
sched.start()
'''