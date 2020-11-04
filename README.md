# Overview

This code converts RGB geotiff into the UV3 file format. The most important is that the file input file must be georreferenced, as geotiff, and it must contain the three RGB bands (Red, Green and Blue). The reading is done through GDAL, and it is pretty quick for converting even big files. 

## rgb-from-geotiff

Open the terminal where this code was cloned or downloaded (with cd path/to/directory) and use:

```
$ python3 rgb-from-geotiff.py -i /home/user/path/to/geotiff.tif -o /home/user/path/to/output.uv3
```
# Copyright and License

**rgb-from-geotiff** - Nils Hamel, Huriel Reichel <br >

# Copyright and License
Copyright (c) 2020 Republic and Canton of Geneva

This program is licensed under the terms of the GNU GPLv3. Documentation and illustrations are licensed under the terms of the CC BY-NC-SA.

