"""
This is where we'll download the data and
migrate it to the database.
"""
import os
import math
from pathlib import Path
from uuid import uuid4
from random import uniform

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
import rasterio as rio
from names import get_first_name, get_last_name
import numpy as np

from .models import User
from .download import download_tiles_zip, unzip_and_grab_tif

# Mollweide projection has this as a 2:1 ratio
__GLOBE_WIDTH = 144000
__GLOBE_HEIGHT = 72000


def get_geo_coordinates(
        index_y: int,
        index_x: int,
        tile_coordinates: tuple,
):
    """
    This function gets the geographic coordinates in radians from a given
    tile and the x,y coordinate within that tile.
    Refer here for geographic calculations: https://gis.stackexchange.com/a/351880/158640

    :param index_y: The index value of the current y within the given tile
    :param index_x: The index value of the current y within the given tile
    :param tile_coordinates: the tile's coordinates on the map
    :return: latitude, longitude in radians
    """
    # Predefining variables for calculation
    # Setting up r, radius of world with given pixel values.
    mollweide_center_width = 72000
    mollweide_center_height = 36000
    sqrt2 = math.sqrt(2)
    r = (__GLOBE_WIDTH / 2) / 2 / sqrt2

    # Get actual x, y coordinates using the indices
    y_2d = index_y + (4000 * tile_coordinates[1]) - mollweide_center_height
    x_2d = index_x + (4000 * tile_coordinates[0]) - mollweide_center_width

    # Start Mollweide projection calculations based on indices
    theta = math.asin(y_2d / r / sqrt2)
    latitude = math.asin((2 * theta + math.sin(2 * theta)) / math.pi)
    longitude = math.pi * x_2d / 2 / r / sqrt2 / math.cos(theta)
    return latitude, longitude


def create_users(apps, schema_editor):
    # In case user using multiple DB
    if schema_editor.connection.alias != "default":  # Default being the database name
        return
    """
    Every tile has a Float32 value from 0 to some 500 ish.
    Each tile is given a max of int(left_out / number_of_users),
    or with default 2598.
    """
    print("\nGrabbing dataset from online...")
    file_and_intervals: dict = unzip_and_grab_tif(download_tiles_zip())
    # tile_apportionment = int(__GLOBE_WIDTH * __GLOBE_HEIGHT / settings.NUM_OF_USERS)
    print("Beginning user creation...")
    tile_apportionment = int(4 * math.pi * ((__GLOBE_WIDTH / 2 / 2 / math.sqrt(2)) ** 2) / settings.NUM_OF_USERS)
    conversion_factor = 180 / math.pi

    # Loop the tif files from dataset directory
    for (tif, tile_coordinates) in file_and_intervals.items():
        with rio.open(Path.cwd() / "dataset" / tif) as src:
            # Densities returns a numpy array representing population density
            densities_array = src.read(1)  # Shape 4000 x 4000
        print("Processing the interval:", tile_coordinates)

        # Start creating users. y is like y=3 as a horizontal line in 2D graph
        for index, density in np.ndenumerate(densities_array):
            if density in (-200, 0):
                continue
            # index var is a tuple of (x, y)
            latitude, longitude = get_geo_coordinates(
                index_y=index[1],
                index_x=index[0],
                tile_coordinates=tile_coordinates
            )

            # Check if latitude and longitude is within range
            if abs(latitude) > math.pi or abs(longitude) > math.pi:
                continue

            # Get the range of (lat, long) values that a user can be in.
            lat_range, lon_range = get_geo_coordinates(
                index_y=index[1] + 1,
                index_x=index[0] + 1,
                tile_coordinates=tile_coordinates
            )

            # Convert to degrees for better Point storage and rendering
            lat_range = (
                latitude * conversion_factor,
                lat_range * conversion_factor
            )
            lon_range = (
                longitude * conversion_factor,
                lon_range * conversion_factor
            )

            # Create the users
            temp_users = []
            for user in range(int(tile_apportionment * density)):  # Number of users in tile
                temp_users.append(
                    User(
                        username=uuid4(),
                        password=make_password("test", None, "md5"),
                        first_name=get_first_name(),
                        last_name=get_last_name(),
                        location=Point(
                            uniform(lon_range[0], lon_range[1]),
                            uniform(lat_range[0], lat_range[1])
                        )
                    )
                )

            # Bulk add users to User model
            User.objects.bulk_create(temp_users)

        # Delete the TIF file to decrease storage
        os.remove(Path.cwd() / "dataset" / tif)
