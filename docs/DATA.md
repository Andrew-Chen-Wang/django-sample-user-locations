# The Population Dataset

### This is the director to put your .tif.ovr file. 

### What have I done

I am VERY new to GIS; in fact, it took me 6 hours to figure out how to open the .TIF file. But I eventually opened the `GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0.tif.ovr` file in QGIS and saw that on the singleband gray render type, you can tell there are some gray hues.

Originally, I wanted different colors (like singleband pseudocolor with a magma color ramp); however, getting the shade using rasterio was good enough.

The population density based on this dataset is how I'm calculating the number of users to put into a single square.

The dataset uses the 250m resolution, Mollweide coordinate system.

### Size of Data

For the entire ZIP file's size, I ran this command in a Unix-based OS: `unzip -Zt GHS*`

Here's the output: 4 files, 541390619 bytes uncompressed, 397963186 bytes compressed:  26.5%
