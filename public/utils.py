"""
This is where we'll download the data and
migrate it to the database.
"""
from math import sqrt, pi
import pathlib
from uuid import uuid4
from random import uniform

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
import rasterio as rio
from names import get_first_name, get_last_name
import numpy as np

from .models import User

from sys import getsizeof


def create_users(apps, schema_editor):  # Don't touch the params
    # In case user using multiple DB
    if schema_editor.connection.alias != "default":  # Default being the database name
        return

    """
    Every tile has a Float32 value from 0 to some 500 ish.
    Each tile is given a max of int(left_out / number_of_users),
    or with default 2598.
    """

    # Begin accessing data
    path_to_data = pathlib.Path("/", "app", settings.GIS_DATASET_NAME)
    with rio.open(path_to_data, "r") as src:
        """
        The data is the "shade" instead of any RGB or grayscale value.
        https://rasterio.readthedocs.io/en/latest/topics/color.html#writing-colormaps
        Using dataset_mask() gave me no luck; only two numbers appeared 0 and 255.
        The data here is Float32 which gave me a nice range of values.
        """
        print("GHS-POP Dataset Meta Info:", src.meta)
        data = src.read(1)
        map_height, map_width = data.shape  # Default 36000, 72164

    # Reduce memory consumption
    if settings.LIMITED_MEMORY:
        # Keep Float32 dtype unless on limited memory
        data.astype('float16')
    data[data < 0] = 0.0

    """
    The shape of the dataset is supposed to be width 72000 and height 36000
    Numpy shape: (36000, 72164) Latitude, Longitude or Horizontal and Vertical.
    meta = {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -200.0, 'width': 72164, 'height': 36000,
    'count': 1, 'crs': None, 'transform': Affine(1.0, 0.0, 0.0,0.0, 1.0, 0.0)}
    
    Basically, whenever we encounter -200.0, we know there is no data there (as in water).
    """
    # Pre-made variables to reduce num of calculations

    # Number of tiles: 36000 * 72164 = 2597904000
    tile_density = int(map_height * map_width / settings.NUM_OF_USERS)

    root2 = sqrt(2)
    map_radius = map_width / (2 * root2)
    lat_range = 90 / map_width  # 180 / map_width / 2
    lon_range = 90 / map_height  # 180 / map_height / 2

    print("Beginning migration creation")

    # Begin migration based on shade
    for i, y in enumerate(data):
        # y starts from top then goes to bottom

        # We have to imagine the current numpy array is like the coordinate system
        # Then translate it when creating user locations
        temp_users = []
        for x in y:
            # x is now a tile. x starts from left and moves to right
            # Points go up to 14 decimal places
            if x in (-200.0, 0.0):  # No data or no people
                continue

            # Calculate the 4 Points as boundaries for these users' coordinates.
            theta = np.arcsin(i / map_radius / root2)

            temp = np.arcsin((2 * theta + np.sin(2 * theta)) / pi)
            lat_range = (
                temp - lat_range,
                temp + lat_range
            )

            temp = pi * x / 2 / map_radius / root2 * np.cos(theta)
            lon_range = (
                temp - lon_range,
                temp + lon_range
            )

            # Add user
            for user in range(int(tile_density * x)):  # Number of users in tile
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
            temp_users.clear()
