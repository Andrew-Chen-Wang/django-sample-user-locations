# Django: Sample Location Build

By: Andrew Chen Wang

If you need a sample data set of users in locations to test your location-based app, this Django sample can help.

### Setup

1. Clone or download this repository.
2. Go to https://ghsl.jrc.ec.europa.eu/download.php?ds=pop and download the entire dataset in one file (below the map).
3. Unzip the file and copy the `.tif.ovr` file into the root directory here.
    - Help!: The root directory has the Dockerfile.
4. You must have Docker and docker-compose to execute the following commands to start: `docker-compose up --build`
    - Help!: You must be in the terminal and in the root directory

A superuser is automatically created with username `test` and password `test`

### Configuration

To use a different GHS-POP dataset, go into the Dockerfile and change the `GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0.tif.ovr` to your file name. You may have to play around with `public/utils.py`.

Population density: Go to the `settings.py` and change the variable `density` to decrease the number of users to generate.

### What did I do?

I've simply added a bunch of users to a custom User model. They have funny names, but, most importantly, their locations are now stored in the database.

These locations are generated based on population density. They are scattered around within towns, as well, so that they aren't all in one location.

The way I've done this is by using rasterio's colormap, or lack thereof. I actually used the shading from the `.tif.ovr` file from the GHS-POP dataset to calculate density.

### Credits

All data comes from: https://ghsl.jrc.ec.europa.eu/download.php (uncompressed size is 541.390619 megabytes). 
- If you want to double check this number and if you're on Linux or MacOS, clone or download this repository and run `unzip -Zt GHS_BUILT_LDS2014_GLOBE_R2018A_54009_250_V2_0.zip` wherever the ZIP file lives.
- Their guide: https://ghsl.jrc.ec.europa.eu/documents/GHSL_Data_Package_2019.pdf?t=1478q532234372

Found the data through: https://luminocity3d.org/WorldPopDen/ which is an interactive map of the population densities.

Here is the blog post that went along with that interactive map: https://citygeographics.org/2016/12/26/global-urban-constellations/

Some of the Docker configuration comes from [cookiecutter-django](https://github.com/pydanny/cookiecutter-django).

### Citation

I'm using the [GHS-POP](https://ghsl.jrc.ec.europa.eu/data.php?sl=3) dataset:
```
Dataset:

Schiavina, Marcello; Freire, Sergio; MacManus, Kytt (2019): GHS population grid multitemporal (1975-1990- 2000-2015), R2019A. European Commission, Joint Research Centre (JRC) [Dataset] doi:10.2905/0C6B9751- A71F-4062-830B-43C9F432370F PID: http://data.europa.eu/89h/0c6b9751-a71f-4062-830b-43c9f432370f

Concept & Methodology:

Freire, Sergio; MacManus, Kytt; Pesaresi, Martino; Doxsey-Whitfield, Erin; Mills, Jane (2016): Development of new open and free multi-temporal global population grids at 250 m resolution. Geospatial Data in a Changing World; Association of Geographic Information Laboratories in Europe (AGILE). AGILE 2016.
```

To open the dataset (since most of us have never used it, including me), we need to have a GIS. I'm using QGIS [brought to me from here.](http://www.statsmapsnpix.com/2016/10/the-global-human-settlement-layer.html)

### FAQ

- Exit code 137 simply means you need to increase the amount of memory to run since this copies the entire `.tif.ovr` dataset. You can adjust by executing `docker stats`
    - I had to use 11 GB (peaking at 10.3 GB)
    - I recommend you do close any other program. Once the migration is finished, this issue will never pop up again since the data is now in your Postgres db.
- Memory allocation is a HUGE problem. If you have to re-run the containers to complete the migration (in case of an error like the one above), delete the containers since rasterio will increase the size of the `.tif.ovr` file to 10+ GB (every time you access it).
    
### TODO
- Admin does not show user location
- Show all users' locations
- Memory allocation is exceeding beyond limits