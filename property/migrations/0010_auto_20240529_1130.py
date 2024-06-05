# Generated by Django 2.2.24 on 2024-05-29 08:30

from django.db import migrations


def migrate_flat_to_owner(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    for flat in Flat.objects.iterator():
        owner, created = Owner.objects.get_or_create(
            holder=flat.owner,
            pure_phone=flat.owner_pure_phone,
            phonenumber=flat.owners_phonenumber
        )
        owner.apartments.add(flat)
        owner.save()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_auto_20240529_1121'),
    ]

    operations = [
        migrations.RunPython(migrate_flat_to_owner),
    ]
