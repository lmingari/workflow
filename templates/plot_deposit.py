import numpy as np
import xarray as xr
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from os.path import join
import warnings

##############################################
###
### Parameters
###
minval          = 0.01
key             = "tephra_grn_load"
basepath        = "$basepath"
fname           = "$resfile"
levels          = [0, 0.1, 0.2, 0.4, 0.8, 1.0, 1.2, 1.4, 1.8, 2]
label           = r"Deposit mass load in $kg/m^2$"
cmap            = plt.cm.RdYlBu_r
###############################################

### General configuration
warnings.filterwarnings("ignore", category=DeprecationWarning)
plt.rcParams.update({'font.size': 9,'lines.markersize': 3})

###
### Set mininmum level
###
if minval>0: levels[0] = minval

###
### Read file
###
ds = xr.open_dataset(fname)

###
### Generate map
###
proj = crs.PlateCarree()
fig, ax = plt.subplots( subplot_kw={'projection': proj} )

###
### Add map features
###
BORDERS = cfeature.NaturalEarthFeature(
        scale     = '10m',
        category  = 'cultural',
        name      = 'admin_0_countries',
        edgecolor = 'gray',
        facecolor = 'none'
        )
LAND = cfeature.NaturalEarthFeature(
        'physical', 'land', '10m',
        edgecolor = 'none',
        facecolor = 'lightgrey',
        alpha     = 0.8
        )

ax.add_feature(LAND,zorder=0)
ax.add_feature(BORDERS, linewidth=0.4)

###
### Add shapefiles
###
geo = Reader(join(basepath,'shapefiles/estados.shp')).geometries()
ax.add_geometries(geo, 
                  crs.PlateCarree(),
                  facecolor='none',
		  edgecolor='gray',
                  linewidth = 0.4,
                  )

###
### Add grid lines
###
gl = ax.gridlines(
    crs         = crs.PlateCarree(),
    draw_labels = True,
    linewidth   = 0.5,
    color       = 'gray',
    alpha       = 0.5,
    linestyle   = '--')
gl.top_labels    = False
gl.right_labels  = False
gl.ylabel_style  = {'rotation': 90}

###
### Add locations
###
df = pd.read_csv('locations.csv')
ax.scatter(df.loc[df['type']=='Volcan'].lon,
           df.loc[df['type']=='Volcan'].lat,
           color  = 'r',
	   marker = '^', 
           alpha  = 0.7)
ax.scatter(df.loc[df['type']=='Ciudad'].lon,
           df.loc[df['type']=='Ciudad'].lat,
           color  = 'k',
	   marker = 'o',
           alpha  = 0.7)
ax.scatter(df.loc[df['type']=='Aeropuerto'].lon,
           df.loc[df['type']=='Aeropuerto'].lat,
           color  = 'g',
	   marker = 's',
           alpha  = 0.7)

for lat,lon,name,stype in zip(df.lat,df.lon,df.name,df.type):
        if stype=='Ciudad': 
	        ax.text(
                   lon+0.05,
                   lat-0.05,
                   name,
                   fontsize=6,
                   ha='left',
                   va='top')

###
### Plot contours
###
it = -1
time_fmt = ds.isel(time=it)['time'].dt.strftime("%d/%m/%Y %H:%M").item()
ax.set_title(time_fmt, loc='right')
ax.set_title(label, loc='left')
fc = ax.contourf(
    ds.lon,ds.lat,ds.isel(time=it)[key],
    levels    = levels,
    norm      = BoundaryNorm(levels,cmap.N),
    cmap      = cmap,
    extend    = 'max',
    zorder    = 0,
    transform = crs.PlateCarree()
    )

###
### Generate colorbar
###
cbar=fig.colorbar(fc,
    orientation = 'vertical',
    ax          = ax,
    )

###
### Output plot
###
fname_plt = f"deposit.png"
plt.savefig(fname_plt,dpi=200,bbox_inches='tight')
