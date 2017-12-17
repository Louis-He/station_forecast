import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler

utc = 0
# draw all the plot in the waitlist file
def regular():
    # copy waitlistmission to onging
    os.system('cp website/waitlistmission.sh website/ongingmission.sh')
    # delete expired waitlist
    os.system('rm website/waitlistmission.sh')
    # create new waitlist file for further mission
    f = open('website/waitlistmission.sh', 'w+')
    f.close()

    # execute the latest onging mission
    os.system('sh website/ongingmission.sh')

# determine whether there are new waitlist plots
def isnewmission():
    f = open('website/waitlistmission.sh')  # Read waitlist mission
    line = f.readline()
    if line != '':
        f.close()
        return True
    f.close()
    return False

# main program to update all plots to the latest
print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tPlot System Start')
count = 0
while True:
    count += 1
    # delete all the products every six hours
    if count >= 6 * 60 * 60 / 5:
        path = 'website/static/images/'
        files = os.listdir(path)
        for file in files:
            if file[-3:] == 'png':
                os.system('rm website/static/images'+file)

    if isnewmission():
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time() + utc * 60 * 60)) + ']' + '\tPlot Start')
        regular()
    else:
        #print('NO new mission or onging mission is in place...')
        time.sleep(5)