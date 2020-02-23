from django.db import migrations
from django.contrib.gis.geos import Point
from public.models import User
from public.utils import create_users


def create_superuser(apps, schema_editor):
    User.objects.create_superuser(
        username="test",
        password="test",
        location=Point(42.3314, -83.0458)
    )


class Migration(migrations.Migration):
    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_users)
    ]
