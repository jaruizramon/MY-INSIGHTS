# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 22:45:03 2019

@author: Pipo
"""

import pygame
import datetime
import os
import lxml
import sys
import re

from bs4 import BeautifulSoup
from threading import Thread, Lock
from time import sleep


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pyvirtualdisplay import Display
from time import sleep

import requests as req

def get_grades():
        
    global day, date, days_til_vacation, time 
    global class_slot1, class_slot2, class_slot3, class_slot4, class_slot5, class_slot6, class_slot7
    global grade_slot1, grade_slot2, grade_slot3, grade_slot4, grade_slot5, grade_slot6, grade_slot7
    global ratio_slot1, ratio_slot2, ratio_slot3, ratio_slot4, ratio_slot5, ratio_slot6, ratio_slot7

    global n
    global driver
        
    junk = "-nograde% "

    mail = ''  #canvas e-mail here
    passw = '' #canvas password here

    display = Display(visible=0, size=(1178, 650))
    display.start()

    n = 'launching driver'
     
    profile = webdriver.FirefoxProfile()
    profile.native_events_enabled = False
    driver = webdriver.Firefox(profile)
    driver.set_page_load_timeout(10)
    
    request_passed = False
    
    while(request_passed == False):
        try:
            driver.get("https://fgcu.instructure.com/")
            request_passed = True
        except:
            n = 'retrying'
            sleep(1)

    uin = driver.find_element_by_xpath('//*[@id="username"]')
    uin.clear()

    uin.send_keys(mail)
    
    passkey = driver.find_element_by_xpath('//*[@id="password"]')
    passkey.clear()
    passkey.send_keys(passw)
    passkey.send_keys(Keys.RETURN)

    sleep(2)

    n = 'logged in!'
    
    request_passed = False
    
    while(request_passed == False):
        try:
            driver.get('https://fgcu.instructure.com/grades')
            request_passed = True
        except:
            n = 'retrying'
            sleep(1)
            
    n = 'requesting data..'

    
    
    while(True):
        
        try:
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            sleep(4)

            table = soup.find('table' , {'class','course_details student_grades'})
            trs = table.find_all('tr')

            index = 0
            elementus = len(trs)
        
##            while (index <= elementus):
##                check_string = str(trs[index].text)
##                partition_string = check_string[0:7]
##                regex = re.compile('[A-Z]{3} [0-9]{4}')
##
##                if regex.match('xxx xxxx') is not None:
##                    print(trs[index].text)
##                    pass
##                else:
##                    trs[index].decompose()
##                    elementus -= 1
##                    
##                index += 1
            
    
            class_slot1 = str(trs[0].text)[0:10].strip()
            class_slot2 = str(trs[1].text)[0:10].strip()
            class_slot3 = str(trs[2].text)[0:10].strip()
            class_slot4 = str(trs[3].text)[0:10].strip()
            class_slot5 = str(trs[4].text)[0:10].strip()
            class_slot6 = str(trs[5].text)[0:10].strip()
            class_slot7 = str(trs[6].text)[0:10].strip()
            
            grade_slot1 = str(trs[0].text)[-18:-1].replace(junk,'').strip()
            grade_slot2 = str(trs[1].text)[-18:-1].replace(junk,'').strip()
            grade_slot3 = str(trs[2].text)[-18:-1].replace(junk,'').strip()
            grade_slot4 = str(trs[3].text)[-18:-1].replace(junk,'').strip()
            grade_slot5 = str(trs[4].text)[-18:-1].replace(junk,'').strip()
            grade_slot6 = str(trs[5].text)[-18:-1].replace(junk,'').strip()
            grade_slot7 = str(trs[6].text)[-18:-1].replace(junk,'').strip()

            n = ''
            sleep(60)

  
        except:
              
            class_slot1 = 'ERR'
            class_slot2 = 'ERR'
            class_slot3 = 'ERR'
            class_slot4 = 'ERR'
            class_slot5 = 'ERR'

            grade_slot1 = 'ERR'
            grade_slot2 = 'ERR'
            grade_slot3 = 'ERR'
            grade_slot4 = 'ERR'
            grade_slot5 = 'ERR'

            n = 'NO SUCH DATA FOUND!'

        n = 'refreshing data...'      
        driver.get('https://fgcu.instructure.com/grades')  
        n = ''
        
def run():   

    global driver
    
    BLACK = ( 0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGH = 720
    
    
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGH], pygame.FULLSCREEN)
    
    # font declarator
    HIGHWAY_FONT = pygame.font.SysFont('Highway Gothic', 45) # font declarator
    HIGHWAY_FONT_NARROW = pygame.font.SysFont('Highway Gothic Condensed', 45)
    keys = pygame.key.get_pressed()
    
    isRunning = True
    
    while isRunning:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:

                pygame.quit()
                driver.quit()
                sys.exit()
                isRunning = False
                
            elif event.type == pygame.KEYDOWN:
                
                keys = pygame.key.get_pressed()
                pygame.quit()
                driver.quit()
                sys.exit()
                
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            
            isRunning = False
    
                
                
            
                        
        screen.fill((0,0,0))
    
        days_til_vacation = 000
        
        time = datetime.datetime.now()
        
        clock = time.strftime('%I:%M %p')
        
        
        day = str(time.day)
        month = str(time.month)
        year = str(time.year)
        
        the_date = month + '/' + day + '/' + year
                
        day_display = HIGHWAY_FONT.render(the_date, True, WHITE)
        screen.blit(day_display, (20,30))
        
        date_display = HIGHWAY_FONT.render(str(), True, WHITE)
        screen.blit(date_display, (240,30))
        
        vac_display = HIGHWAY_FONT_NARROW.render('DAYS TILL VACATION: ' + str(days_til_vacation), True, WHITE)
        screen.blit(vac_display, (650,30))
        
        time_display = HIGHWAY_FONT.render(str(clock), True, WHITE)
        screen.blit(time_display, (1050,30))

        n_display = HIGHWAY_FONT.render(str(n), True, WHITE)
        screen.blit(n_display, (10,500))
        
        class_slot1_display = HIGHWAY_FONT.render(str(class_slot1), True, WHITE)
        screen.blit(class_slot1_display, (20,100))
        
        class_slot2_display = HIGHWAY_FONT.render(str(class_slot2), True, WHITE)
        screen.blit(class_slot2_display, (20,150))
        
        class_slot3_display = HIGHWAY_FONT.render(str(class_slot3), True, WHITE)
        screen.blit(class_slot3_display, (20,200))
        
        class_slot4_display = HIGHWAY_FONT.render(str(class_slot4), True, WHITE)
        screen.blit(class_slot4_display, (20,250))
        
        class_slot5_display = HIGHWAY_FONT.render(str(class_slot5), True, WHITE)
        screen.blit(class_slot5_display, (20,300))

        class_slot6_display = HIGHWAY_FONT.render(str(class_slot6), True, WHITE)
        screen.blit(class_slot6_display, (20,350))

        class_slot7_display = HIGHWAY_FONT.render(str(class_slot7), True, WHITE)
        screen.blit(class_slot7_display, (20,400))
        


        grade_slot1_display = HIGHWAY_FONT.render(str(grade_slot1), True, WHITE)
        screen.blit(grade_slot1_display, (250,100))
        
        grade_slot2_display = HIGHWAY_FONT.render(str(grade_slot2), True, WHITE)
        screen.blit(grade_slot2_display, (250,150))
        
        grade_slot3_display = HIGHWAY_FONT.render(str(grade_slot3), True, WHITE)
        screen.blit(grade_slot3_display, (250,200))
        
        grade_slot4_display = HIGHWAY_FONT.render(str(grade_slot4), True, WHITE)
        screen.blit(grade_slot4_display, (250,250))
        
        grade_slot5_display = HIGHWAY_FONT.render(str(grade_slot5), True, WHITE)
        screen.blit(grade_slot5_display, (250,300))
        
        grade_slot6_display = HIGHWAY_FONT.render(str(grade_slot6), True, WHITE)
        screen.blit(grade_slot6_display, (250,350))

        grade_slot7_display = HIGHWAY_FONT.render(str(grade_slot7), True, WHITE)
        screen.blit(grade_slot7_display, (250,400))
        
        
        ratio_slot1_display = HIGHWAY_FONT.render(str(ratio_slot1), True, WHITE)
        screen.blit(ratio_slot1_display, (450,100))
     
        ratio_slot2_display = HIGHWAY_FONT.render(str(ratio_slot2), True, WHITE)
        screen.blit(ratio_slot2_display, (450,150))
        
        ratio_slot3_display = HIGHWAY_FONT.render(str(ratio_slot3), True, WHITE)
        screen.blit(ratio_slot3_display, (450,200))   
        
        ratio_slot4_display = HIGHWAY_FONT.render(str(ratio_slot4), True, WHITE)
        screen.blit(ratio_slot4_display, (450,250))    
        
        ratio_slot5_display = HIGHWAY_FONT.render(str(ratio_slot5), True, WHITE)
        screen.blit(ratio_slot5_display, (450,300))

        ratio_slot6_display = HIGHWAY_FONT.render(str(ratio_slot6), True, WHITE)
        screen.blit(ratio_slot6_display, (450,350))    
        
        ratio_slot7_display = HIGHWAY_FONT.render(str(ratio_slot7), True, WHITE)
        screen.blit(ratio_slot7_display, (450,400))
        
        
        google_calendar_header = HIGHWAY_FONT.render('GOOGLE CALENDAR', True, WHITE)
        screen.blit(google_calendar_header, (650,100))
        
        pygame.display.flip()
        sleep(1)
    
    del HIGHWAY_FONT
    del HIGHWAY_FONT_NARROW
    
    pygame.quit()

''' 
S T A R T
'''
global day, date, days_til_vacation, time 
global class_slot1, class_slot2, class_slot3, class_slot4, class_slot5, class_slot6, class_slot7
global grade_slot1, grade_slot2, grade_slot3, grade_slot4, grade_slot5, grade_slot6, grade_slot7
global ratio_slot1, ratio_slot2, ratio_slot3, ratio_slot4, ratio_slot5, ratio_slot6, ratio_slot7

global n
global driver

class_slot1 = ''
class_slot2 = ''
class_slot3 = ''
class_slot4 = ''
class_slot5 = ''
class_slot6 = ''
class_slot7 = ''


grade_slot1 = ''
grade_slot2 = ''
grade_slot3 = ''
grade_slot4 = ''
grade_slot5 = ''
grade_slot6 = ''
grade_slot7 = ''

ratio_slot1 = ''
ratio_slot2 = ''
ratio_slot3 = ''
ratio_slot4 = ''
ratio_slot5 = ''
ratio_slot6 = ''
ratio_slot7 = ''

n = 'initialized'

t1 = Thread(target=get_grades) # second track
t2 = Thread(target=run) # first track

# start all the processes first 
t1.start()
t2.start()

sleep(5)

# join them in order to run them at the same time (supposedly)
t1.join()
t2.join()
