# rgb-from-geotiff
This code converts RGB geotiff into the UV3 file format. The most important is that the file input file must be georreferenced, as geotiff, and it must contain the three RGB bands (Red, Blue and Green). The reading is done through GDAL, and it is pretty quick for converting even big files. 

## Usage

Open the terminal where this code was cloned or downloaded (with cd path/to/directory) and use:

```
$ python 3 rgb-from-geotiff -i /home/user/path/to/geotiff.tif -o /home/user/path/to/output.uv3
```


