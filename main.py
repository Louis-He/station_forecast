#NOAA-GFS
#https://node.windy.com/forecast/v2.1/gfs/43.663/-79.399?source=detail
#EC
#https://node.windy.com/forecast/v2.1/ecmwf/43.663/-79.399?setup=summary&includeNow=true&source=hp
import matplotlib
matplotlib.use('Agg')

import json
import urllib.request
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
import time
from apscheduler.schedulers.background import BackgroundScheduler

def getData(org,lon,lat):
    if org == 'GFS':
        data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/gfs/' + str(lat) +'/' + str(lon) + '?source=detail').read()
    if org == 'EC':
        data = urllib.request.urlopen('https://node.windy.com/forecast/v2.1/ecmwf/' + str(lat) +'/' + str(lon) + '?setup=summary&includeNow=true&source=hp').read()
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
    plt.savefig("/root/web/static/easyplot.png")
    #plt.show()

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

    plt.savefig("/root/web/static/detailplot.png")
    #plt.plot_date(dates, values)
    #plt.xticks(timeseq, datelist, size='small', rotation=30)

def getweather():
    global date
    global HI
    global LOW
    global source
    iodata = getData(source, -79.399, 43.663)
    analyze(source, iodata)
    dailygraph()

date = []
HI = []
LOW = []
source = 'EC'
getweather()
scheduler = BackgroundScheduler()
scheduler.add_job(getweather, 'interval', seconds = 3 * 60 * 60)  # 间隔24小时执行一次
scheduler.start()  # 这里的调度任务是独立的一个线程