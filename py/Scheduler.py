#-----------------------------------------------------------------------------
# Name:        Scheduler.py
# Product:     ClamWin Free Antivirus
#
# Author:      alch [alch at users dot sourceforge dot net]
#
# Created:     2004/19/03
# Copyright:   Copyright alch (c) 2004
# Licence:
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#-----------------------------------------------------------------------------
#!/usr/bin/env python


import os, tempfile
import sched, time, locale, random
import types
import threading


class Scheduler(threading.Thread):
    # empty tuple for status_filenames parameter will reuslt in no checking
    # for missed schedules
    def __init__(self, frequency, startTime, weekDay, runMissed, action, argument=(),
            status_filenames=(), loopDelay = 0.5, label = int(time.clock()*10000000) + random.randint(0,1000)):
        threading.Thread.__init__(self)
        self._filenames = status_filenames
        self._delay = 0.5
        self._loopDelay = loopDelay
        self._cancelling = False
        self._frequency = frequency
        self._weekDay = weekDay
        self._startTime = startTime
        self._runMissed = runMissed

        self._action = action
        self._argument = argument
        self._lastRun = self._ReadLastRun()

        self._sched = sched.scheduler(time.time, self._DelayFunc)
        self._missedSchedule = False        
        self._paused = False
        self._label = label
        self._id = self._sched.enterabs(self._CalcNextRun(), 0, self._RunTask, ())

    def label(self):
        return self._label


    def reset(self, frequency, startTime, weekDay, action, argument=(), loopDelay = 0.2):
        self._delay = 1.0
        self._loopDelay = loopDelay
        self._cancelling = False
        self._frequency = frequency
        self._weekDay = weekDay
        self._startTime = startTime

        self._action = action
        self._argument = argument
        self._lastRun = self._ReadLastRun()
        self._missedSchedule = False
        self._paused = False
        # stop current thread
        self.stop()
        threading.Thread.__init__(self)


        # ensure it stopped
        i = 0
        while self.isAlive() and i < 50:
            time.sleep(0.1)
            i+=1

        # recreate scheduled event
        self._id = self._sched.enterabs(self._CalcNextRun(), 0, self._RunTask, ())


    def _ReadLastRun(self):
        # 0 signifies an error
        t = 0

        # read when the task was run last
        for filename in self._filenames:
            try:
                f = file(os.path.join(tempfile.gettempdir(), filename), 'r')
                t = f.read()
                f.close()
            except:
                t = 0
                continue
            # check that we have a float
            try:
                t = float(t)
            except ValueError:
                print 'time in %s is not float' % filename
                t = 0
                continue
            if time.time() < t:
                # got time in future, ignore it
                t = 0
                continue
            else:
                break

        return t

    def _WriteLastRun(self):
        # save time when the task was run for future
        for filename in self._filenames:
            try:
                f = file(os.path.join(tempfile.gettempdir(), filename), 'w')
                f.write(str(self._lastRun))
                f.close()
            except IOError:
                pass

    def _AdjustDST(self, t):
        # deal with daylight savings, if we're on the edge
        dstDiff = time.localtime().tm_isdst - time.localtime(t).tm_isdst
        t += dstDiff * 3600.00
        return t

    # returns time in seconds (as in time.time())
    # when next scheduled run occurs
    def _CalcNextRun(self, missedAlready = False):
        # calculate when the next task should run
        # depending on last run time, update frequency,
        # task start time and day of the week

        # set C locale, otherwise python and wxpython complain
        locale.setlocale(locale.LC_ALL, 'C')
        # get current time, skip milliseconds
        t = time.time()
        if self._frequency == 'Hourly':
            try:
                # use only MM:SS part of starttime
                schedTime = time.mktime(time.strptime(time.strftime('%d-%m-%Y %H:') + self._startTime.split(':', 1)[1],'%d-%m-%Y %H:%M:%S'))
            except ValueError, e:
                print "couldn't parse time, self._startTime = %s.\n Error: %s" % (self._startTime, str(e))
                self._missedSchedule = True
                schedTime = t + 3600
            addTime = 3600.0
        elif self._frequency in ('Weekly', 'Once'):
            try:
                lt = time.localtime(t)
                # Y2009 and Y2010 fix (dtimestamp was wron so the binary did not update until 2011, doh)
                # http://forums.clamwin.com/viewtopic.php?t=1988&postdays=0&postorder=asc&start=60
                year = lt.tm_year
                yday = lt.tm_yday - lt.tm_wday + self._weekDay
                if yday > 365:
                    yday = yday - 365                    
                    year = year + 1
                while yday < 1:
                    yday += 7                                
             
                    
                # use  weekday and HH:MM:SS part of starttime
                schedTime = time.mktime(time.strptime(str(yday) + ' ' + str(year) + ' ' + \
                            self._startTime, '%j %Y %H:%M:%S'))
                print 'weekly/once schedTime: ',time.asctime(time.localtime(schedTime))  
            except ValueError, e:
                print "couldn't parse time, self._startTime = %s. self._weekDay = %i\n Error: %s" % (self._startTime, self._weekDay, str(e))
                self._missedSchedule = True
                schedTime = t + 86400*7
            addTime = 3600.0*24*7
        else: #'Daily' or 'Workdays' is default
            try:
                # use HH:MM:SS part of starttime
                schedTime = time.mktime(time.strptime(time.strftime('%d-%m-%Y ') + self._startTime,'%d-%m-%Y %H:%M:%S'))
            except ValueError, e:
                self._missedSchedule = True
                schedTime = t + 86400
                print "couldn't parse time, self._startTime = %s.\n Error: %s" % (self._startTime, str(e))
            addTime = 3600.0*24

        # go to next time interval if it is out
        tmp = schedTime
        while self._AdjustDST(schedTime) < t:
            schedTime += addTime

        # move out of the weekend for workdays
        if self._frequency == 'Workdays':
            while time.localtime(self._AdjustDST(schedTime)).tm_wday in (5,6):
                schedTime += addTime
            if tmp < schedTime:
                addTime = schedTime - tmp

        #don't return for missed schedule if frequency is workdays and it is weekend now
        if self._runMissed and not self._paused and not missedAlready and \
           (self._frequency != 'Workdays' or time.localtime(t).tm_wday not in (5,6)):
            # check if we missed the scheduled run
            # and return now (+ 2 minutes) instead
            if  self._lastRun != 0 and schedTime - addTime - 1 > self._lastRun:
                print "self._lastRun=", self._lastRun
                print "schedTime=", schedTime
                print "addTime=", addTime
                t = t + 120
                print 'Schedule missed, returning: %s' % time.asctime(time.localtime(t))
                try:
                      print 'LastRun: %s' % time.asctime(time.localtime(self._lastRun))
                except:
                      pass
                self._missedSchedule = True
                return t

        schedTime = self._AdjustDST(schedTime)
        print 'Scheduling task %s  for: %s' % (self._argument, time.asctime(time.localtime(schedTime)))
        return schedTime + self._delay


    def _RunTask(self):
        # get current time
        if self._cancelling:
            return
        # set C locale, otherwise python and wxpython complain
        locale.setlocale(locale.LC_ALL, 'C')

        t = time.time()
        
        action = 'action=%s%s; when= %s' % \
                 (self._action, self._argument, time.strftime('%d-%m-%y %H:%M:%S', time.localtime(t)))

        if self._missedSchedule and not self._runMissed:
            print 'not running missed schedule label %s' % action
        else:
            if not self._paused:
                # execute the action
                print 'running task %s. Frequency is: %s\n' % (action, self._frequency)
                void = self._action(*self._argument)
                self._lastRun = t
                self._WriteLastRun()
            else:
                print 'schedule label %i is paused' % self._label

        # schedule next action
        if self._frequency != 'Once':
            self._id = self._sched.enterabs(self._CalcNextRun(self._missedSchedule), 0, self._RunTask, ())

    def _DelayFunc(self, delay):
        start = time.time()
        while not self._cancelling and int(time.time() - start) < int(delay):
            time.sleep(self._loopDelay)

    def run(self):
        self._sched.run()
        print 'Scheduler %s(%s), frequency :%s terminated' % (self._action, self._argument, self._frequency)

    def stop(self):
        try:
           self._sched.cancel(self._id)
        except:
           pass
        self._cancelling = True

    def pause(self):
        print 'pausing scheduler label %i' % self._label
        self._paused = True

    def resume(self):
        print 'resuming scheduler label %i' % self._label
        self._paused = False

if __name__ == '__main__':
    import sys
    def action():
        print 'execute'

    s = Scheduler('Workdays', '20:20:00', 5, action)
    s.start()
    while sys.stdin.read(1) != 'c':
        time.sleep(0)
    s.stop()
    s.join(1)
    print 'completed'


