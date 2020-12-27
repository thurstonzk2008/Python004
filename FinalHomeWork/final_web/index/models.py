from django.db import models


class SKUs(models.Model):
    # id 自动创建
    sku = models.PositiveIntegerField()  # sku id
    skuname = models.CharField(max_length=200)  # sku name
    updatetime = models.DateTimeField(null=True)  # update time
    skuurl = models.URLField()
    pricescript = models.CharField(
        max_length=50, null=True)  # description of price
    skudescription = models.TextField(null=True)
    worthy = models.PositiveIntegerField(null=True)
    notworthy = models.PositiveIntegerField(null=True)
    stars = models.PositiveIntegerField(null=True)


class Comments(models.Model):
    # id 自动创建
    sku = models.PositiveIntegerField()  # sku id
    cid = models.PositiveIntegerField()  # comment id
    # quote id, which comment followed, if more than one commont to follow, use the minimal qid(earlyer)
    qid = models.PositiveIntegerField()
    updatetime = models.DateTimeField(null=True)
    user = models.CharField(max_length=200)  # user name
    cdescription = models.TextField(null=True)
    sentiments = models.FloatField(null=True)
