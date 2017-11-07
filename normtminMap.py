#!/Users/belcher/anaconda2/bin/python

import matplotlib as mpl
mpl.use('Agg')
import os, datetime, sys, shapefile, glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.font_manager as font_manager
from PIL import Image
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def divlookup(dfile, division, month):
	'''
	Function divlookup: pulls division data from CMB data (i.e., text file)
	'''
	cmd = 'grep ^'+division+'280009 '+dfile
	#print cmd
	dval = os.popen(cmd)
	dval = float(dval.read().split()[month])
	#print division
	return dval
	

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


dfile = glob.glob('./Data/*tmindv*')
dfile = dfile[0]


path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
	figxsize = 8.62
	figysize = 5.56
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 566
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_620_BaseLayer.png'
	line_img = './CONUS_620_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"

if(imgsize == '1000'):
	figxsize = 13.89
	figysize = 8.89
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_1000_BaseLayer.png'
	line_img = './CONUS_1000_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"

if(imgsize == 'DIY'):
	figxsize = 13.655
	figysize = 8.745
	figdpi = 300
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_DIY_BaseLayer.png'
	line_img = './CONUS_DIY_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"

if(imgsize == 'HD'):
	figxsize = 21.33
	figysize = 10.25
	figdpi = 72
	lllon, lllat, urlon, urlat = [-126.95182, 19.66787, -52.88712, 46.33016]
	logo_image = './noaa_logo_100.png'
	logo_x = 1421
	logo_y = 35
	framestat = 'True'
	base_img = './CONUS_HD_BaseLayer.png'
	line_img = './CONUS_HD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'
	cmask = "./Custom_HD_mask.png"

if(imgsize == 'HDSD'):
	figxsize = 16
	figysize = 9.75
	figdpi = 72
	lllon, lllat, urlon, urlat = [-120.8000, 19.5105, -57.9105, 48.9905]
	logo_image = './noaa_logo_100.png'
	logo_x = 1037
	logo_y = 35
	framestat = 'True'
	base_img = './CONUS_HDSD_BaseLayer.png'
	line_img = './CONUS_HDSD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'
	cmask = "./Custom_HDSD_mask.png"


fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=framestat)#, axisbg=bgcol)
ax1.spines['left'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)

# Create Map and Projection Coordinates
kwargs = {'epsg' : 5070,
          'resolution' : 'i',
          'llcrnrlon' : lllon,
          'llcrnrlat' : lllat,
          'urcrnrlon' : urlon,
          'urcrnrlat' : urlat,
          'lon_0' : -96.,
          'lat_0' : 23.,
          'lat_1' : 29.5,
          'lat_2' : 45.5,
		  'area_thresh' : 15000,
		  'ax' : ax1,
		  'fix_aspect' : False
}

#Set up the Basemap
m =Basemap(**kwargs)


#Add the BaseLayer image 1st pass
outline_im = Image.open(base_img)
m.imshow(outline_im, origin='upper', aspect='auto')


cdict1 = gmtColormap('./CPT/temperature_0-100.cpt')
valmax = 100.
valmin = 0.
cwidth = valmax - valmin #used to determine where a given data value lies in the span of the color ramp (0-100=100, 20-80=60 and so on)
cmap_temp = LinearSegmentedColormap('cmap_temp', cdict1)

if(mm != '00'):
	#Now read in the Climate Division Shapes and fill the basemap 
	r = shapefile.Reader(r"./Shapefiles/GIS_OFFICIAL_CLIM_DIVISIONS")
	shapes = r.shapes()
	records = r.records()

	for record, shape in zip(records,shapes):
	    lons,lats = zip(*shape.points)
	    data = np.array(m(lons, lats)).T
	 
	    if len(shape.parts) == 1:
	        segs = [data,]
	    else:
	        segs = []
	        for i in range(1,len(shape.parts)):
	            index = shape.parts[i-1]
	            index2 = shape.parts[i]
	            segs.append(data[index:index2])
	        segs.append(data[index2:])
	 
	    lines = LineCollection(segs,antialiaseds=(1,))
	    #Now obtain the data in a given poly and assign a color to the value
	    div = str(record[5])
	    if(len(div) < 4): div = '0'+div
	    dval = divlookup(dfile,div,int(mm))
	    #if(dval > valmax): dval = valmax - 0.1
	    lines.set_facecolors(cmap_temp([dval/cwidth]))
	    lines.set_edgecolors(cmap_temp([dval/cwidth]))
	    lines.set_linewidth(0.25)
	    ax1.add_collection(lines)


#Add the custom mask
omask_im = Image.open(cmask)
m.imshow(omask_im, origin='upper', alpha=1., zorder=10, aspect='auto', interpolation='nearest')

#Add the Line image
outline_im = Image.open(line_img)
m.imshow(outline_im, origin='upper', alpha=0.75, zorder=10, aspect='auto')


#Add the NOAA logo (except for DIY)
if(imgsize != 'DIY'):
	logo_im = Image.open(logo_image)
	height = logo_im.size[1]
	# We need a float array between 0-1, rather than
	# a uint8 array between 0-255 for the logo
	logo_im = np.array(logo_im).astype(np.float) / 255
	fig.figimage(logo_im, logo_x, logo_y, zorder=10)



outpng = "temporary_map.png"

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.00)

if(imgsize == 'HD' or imgsize =='HDSD'):
	plt.savefig(outpng, dpi=figdpi, orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)


