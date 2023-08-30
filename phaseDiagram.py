# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 13:26:56 2022

@author: Frank
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('PhaseDiagramData2.csv')
shade = 1 #fill is opaque when =1 
degree = 2 # degree of polynomial fit.
samples = 50 #number of points to sample each curve at
axisMin , axisMax = 0.96, 1.04

#plot raw data points, visible iff 0<=shade<1
fig1, ax1 = plt.subplots()
ax1.scatter(data.Z0x,data.Z0y,25, color='blue', label='$Z_4$=0')
ax1.scatter(data.Z1x,data.Z1y,25, color='red', label='$Z_4$=1')
ax1.scatter(data.Z2x,data.Z2y,25, color='cyan', label='$Z_4$=2')
ax1.scatter(data.Z3x,data.Z3y,25, color='green',label='$Z_4$=3')


#data.Crit contains critical points at transitions b/w distinct phases.
#For each border, we fit a polynomial to its crit. points
#later we'll use these curves as boundaries for fill region.

#define curve demarcating green region from red and cyan
greenX = data.Critx[0:3]
greenY = data.Crity[0:3]
greenCurveFnc = np.poly1d(np.polyfit(greenX, greenY, degree))
greenCurveX = np.linspace(min(greenX), max(greenX), samples)
greenCurveY = greenCurveFnc(greenCurveX) 

#define curve demarcating red and cyan
redX = data.Critx[2:8]
redY = data.Crity[2:8]
redFnc = np.poly1d(np.polyfit(redY,redX,5))
redCurveX = np.linspace(min(redY),max(redY),samples)
redCurveY = redFnc(redCurveX)


#define curve demarcating blue from red.
#For both the green and red curves, we later have to reflect them about y=x and
#treat these as two separate boundaries for the fill region
#But here that's not necessary, so we'll concatenate these critical points
#with their reflection about y=x
blueX = pd.concat([data.Critx[8:12], data.Crity[8:12]], ignore_index=True)
blueY = pd.concat([data.Crity[8:12], data.Critx[8:12]], ignore_index=True)
blueFnc = np.poly1d(np.polyfit(blueX,blueY,degree))
blueCurveX = np.linspace(min(blueX), max(blueX),samples)
blueCurveY = blueFnc(blueCurveX)



#make a small line perpendicular to y=x , at the border of red and green
#so as to give the border between these two regions some small finite distance
pt1 = max(greenCurveY)
pt2 = max(greenCurveX)
line = np.linspace(pt1,pt2, samples)
#the reflection of our previously defined green curve over y=x
greenCurveFnc_b = np.poly1d(np.polyfit(greenY, greenX, degree))
fncOfLine = greenCurveFnc_b(line)
plt.fill_between(line,fncOfLine,axisMax,color='red',interpolate=True)
#plt.fill_between(line, fncOfLine,line[::-1],color='green',interpolate=True)



#fill in red region. ALL area above bottom red curve is red, including some
#which should be cyan and some blue. this area will be overwritten soon
plt.fill_between(redCurveX, redCurveY, axisMax, color='red', alpha=shade, interpolate=True)

#make top right blue
plt.fill_between(blueCurveX, blueCurveY,max(blueCurveY), where=blueCurveY<=max(blueCurveY),color='b',alpha=shade)

#fill below top green curve ALL as green
plt.fill_between(greenCurveX, greenCurveY,min(greenCurveX),color='green',interpolate=True)

#fill below bottom green curve as cyan, overwriting previous.
plt.fill_between(greenCurveY, greenCurveX, min(greenCurveX), color='cyan', alpha=shade, interpolate=True)


#below red is cyan
plt.fill_between(redCurveX, redCurveY, axisMin, color='cyan', alpha=shade, interpolate=True)

#left of red is cyan:
plt.fill_between(redCurveY, redCurveX, axisMax, color='cyan', alpha=shade, interpolate=True)

#above green is cyan
plt.fill_between(greenCurveX, greenCurveY, axisMax, color='cyan', alpha=shade, interpolate=True)


plt.title('$c=c_0$',fontsize=14)
plt.legend(loc='upper left')
plt.xlabel('Strain ($b / b_0$)',fontsize=14)
plt.ylabel('Strain ($a / a_0$)',fontsize=14)
ax1 = plt.gca()
ax1.set_aspect('equal', adjustable='box')
plt.xlim(axisMin,axisMax)
plt.ylim(axisMin,axisMax)
plt.xticks(np.arange(axisMin, axisMax, 0.02))
plt.yticks(np.arange(axisMin, axisMax, 0.02))
ax1.tick_params(direction='out')
plt.savefig('Fig5A.pdf')

#Second figure, containing just the raw data
fig2, ax2 = plt.subplots()
ax2.scatter(data.Z0x,data.Z0y,25, color='blue', label='$Z_4$=0')
ax2.scatter(data.Z1x,data.Z1y,25, color='red', label='$Z_4$=1')
ax2.scatter(data.Z2x,data.Z2y,25, color='cyan', label='$Z_4$=2')
ax2.scatter(data.Z3x,data.Z3y,25, color='green',label='$Z_4$=3')
ax2.scatter(data.Critx,data.Crity,25, color='black',label='Crit pt.')
#slightly bigger axis limits for raw data points
# data accumulated before determining the pressure
#required to achieve strain <0.96 or >1.04 is unreasonably high
plt.xlim(axisMin-0.025,axisMax+0.025) 
plt.ylim(axisMin-0.025,axisMax+0.025) 
ax2.set_aspect('equal', adjustable='box')
plt.title('Raw Data Points',fontsize=14)
plt.legend(loc='lower right')
plt.xlabel('Strain ($b / b_0$)',fontsize=14)
plt.ylabel('Strain ($a / a_0$)',fontsize=14)

