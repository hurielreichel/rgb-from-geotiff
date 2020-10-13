#!/usr/bin/env python3
#  rgb-from-geotiff
#
#     Nils Hamel - nils.hamel@bluewin.ch
#     Huriel Reichel - huriel.ruan@gmail.com
#     Copyright (c) 2020 STDL, Swiss Territorial Data Lab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on Fri Oct  9 10:08:28 2020

@author: huriel
"""
from osgeo import gdal
from struct import *
from progress.bar import ShadyBar

import argparse
import math
import sys
import os
import glob
import numpy as np
import progress

def pm_assign_rgb( pm_input, pm_output, pm_raster_r, pm_raster_g, pm_raster_b, pm_x, pm_y, pm_pw, pm_ph, pm_nodata, pm_w, pm_h):
    
             # create output stream #
       with open( pm_output, mode='wb' ) as uv3:

          # compute raster position #
          for x in range(pm_width):
              for y in range(pm_height):
                  pm_r = pm_raster_r[y][x]
                  pm_g = pm_raster_g[y][x]
                  pm_b = pm_raster_b[y][x]
                  pm_rx = ( ( x * pm_pw ) + pm_x ) * ( math.pi/180 )
                  pm_ry = ( pm_y - ( y * pm_ph ) ) * ( math.pi/180 )
                  pm_buffer = pack( '<dddBBBB', pm_rx, pm_ry, 0, 1, pm_r, pm_g, pm_b )
                  uv3.write( pm_buffer )
                  #print( pm_rx, pm_ry, 0, 1, pm_r, pm_g, pm_b ) # in chase you want to print results as the former Octave code

#
#   source - main function
#

# create argument parser #
pm_argparse = argparse.ArgumentParser()

# argument and parameter directive #
pm_argparse.add_argument( '-i', '--input', type=str  , help='geotiff path'    )
pm_argparse.add_argument( '-o', '--output' , type=str  , help='uv3 output path' )

# read argument and parameters #
pm_args = pm_argparse.parse_args()

# GDAL configuration #
gdal.UseExceptions()

# GDAL open geotiff file #
pm_geotiff = gdal.Open( pm_args.input )
#pm_geotiff = gdal.Open( pm_input ) #in chase of working inside a GUI

# retrieve raster data #
pm_band_r = pm_geotiff.GetRasterBand(1)
pm_band_g = pm_geotiff.GetRasterBand(2)
pm_band_b = pm_geotiff.GetRasterBand(3)

# retrieve raster no data value #
pm_nodata = pm_band_r.GetNoDataValue()

# extract raster resolution #
pm_width = pm_geotiff.RasterXSize
pm_height = pm_geotiff.RasterYSize

# retrieve raster transformation #
pm_gtrans = pm_geotiff.GetGeoTransform()

# retrieve raster geographic parameters #
pm_x = pm_gtrans[0] # origin x #
pm_y = pm_gtrans[3] # origin y #
pm_pw = pm_gtrans[1] # pixel width #
pm_ph = -pm_gtrans[5] # pixel height #

# format raster pm_raster
pm_raster_r = pm_band_r.ReadAsArray( 0, 0, pm_width, pm_height )
pm_raster_g = pm_band_g.ReadAsArray( 0, 0, pm_width, pm_height )
pm_raster_b = pm_band_b.ReadAsArray( 0, 0, pm_width, pm_height ) 
pm_raster = np.array([[pm_raster_r], [pm_raster_g], [pm_raster_b]])

# check no data value #
if pm_nodata is not None:   

    # replace no data value #
    pm_raster = np.where( pm_raster == int( pm_nodata), int( 0 ), pm_raster )

# display message #
print( 'Processing file : ' + os.path.basename( pm_args.input ) + '...' )

# process file #
bar = ShadyBar('Processing', max=100)
for i in range(100):
    pm_assign_rgb( pm_args.input, pm_args.output, pm_raster_r, pm_raster_g, pm_raster_b, pm_x, pm_y, pm_pw, pm_ph, pm_nodata, pm_width, pm_height )
    bar.next()
bar.finish()


# exit script #
sys.exit( 'Done' )
