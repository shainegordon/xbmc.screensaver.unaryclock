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


import threading
import datetime


class Controller(threading.Thread):
  
    def __init__(self, log_callback, drawClock_callback):
      super(Controller, self).__init__()
      self.log_callback = log_callback
      self.drawClock_callback = drawClock_callback
      self.waitCondition = threading.Condition()
      self._stop = False
      
    def run(self):
         self.waitCondition.acquire()
         while not self.shouldStop():
             self.now = datetime.datetime.today()
             self.waitFor = 10-self.now.second % 10
             
	     self.drawClock_callback()
         
             self.waitCondition.wait(self.waitFor)
         self.waitCondition.release()
      
      
    def shouldStop(self):
        '''
        Two conditions result in stopping: a call to stop(), or the window not
        being visible after once being visible.
        '''
        #visible = xbmc.getCondVisibility('Window.IsVisible(%s)' % WINDOW_ID)
        #if self.windowSighted and not visible:
        #    return True
        #elif visible:
        #     self.windowSighted = True
        return self._stop
        
    def stop(self):
        self.waitCondition.acquire()
        self._stop = True
        self.waitCondition.notifyAll()
        self.waitCondition.release()
