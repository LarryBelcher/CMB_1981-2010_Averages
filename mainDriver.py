#!/usr/bin/python


import os, datetime, sys, subprocess

isz = ['620', '1000', 'DIY', 'HD', 'HDSD']
mons = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for i in xrange(len(mons)):
	for j in xrange(len(isz)):
		cmd = 'python normtavgDriver.py '+mons[i]+' '+isz[j]
		subprocess.call(cmd, shell=True)


for i in xrange(len(mons)):
	for j in xrange(len(isz)):
		cmd = 'python normprecipDriver.py '+mons[i]+' '+isz[j]
		subprocess.call(cmd, shell=True)