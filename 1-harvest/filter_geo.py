from langid import classify
import sys
import os
import re
import json
import gzip

remove_specific_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+',re.UNICODE)
space_re=re.compile(r'\s+',re.UNICODE)

if __name__=='__main__':
  PROJECT=sys.argv[1]
  if not os.path.isfile(PROJECT+'.py'):
    sys.stderr.write('There is no configuration file '+PROJECT+'.py for project '+PROJECT+'\n')
    sys.exit(1)
  exec('from '+PROJECT+' import *')
  if os.path.exists(PROJECT+'.filter'):
    sys.stderr.write('The folder '+PROJECT+'.filter already exists. Please remove it before you proceed.\n')
    sys.exit(1)
  os.makedirs(PROJECT+'.filter')
  users={}
  num=0
  for file in os.listdir(PROJECT):
    for status in json.load(gzip.open(os.path.join(PROJECT,file))):
      num+=1
      if num%10000==0:
        print 'Read',num
      if len(COUNTRIES)>0:
        if status['place']==None:
          continue
        if status['place']['country_code'] not in COUNTRIES:
          continue
      user=status['user']['screen_name']
      if user not in users:
        users[user]=[]
      users[user].append(status)
  print 'Read all together',num
  num=0
  print 'Writing down started'
  for user in users:
    if len(LANGID_GEO)!=0:
      if classify(' '.join([space_re.sub(' ',remove_specific_re.sub(' ',status['text'])).strip() for status in users[user]]))[0] not in LANGID_GEO:
        continue
    num+=len(users[user])
    gzip.open(os.path.join(PROJECT+'.filter',user+'.gz'),'w').write(json.dumps(users[user]))
  print 'Wrote all together',num