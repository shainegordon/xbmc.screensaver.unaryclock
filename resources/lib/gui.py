#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Philip Schmiegelt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import random
import datetime
import time

import xbmcaddon
import xbmcgui
import xbmc

import numpy as np
import controller

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')
image_dir = addon_path + "/resources/skins/default/media/"



lightSize = 50
lightPadding = 2
blockPaddingLarge = 50
blockPaddingSmall = 10
blockSize = 3



class Screensaver(xbmcgui.WindowDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback, log_callback):
            self.exit_callback = exit_callback
	    self.log_callback = log_callback

        def onScreensaverDeactivated(self):
            self.log_callback('sending exit_callback')
            self.exit_callback()

        

    
    def computeActiveLights(self, size, numberOfLights):
        self.flatLightsArray = np.zeros((size*size))
        for number in range(0,numberOfLights):
            rand = random.randint(0,size*size-1)
            while self.flatLightsArray[rand] == 1:
               rand = (rand+1) % (size*size)
            self.flatLightsArray[rand] = 1
            numberOfLights = numberOfLights-1
            #self.log(self.flatLightsArray)
        return self.flatLightsArray
      
    def drawSinglePart(self, xOffset, yOffset, numberOfLights, texture):
        size = blockSize
        lightBlock = self.computeActiveLights(size, numberOfLights)
        for cell in range(0,size*size):
	    column = cell%size +1
            row = cell/size +1
            #self.log((str(cell) + ' ' + str(row) + ',' + str(column)))
            t = 'grey.png'
	    if (1 == lightBlock[cell]):
	      t = texture
            testbutton = xbmcgui.ControlButton(self.topX+xOffset+row*(lightSize+lightPadding),self.topY+yOffset+column*(lightSize+lightPadding),lightSize,lightSize, '', focusTexture=image_dir+t, noFocusTexture=image_dir+t)
            testbutton.setEnabled(False)
            testbutton.setVisible(False)
            self.allButtons.append(testbutton)
            self.addControl(testbutton)


    def showClock(self):
        for b in self.allButtons[:]:
	    b.setVisible(False)
            self.removeControl(b)
        del self.allButtons[:]
        self.log('len ' + str(len(self.allButtons)))
        now = datetime.datetime.today()
        hour = 23 #now.hour
        #self.log(('hour ' + str(hour)))
        self.drawSinglePart(0, 0, (hour/10), 'red.png')
        self.drawSinglePart(3*(lightSize+lightPadding)+1*blockPaddingSmall, 0, (hour%10), 'blue.png')
       
        minute = 59 #now.minute
        #self.log(('minute ' + str(minute)))
        self.drawSinglePart(6*(lightSize+lightPadding)+1*blockPaddingSmall+blockPaddingLarge, 0, (minute/10), 'green.png')
        self.drawSinglePart(9*(lightSize+lightPadding)+2*blockPaddingSmall+blockPaddingLarge, 0, (minute%10), 'purple.png')
        for b in self.allButtons[:]:
	    b.setVisible(True)
        self.topX = random.randint(50,500)
        self.topY = random.randint(50,500)

    def __init__(self):
	self.log("Screensaver starting");
	self.monitor = self.ExitMonitor(self.exit, self.log)
	self.allButtons = list()
	self.topX = 200
        self.topY = 200
        #self.strActionInfo = xbmcgui.ControlLabel(100, 120, 200, 200, '', 'font13', '0xFFFF00FF')
        #self.addControl(self.strActionInfo)
        #self.strActionInfo.setLabel('Push BACK to quit - A to reset text')
        #self.strActionFade = xbmcgui.ControlFadeLabel(200, 300, 200, 200, 'font13', '0xFFFFFF00')
        #self.addControl(self.strActionFade)
        #self.strActionFade.addLabel('This is a fade label')
        
        #self.testbutton = xbmcgui.ControlButton(150,150,50,50, '', focusTexture=image_dir+'red.png', noFocusTexture=image_dir+'red.png')
        #self.addControl(self.testbutton)
        self.log(addon_path)

	self.cont = controller.Controller(self.log, self.showClock)
        self.cont.start() 
        #self.showClock()
        
    

    def exit(self):
        self.log('Exit requested')
	self.cont.stop()
	del self.monitor
	del self.cont
	map(self.removeControl, self.allButtons)
        del self.allButtons[:]
        self.close()
    
    def log(self, msg):
        xbmc.log(u'Unary Clock Screensaver: %s' % msg)

