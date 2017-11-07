#!/Users/belcher/anaconda2/bin/python


import os, datetime, sys, subprocess

#isz = ['620', '1000', 'DIY', 'HD', 'HDSD']
isz = ['620', '1000']
mons = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for i in xrange(len(mons)):
	for j in xrange(len(isz)):
		cmd = '/Users/belcher/anaconda2/bin/python normtmaxDriver.py '+mons[i]+' '+isz[j]
		subprocess.call(cmd, shell=True)

for i in xrange(len(mons)):
	for j in xrange(len(isz)):
		cmd = '/Users/belcher/anaconda2/bin/python normtminDriver.py '+mons[i]+' '+isz[j]
		subprocess.call(cmd, shell=True)

for i in xrange(len(mons)):
	for j in xrange(len(isz)):
		cmd = '/Users/belcher/anaconda2/bin/python normtavgDriver.py '+mons[i]+' '+isz[j]
		subprocess.call(cmd, shell=True)
		
for i in xrange(len(mons)):
	for j in xrange(len(isz)):
		cmd = '/Users/belcher/anaconda2/bin/python normprecipDriver.py '+mons[i]+' '+isz[j]
		subprocess.call(cmd, shell=True)