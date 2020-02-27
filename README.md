# Django: Sample Location Build

By: Andrew Chen Wang

If you need a sample data set of users in locations to test your location-based app, this Django sample can help.

If you just need a pre-populated database of users with locations based on real-world population density, then follow the below instructions and use Docker to backup the Postgres data.

Note: Populating the database takes an extremely long time on my Raspberry Pi while my MacBook Air is most likely dying. Either interval 0,11 has an issue or it's really taking a long time. Either way, I only use this repository to get started with PostGIS now. Based on docker stats, the process does seem like it's working. Since I'm using a remote machine (RPi 3B+), it's taking awhile; however, the memory and CPU usage does fluctuate well enough to prompt me to believe it does work. I'm leaving my Pi to run for awhile and will archive if this does, in fact, not work. ~ 2020-02-27 Andrew C. Wang

Besides that, this is basically a repository with an already setup Docker-compose + Django + PostGIS stack.

Table of Contents:
- Setup
- Configuration/Settings
- Running on remote machine then restoring db on work machine
- What did I do?
- Credits
- Citation
- TODO

### Setup

I recommend you do this with a remote machine (below this section) instead of doing this on your personal machine. (I used a Raspberry Pi).

1. Clone or download this repository.
2. You must have Docker and docker-compose to execute the following commands to start: `docker-compose up --build`
    - Help!: You must be in the terminal and in the root directory
3. The following is only if you want to use the Django admin (localhost:8000/admin): In your preferred browser, you will need to Disable Cross-Origin Restrictions (seems like a JS error-doodle).
    - Reference: https://stackoverflow.com/questions/9310112/why-am-i-seeing-an-origin-is-not-allowed-by-access-control-allow-origin-error

A superuser is automatically created with username `test` and password `test`

### Configuration/Settings

Population density: Go to the `settings.py` and change the variable `NUM_OF_USERS` to decrease the number of users to generate.

### Running on remote machine then restoring db on work machine

My MacBook Air was going to die, so I decided to do this on a Raspberry Pi. Follow these steps (should be similar for Windows; look up PuTTY or Windows SSH to better understand the following steps):

1. Turn on your other machine. In my case, the Pi was to be connected on the same WiFi network. This may not be the case if you're using an EC2 instance (definitely not needed).
    - Again, make sure Docker and D.Compose is installed. On Pi, you can use this: https://dev.to/zuidwijk/comment/ke9l
    - If you've just installed Docker, make sure you logout then login or reboot (sudo reboot for pi)
2. Move this code to your machine. In my case, being in the terminal of my work machine and in the root directory (where this README lives), it was `rsync -a ./ pi@raspberrypi.local:~/my/code/dir` 
    - Your code will live in dir. This will not create a new directory.
    - `pi` is the username and `raspberrypi` is the hostname
3. Run `docker-compose -f pi-compose.yml up --build` on the remote machine
    - I ran this detached since this took a long time: `docker-compose -f pi-compose.yml up -d --build && docker container ls -a && docker logs <CONTAINER ID OF location_testing_django>`
4. Then run `docker exec -t location_testing_django_postgres pg_dumpall -c -U postgres > ~/dump_location_user_sample.sql`
    - Here's the size of the SQL dump:
5. Now to transfer that database back to the local machine. On your WORK machine: `rsync pi@raspberrypi.local:~/dump_location_user_sample.sql ~/dump_location_user_sample.sql`
    - Delete the .sql file on your remote machine by doing `rm ~/dump_location_user_sample.sql`
6. On your work machine, run `docker exec -i location_testing_django_postgres psql -U postgres location_django < ~/dump_location_user_sample.sql`
    - Delete the .sql file since it's now backed up: `rm ~/dump_location_user_sample.sql`
7. Finally, run the Docker container on your work machine: `docker-compose up`

### What did I do?

I've simply added a bunch of users to a custom User model. They have funny names, but, most importantly, their locations are now stored in the database.

These locations are generated based on population density. They are scattered around within towns, as well, so that they aren't all in one location.

The way I've done this is by using rasterio's colormap, or lack thereof. I actually used the shading from the `.tif` file from the GHS-POP dataset's tiles to calculate density.

### Credits

All data comes from: https://ghsl.jrc.ec.europa.eu/download.php (uncompressed size is 541.390619 megabytes for one file download). 
- If you want to double check this number and if you're on Linux or MacOS, clone or download this repository and run `unzip -Zt GHS_BUILT_LDS2014_GLOBE_R2018A_54009_250_V2_0.zip` wherever the ZIP file lives.
- Their guide: https://ghsl.jrc.ec.europa.eu/documents/GHSL_Data_Package_2019.pdf?t=1478q532234372

Found the data through: https://luminocity3d.org/WorldPopDen/ which is an interactive map of the population densities.

Here is the blog post that went along with that interactive map: https://citygeographics.org/2016/12/26/global-urban-constellations/

Some of the Docker configuration comes from [cookiecutter-django](https://github.com/pydanny/cookiecutter-django).

### Citation

I'm using the [GHS-POP](https://ghsl.jrc.ec.europa.eu/data.php?sl=3) dataset (in tiled versions):
```
Dataset:

Schiavina, Marcello; Freire, Sergio; MacManus, Kytt (2019): GHS population grid multitemporal (1975-1990- 2000-2015), R2019A. European Commission, Joint Research Centre (JRC) [Dataset] doi:10.2905/0C6B9751- A71F-4062-830B-43C9F432370F PID: http://data.europa.eu/89h/0c6b9751-a71f-4062-830b-43c9f432370f

Concept & Methodology:

Freire, Sergio; MacManus, Kytt; Pesaresi, Martino; Doxsey-Whitfield, Erin; Mills, Jane (2016): Development of new open and free multi-temporal global population grids at 250 m resolution. Geospatial Data in a Changing World; Association of Geographic Information Laboratories in Europe (AGILE). AGILE 2016.
```

To open the dataset (since most of us have never used it, including me), we need to have a GIS. I'm using QGIS [brought to me from here.](http://www.statsmapsnpix.com/2016/10/the-global-human-settlement-layer.html)

### TODO
- Show all users' locations
