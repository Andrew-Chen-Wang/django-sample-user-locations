from django.db import migrations
from django.contrib.gis.geos import Point
from public.models import User
from public.utils import create_users


def create_superuser(apps, schema_editor):
    User.objects.create_superuser(
        username="test",
        password="test",
        # Location of DARPA
        location=Point(-77.108704, 38.878888)  # West, North | Long, Lat
    )


class Migration(migrations.Migration):
    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_users)
    ]
