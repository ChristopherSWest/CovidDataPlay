import pygame, sys, os, time
from pygame.locals import *
import tensorflow as tf
from Chart import Chart
import requests
from CovidDataHandler import CovidDataHandler
import numpy as np
from random import randrange

class CovidRiseAndFallGenerator:
    def __init__(self, key):
        """
        This chart is modeled after the overview chart the Covid Tracking Project uses at the top of their charts page.  The chart uses squares to represent the states and territories
        of the US.  The squares are colored based on if the cases are rising, falling or staying the same.  The generator attemps to do that
        """
        self.state_r = requests.get("https://api.covidtracking.com/v1/states/daily.json")
        self.state_data = self.state_r.json() 
        self.r = requests.get("https://api.covidtracking.com/v1/us/daily.json")

        self.d = self.r.json()
        self.key = key
        pygame.init()
        self.SIZE = 1400
        self.WIDTH = self.SIZE
        self.HEIGHT = self.SIZE * 0.571
        self.DISPLAY=pygame.display.set_mode((int(self.WIDTH),int(self.HEIGHT)),0,32)

        self.WHITE=(255,255,255)
        self.BLUE=(200,255,155)
        self.RED=(225,175,100)
        self.GRAY= (210,210,210)
        self.DISPLAY.fill(self.WHITE)

        self.chart_layout_dict = {
                "ME": [600,100],
                "WI": [375,145],
                "VT": [555,145],
                "NH": [600,145],
                "WA": [150,190],
                "ID": [195,190],
                "MT": [240,190],
                "ND": [285,190],
                "MN": [330,190],
                "IL": [375,190],
                "MI": [420,190],
                "NY": [510,190],
                "MA": [555,190],
                "OR": [150,235],
                "NV": [195,235],
                "WY": [240,235],
                "SD": [285,235],
                "IA": [330,235],
                "IN": [375,235],
                "OH": [420,235],
                "PA": [465,235],
                "NJ": [510,235],
                "CT": [555,235],
                "RI": [600,235],
                "CA": [150,280],
                "UT": [195,280],
                "CO": [240,280],
                "NE": [285,280],
                "MO": [330,280],
                "KY": [375,280],
                "WV": [420,280],
                "VA": [465,280],
                "MD": [510,280],
                "DE": [555,280],
                "AZ": [195,325],
                "NM": [240,325],
                "KS": [285,325],
                "AR": [330,325],
                "TN": [375,325],
                "NC": [420,325],
                "SC": [465,325],
                "DC": [510,325],
                "OK": [285,370],
                "LA": [330,370],
                "MS": [375,370],
                "AL": [420,370],
                "GA": [465,370],
                "GU": [60,415],
                "MP": [105,415],
                "HI": [150,415],
                "AK": [195,415],
                "TX": [285,415],
                "FL": [510,415],
                "PR": [555,415],
                "VI": [600,415],
                "AS": [150,460]
            }
        # The following path needs to be updated to point to the chartEye10.h5 file
        #TODO: Make this work with relative path
        self.checkpoint_path = "chartEye10.h5"
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)
        self.covidModel = tf.keras.models.load_model(self.checkpoint_path)
        self.cvid = CovidDataHandler(self.state_data)

        

    def render_chart(self, k):
        
        for item in self.chart_layout_dict:
            state_data_list = self.cvid.get_state_data_list(item, self.key)
            state_av_list = self.cvid.seven_day_average(state_data_list)
            state_data_list.reverse()
            test_item = self.cvid.get_two_week_list(state_data_list, state_av_list, len(state_data_list)-(1 + k))
            #print(new)
            test = []
            test.append(test_item)
            #print(test)
            prediction = self.covidModel.predict(test, verbose=0)
            newList = []
            prediction = np.array(prediction)
            
            
            normalize = []
            sum = prediction[0][0] + prediction[0][1] + prediction[0][2]
            
            for i in range(len(prediction[0])):
                normalize.append(prediction[0][i]/sum)
            for i in range(len(normalize)):
                normalize[i] = round(normalize[i], 2)
           
            randInt = randrange(100)
            font = pygame.font.SysFont('Arial', 22)
            #print(normalize)
            if randInt <= (normalize[0] * 100):
                #print(f"Cases are rising in {item}")
                square = pygame.draw.rect(self.DISPLAY,self.RED,(self.chart_layout_dict[item][0], self.chart_layout_dict[item][1], 40,40))
                self.DISPLAY.blit(font.render(item, True, (0,0,0)), (self.chart_layout_dict[item][0] + 10, self.chart_layout_dict[item][1] + 10))
            elif randInt <= ((normalize[1] + normalize[0]) * 100):# and randInt > (normalize[0] * 100):
                #print(f"Cases are staying about the same in {item}")
                square = pygame.draw.rect(self.DISPLAY,self.GRAY,(self.chart_layout_dict[item][0], self.chart_layout_dict[item][1], 40,40))
                self.DISPLAY.blit(font.render(item, True, (0,0,0)), (self.chart_layout_dict[item][0] + 10, self.chart_layout_dict[item][1] + 10))
            elif randInt <= ((normalize[1] + normalize[0] + normalize[2]) * 100):# and randInt > (normalize[0] * 100) + (normalize[1] * 100):
                #print(f"Cases are falling in {item}")
                square = pygame.draw.rect(self.DISPLAY,self.BLUE,(self.chart_layout_dict[item][0], self.chart_layout_dict[item][1], 40,40))
                self.DISPLAY.blit(font.render(item, True, (0,0,0)), (self.chart_layout_dict[item][0] + 10, self.chart_layout_dict[item][1] + 10))
    
    def generate(self):
        while True:
            i = 15
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
            #this.render_chart()           

            pygame.display.update()
            #time.sleep(0.5)
            i-=1

this = CovidRiseAndFallGenerator("positiveIncrease")
this.render_chart(0)
this.generate()

