# Django: Sample Location Build

By: Andrew Chen Wang

If you need a sample data set of users in locations to test your location-based app, this Django sample can help.

### Setup

1. Clone or download this repository.
2. You must have Docker and docker-compose to execute the following commands to build and 
download the data: `docker-compose up --build`
3. Start looking around!

### Configuration

If you only want users to be created for the US, go to public/utils.py and set the GLOBAL variable to "US"

### What did I do?

I've simply added a bunch of users to a custom User model. They have funny names, but most importantly, their locations are now stored in the database.

These locations are generated based on population count. They are scattered around within a city, as well.

### Credits

Sample data comes from the US Census Bureau.

Some of the Docker configuration comes from [cookiecutter-django](https://github.com/pydanny/cookiecutter-django).
