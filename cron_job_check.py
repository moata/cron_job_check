#!/usr/bin/env python

#Author : Moatasem.Abdalmahdi
#Date   : 2013-12-12
#Nagios plugin :  Check cron job 



import sys,getopt,os,time,stat

MODE = 'r'

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3



def usges():
  print 'cron_job_check\n'\
  'Verion 1.0\n' \
  '--------------------------------------------\n'\
  'cron_job_check.py This script allows you to check cron job whether running or not .\n'\
  'you simmply pass the path of cron job log file , and threshold of modification time in minute/second.\n'\
  '\n'\
  'usage : \n'\
  '---------------------------------------------\n'\
  '-t <time_in_second>\n'\
  '-f <path to cron job log file>\n'\
  'example : ./cron_job_check -f /va/log/test.log -t 0.30\n'


def pares_option():
  try:
    opts , args = getopt.getopt(sys.argv[1:],'f:t:h',["file=","time=","help"])
  except getopt.GetoptError as err:
    print str(err)
    usges()
    sys.exit(EXIT_CRITICAL)
  return opts

def file_accessible(f,mode):
  try:
    fh = open(f,mode)
  except IOError as e:
    print str(e)
    sys.exit(EXIT_CRITICAL)
    
  return fh
     
     

def check_file_time(f,t):
  t_check = round(((time.time() - os.stat(f)[stat.ST_MTIME])/60),2)
  if float(t_check) < float(t):
    print 'ERROR: %s last modified %s , threshold set to %s'%(f,t_check,t)
    sys.exit(EXIT_CRITICAL)


if __name__ == '__main__':
  t = None
  f = None
  status = 2
  msg    = 'cron job not running ! '
  
  opts = pares_option()
  for opt,arg in opts:  
    if opt in ('-f','--file'):
      f = arg
    elif opt in ('-t','--time'):
      t = arg
    elif opt in ('-h','--help'):
      usges()
      sys.exit(EXIT_OK)
    else:
       raise False ,"unhandled option"
  
  if not t and f:
    usges()
    sys.exit(EXIT_CRITICAL)
  
  fh = file_accessible(f,MODE)
  check_file_time(f,t)
  for line in fh.readlines():
    if line.replace('\n','') == "Exit code:0":
      msg = 'cron job currently running'
      status = 0
    
  print msg
  sys.exit(status)
  
  
    
    






