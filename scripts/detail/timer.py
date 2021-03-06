# Copyright (C) 2015 DataSift Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import sys
import time

perf_counter_available = (sys.version_info.minor >= 3)

class Job:
  def __init__(self, job_name):
    if perf_counter_available:
      self.start = time.perf_counter()
    else:
      self.start = 0
    self.job_name = job_name
    self.stopped = False

  def stop(self):
    if self.stopped:
      sys.exit('Already stopped')
    self.stopped = True
    if perf_counter_available:
      self.total = time.perf_counter() - self.start
    else:
      self.total = 0

  def result(self):
    if not self.stopped:
      sys.exit("Stop the job before result")
    print(
        '{}: {}s'.format(self.job_name, datetime.timedelta(seconds=self.total))
    )

class Timer:
  def __init__(self):
    self.jobs = []
    self.total = Job('Total')

  def start(self, job_name):
    if job_name == 'Total':
      sys.exit('Name reserved')
    for i in self.jobs:
      if i.job_name == job_name:
        sys.exit('Job already exists: {}'.format(job_name))
    self.jobs.append(Job(job_name))

  def stop(self):
    if len(self.jobs) == 0:
      sys.exit("No jobs to stop")
    self.jobs[-1].stop()

  def result(self):
    if not perf_counter_available:
      print('timer.perf_counter is not available (update to python 3.3+)')
      return
    for i in self.jobs:
      i.result()
    print('-')
    self.total.stop()
    self.total.result()
