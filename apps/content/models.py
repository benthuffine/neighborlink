from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='ext/heroshots')
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255,blank=True)
    sort_order = models.PositiveIntegerField(null=True, blank=True)

class Page(models.Model):
    slug = models.SlugField(max_length=255)
    heroshots = models.ManyToManyField(Image, null=True)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.slug