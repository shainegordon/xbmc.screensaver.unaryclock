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

#import numpy as np
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
        def onAbortRequested(self):
	    self.log_callback('abort requested')
	    self.exit_callback()

        

    
    def computeActiveLights(self, size, numberOfLights): 
        self.flatLightsArray = list()
        for number in range(0,size*size):
            self.flatLightsArray.append(0)
        for number in range(0,numberOfLights):
            rand = random.randint(0,size*size-1)
            while self.flatLightsArray[rand] == 1:
               rand = (rand+1) % (size*size)
            self.flatLightsArray[rand] = 1
            numberOfLights = numberOfLights-1
            #self.log(self.flatLightsArray)
        return self.flatLightsArray
      
    def drawSinglePart(self, xOffset, yOffset, numberOfLights, texture, imageOffset):
        size = blockSize
        lightBlock = self.computeActiveLights(size, numberOfLights)
        for cell in range(0,size*size):
	    column = cell%size +1
            row = cell/size +1
            #self.log((str(cell) + ' ' + str(row) + ',' + str(column)))
            t = 'grey.png'
            newX = self.topX+xOffset+row*(lightSize+lightPadding)
            newY = self.topY+yOffset+column*(lightSize+lightPadding)
	    if (1 == lightBlock[cell]):
	      t = texture

            if (len(self.allImages)<=imageOffset+cell):
                image = xbmcgui.ControlImage(newX,newY,lightSize,lightSize, image_dir+t, 0)
                image.setVisible(False)
                self.allImages.append(image)
                self.addControl(image)
            else:
                self.allImages[imageOffset+cell].setImage(image_dir+t)
                self.allImages[imageOffset+cell].setPosition(newX,newY)
                


    def showClock(self):
        #self.log(xbmcgui.getCurrentWindowId())
        #self.log('drawing clock')
        for b in self.allImages[:]:
	    b.setVisible(False)
            #self.removeControl(b)
        #del self.allImages[:]
        #self.log('len ' + str(len(self.allImages)))
        now = datetime.datetime.today()
        hour = now.hour
        #self.log(('hour ' + str(hour)))
        self.drawSinglePart(0, 0, (hour/10), 'red.png', 0)
        self.drawSinglePart(3*(lightSize+lightPadding)+1*blockPaddingSmall, 0, (hour%10), 'blue.png', 9)
       
        minute = now.minute
        #self.log(('minute ' + str(minute)))
        self.drawSinglePart(6*(lightSize+lightPadding)+1*blockPaddingSmall+blockPaddingLarge, 0, (minute/10), 'green.png', 18)
        self.drawSinglePart(9*(lightSize+lightPadding)+2*blockPaddingSmall+blockPaddingLarge, 0, (minute%10), 'purple.png', 27)
        for b in self.allImages[:]:
	    b.setVisible(True)
        self.topX = random.randint(50,500)
        self.topY = random.randint(50,500)

    def __init__(self):
	self.log("Screensaver starting");
	self.monitor = self.ExitMonitor(self.exit, self.log)
	self.allImages = list()
	self.topX = 200
        self.topY = 200
        
        self.log(addon_path)

        
        self.cont = controller.Controller(self.log, self.showClock)
        self.cont.start() 
        #self.showClock()
        
        
    

    def exit(self):
        self.log('Exit requested')
	self.cont.stop()
	for b in self.allImages[:]:
	    b.setVisible(False)
	del self.monitor
	del self.cont
	for b in self.allImages[:]:
	    self.removeControl(b)
        del self.allImages[:]
        self.close()
    
    def log(self, msg):
        xbmc.log(u'Unary Clock Screensaver: %s' % msg)

