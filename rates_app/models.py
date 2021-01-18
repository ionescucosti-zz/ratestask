from django.db import models


class Regions(models.Model):
    slug = models.TextField(primary_key=True)
    name = models.TextField()
    parent_slug = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_slug', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regions'


class Ports(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()
    parent_slug = models.ForeignKey(Regions, models.DO_NOTHING, db_column='parent_slug')

    class Meta:
        managed = False
        db_table = 'ports'


class Prices(models.Model):
    orig_code = models.ForeignKey(Ports, models.DO_NOTHING, db_column='orig_code', related_name='orig_code')
    dest_code = models.ForeignKey(Ports, models.DO_NOTHING, db_column='dest_code', related_name='dest_code')
    day = models.DateField()
    price = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'prices'
