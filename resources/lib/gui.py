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

import controller

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')
image_dir = addon_path + "/resources/skins/default/media/"


lightSizeNormal = 50
lightPaddingNormal = 2
blockPaddingLarge = 50
blockPaddingSmall = 10
blockSizeNormal = 3
blockSizeSeconds = 8


scriptId   = 'screensaver.unaryclock'



class Screensaver(xbmcgui.WindowXMLDialog):

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
      
    def drawSinglePart(self, xOffset, yOffset, numberOfLights, blockSize, texture, imageOffset):
        lightBlock = self.computeActiveLights(blockSize, numberOfLights)
        lightSize = lightSizeNormal
        lightPadding = lightPaddingNormal
        #autoscaling
        if (blockSize > blockSizeNormal):
	    lightSize = ((blockSizeNormal*lightSize)+(blockPaddingSmall*(blockSizeNormal-1)) - blockSize*3)  / (blockSize+1)
	    lightPadding = 3
        for cell in range(0,blockSize*blockSize):
	    column = cell%blockSize
            row = cell/blockSize
            t = 'grey.png'
            
            newX = self.topX+xOffset+column*(lightSize+lightPadding)
            newY = self.topY+yOffset+row*(lightSize+lightPadding)
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
                

    def showClock(self, onlySeconds):
        now = datetime.datetime.today()
        if (onlySeconds == False):
            for b in self.allImages[:]:
	        b.setVisible(False)
	    self.topX = random.randint(blockPaddingLarge, self.getWidth() - self.totalClockWidth)
            self.topY = random.randint(blockPaddingLarge, self.getHeight() - self.totalClockHeight)
           
            hour = now.hour
            #self.log(('hour ' + str(hour)))
            self.drawSinglePart(0, 0, (hour/10), blockSizeNormal, 'red.png', 0)
            self.drawSinglePart(3*(lightSizeNormal+lightPaddingNormal)+1*blockPaddingSmall, 0, (hour%10), blockSizeNormal, 'cyan.png', 9)
       
            minute = now.minute
            #self.log(('minute ' + str(minute)))
            self.drawSinglePart(6*(lightSizeNormal+lightPaddingNormal)+1*blockPaddingSmall+blockPaddingLarge, 0, (minute/10), blockSizeNormal, 'green.png', 18)
            self.drawSinglePart(9*(lightSizeNormal+lightPaddingNormal)+2*blockPaddingSmall+blockPaddingLarge, 0, (minute%10), blockSizeNormal, 'purple.png', 27)
        if (self.showSeconds == True):
           second = now.second
           self.drawSinglePart(12*(lightSizeNormal+lightPaddingNormal)+3*blockPaddingSmall+2*blockPaddingLarge, 0, second, blockSizeSeconds, 'blue.png', 36)
        
        if (onlySeconds == False):
            for b in self.allImages[:]:
	        b.setVisible(True)
            

    def onInit(self):
	self.log("Screensaver starting")
        
        self.addon      = xbmcaddon.Addon(scriptId)
        if (self.addon.getSetting('setting_show_seconds') in ['false', 'False']):
            self.showSeconds = False
        else:
	    self.showSeconds = True
        self.redrawInterval = int(self.addon.getSetting('setting_redraw_interval'))
	self.monitor = self.ExitMonitor(self.exit, self.log)
	self.allImages = list()
	self.topX = blockPaddingLarge
        self.topY = blockPaddingLarge
        
        self.totalClockWidth = 4 * (blockSizeNormal*(lightSizeNormal + lightPaddingNormal)) + 2*blockPaddingSmall + 1*blockPaddingLarge
        if (self.showSeconds):
	  self.totalClockWidth = self.totalClockWidth + (blockSizeNormal*(lightSizeNormal + lightPaddingNormal)) + 1*blockPaddingLarge
        self.totalClockHeight = blockSizeNormal*(lightSizeNormal + lightPaddingNormal)
        
      
        self.log(addon_path)

        self.showClock(False)
	xbmc.sleep(1000)
        self.cont = controller.Controller(self.log, self.showClock, self.showSeconds, self.redrawInterval)
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

