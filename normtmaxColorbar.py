#!/Users/belcher/anaconda2/bin/python

import matplotlib as mpl
mpl.use('Agg')
import os, datetime, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.font_manager as font_manager
from PIL import Image
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def gmtColormap(fileName):

      import colorsys
      import numpy as N
      try:
          f = open(fileName)
      except:
          print "file ",fileName, "not found"
          return None

      lines = f.readlines()
      f.close()

      x = []
      r = []
      g = []
      b = []
      colorModel = "RGB"
      for l in lines:
          ls = l.split()
          if l[0] == "#":
             if ls[-1] == "HSV":
                 colorModel = "HSV"
                 continue
             else:
                 continue
          if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
             pass
          else:
              x.append(float(ls[0]))
              r.append(float(ls[1]))
              g.append(float(ls[2]))
              b.append(float(ls[3]))
              xtemp = float(ls[4])
              rtemp = float(ls[5])
              gtemp = float(ls[6])
              btemp = float(ls[7])

      x.append(xtemp)
      r.append(rtemp)
      g.append(gtemp)
      b.append(btemp)

      nTable = len(r)
      x = N.array( x , N.float32)
      r = N.array( r , N.float32)
      g = N.array( g , N.float32)
      b = N.array( b , N.float32)
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "RGB":
          r = r/255.
          g = g/255.
          b = b/255.
      xNorm = (x - x[0])/(x[-1] - x[0])

      red = []
      blue = []
      green = []
      for i in range(len(x)):
          red.append([xNorm[i],r[i],r[i]])
          green.append([xNorm[i],g[i],g[i]])
          blue.append([xNorm[i],b[i],b[i]])
      colorDict = {"red":red, "green":green, "blue":blue}
      return (colorDict)

def int2str(mm):
	if(mm == '00'): ms = 'No Data'
	if(mm == '01'): ms = 'January'
	if(mm == '02'): ms = 'February'
	if(mm == '03'): ms = 'March'
	if(mm == '04'): ms = 'April'
	if(mm == '05'): ms = 'May'
	if(mm == '06'): ms = 'June'
	if(mm == '07'): ms = 'July'
	if(mm == '08'): ms = 'August'
	if(mm == '09'): ms = 'September'
	if(mm == '10'): ms = 'October'
	if(mm == '11'): ms = 'November'
	if(mm == '12'): ms = 'December'
	return ms

mm = sys.argv[1]   #(expects format like: 01)
monthstr = int2str(mm)
labeldate = monthstr

imgsize = sys.argv[2]   #(expects 620, 1000, DIY, HD, or HDSD)

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
	figxsize = 8.62
	figysize = 0.695
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.2258; cbw = 0.5463; cby = 0.33; cbh = 0.259
	t1x = 0.343; t1y = 0.68
	t2x = 0.630; t2y = 0.678
	t3x = 0.006; t3y = 0.77
	t4x = 0.899; t4y = 0.77
	t5x = 0.904; t5y = 0.55
	pngfile = "temporary_cbar.png"

if(imgsize == '1000'):
	figxsize = 13.89
	figysize = 0.695
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.33; cbw = 0.339; cby = 0.33; cbh = 0.259
	t1x = 0.398; t1y = 0.68
	t2x = 0.578; t2y = 0.678
	t3x = 0.004; t3y = 0.77
	t4x = 0.938; t4y = 0.77
	t5x = 0.941; t5y = 0.55
	pngfile = "temporary_cbar.png"

if(imgsize == 'DIY'):
	figxsize = 8.89
	figysize = 2.44
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.185; cbw = 0.63; cby = 0.38; cbh = 0.1
	t1x = 0.295; t1y = 0.68
	t2x = 0.578; t2y = 0.678
	t3x = 0.05; t3y = 0.82
	t4x = 0.85; t4y = 0.82
	t5x = 0.852; t5y = 0.73
	pngfile = "temporary_cbar.eps"

if(imgsize == 'HD' or imgsize == 'HDSD'):
	figxsize = 13.5
	figysize = 0.69
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.0; cbw = 1.0; cby = 0.01; cbh = 0.99
	t1x = 0.33; t1y = 0.565
	t2x = 0.69; t2y = 0.565
	t3x = 0.05; t3y = 0.82
	t4x = 0.85; t4y = 0.82
	t5x = 0.86; t5y = 0.63
	pngfile = "temporary_cbar.png"

fig = plt.figure(figsize=(figxsize,figysize))

# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0,0.0,1.0,1.0], axisbg='#F5F5F5')
ax1.set_frame_on(False)
ax1.set_xticks([])
ax1.set_xticklabels([])
ax1.set_yticks([])
ax1.set_yticklabels([])


if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	dval = "Average maximum temperature"
	plt.text(t1x, t1y, dval, fontproperties=propb, size=fsiz1, color='#333333')
	plt.text(t2x, t2y, '($^\circ$F)', fontproperties=propr, size=fsiz1, color='#333333')
	plt.text(t3x, t3y-0.2, '1981-2010 Average', fontproperties=propr, size=fsiz2-1, color='#8D8D8D')
	#plt.text(t3x, t3y-0.4, 'Climate Normals', fontproperties=propr, size=fsiz2-1, color='#8D8D8D')
	plt.text(t3x, t3y, labeldate, fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t4x, t4y, 'Climate.gov', fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t5x, t5y, 'Data: NCEI', fontproperties=propr, size=fsiz2, color='#8D8D8D')

cdict1 = gmtColormap('./CPT/temperature_0-100.cpt')
cmap = LinearSegmentedColormap('cmap_temp', cdict1)
levs = np.asarray([0, 50, 100])
norm = colors.Normalize(levs[0], levs[-1])
#norm = mpl.colors.BoundaryNorm(levs, cmap.N)
ax2 = fig.add_axes([cbx,cby,cbw,cbh], axisbg='#F5F5F5')
ax2.set_frame_on(False)
ax2.set_xticks([])
ax2.set_xticklabels([])
ax2.set_yticks([])
ax2.set_yticklabels([])

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	barticks = levs
	barlevs = levs
	bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	if(imgsize == 'DIY'):
		bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
		bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	bar.outline.set_visible(True)
	bar.outline.set_linewidth(0.6)
	bar.ax.tick_params(size=0.01)
	bar.ax.set_xticklabels(barlevs, fontproperties=propr, size=fsiz2, va='top')

if(imgsize == 'HD' or imgsize == 'HDSD'):
	barticks = levs
	barlevs = ['', '', '']
	bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	bar.outline.set_visible(True)
	bar.outline.set_linewidth(0.6)
	bar.ax.tick_params(size=0.01)
	bar.ax.set_xticklabels(barlevs, fontproperties=propr, size=fsiz2, va='top')

if(imgsize != 'DIY'):
	plt.savefig(pngfile, dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.0)

if(imgsize == 'DIY'):
	plt.savefig(pngfile, dpi=figdpi, orientation='portrait', bbox_inches='tight', pad_inches=0.0)