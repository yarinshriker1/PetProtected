# Generated by Django 4.0 on 2021-12-26 12:33

from django.db import migrations, models

STATUS_LIST = [
    'Like New',
    'Good',
    'Slightly damaged',
    'Requires repair'
]


def add_default_status(apps, schema_editor):
    mode_class = apps.get_model("share_place", "Product")
    for sta in STATUS_LIST:
        mode_class.objects.get_or_create(
            title=sta
        )


class Migration(migrations.Migration):
    dependencies = [
        ('share_place', '0005_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.RunPython(add_default_status)
    ]
