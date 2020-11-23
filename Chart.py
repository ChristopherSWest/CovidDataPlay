import requests
from matplotlib import pyplot as plt
import datetime
"""
Programmer: Christopher West
Purpose: This is a Chart class to create a simple bar graph and sevend day average line plot 
         of Covid19 data collected by the Covid Tracking project using their data API and 
         matplotlib.  The charts are similar to the charts used on the Covid Tracking Project's website

"""


class Chart:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fig = plt.figure()

        self.ax = self.fig.add_axes([0.1,0.05,0.9,0.95])
        self.ax.bar(self.x,self.y)

        self.seven_day = self.seven_day_average(self.y)
        self.seven_day.reverse()
        plt.plot(self.x, self.seven_day)

    def seven_day_average(self, clist):
        #print(clist)
        seven_list = []
        clist.reverse()
        
        for i in range(len(clist)):
            count = 0
            sum = 0
            average = 0
            if i == 0:
                sum += clist[i]
                count += 1
            elif i > 0 and i < 7:
                
                for j in range(i):
                    sum += clist[i-j]
                    count += 1
                
                average = sum/count
                count = 0
                sum = 0
            else:
                for j in range(7):
                    sum += clist[i-j]
                    count += 1
                average = sum/count
            seven_list.append(average)
        
        return seven_list