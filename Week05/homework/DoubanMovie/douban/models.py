# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbDouban(models.Model):
    short_comments = models.CharField(max_length=1000, blank=True, null=True)
    star_num = models.IntegerField(blank=True, null=True)
    comment_time = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_douban'
