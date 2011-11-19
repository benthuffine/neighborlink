from django.db import models
from datetime import datetime

class Page(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=255)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.slug

class Heroshot(models.Model):
    image = models.ImageField(upload_to='ext/heroshots')
    description = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255,blank=True)
    sort_order = models.PositiveIntegerField(null=True, blank=True)
    page = models.ForeignKey(Page)   
    
    class Meta:
        ordering = ['sort_order',]

class Article(Page):
    insert_date = models.DateField(null=True, auto_add_now=True)
    teaser = models.CharField(max_length=1024, null=True, blank=True)

class NewsEvent(Page):
    start_date = models.DateField(null=True, verbose_name='Date to start display')
    end_date = models.DateField(null=True, verbose_name='Date to end display')
    event_start_date = models.DateTimeField(null=True)
    event_end_date = models.DateTimeField(null=True)
    teaser = models.CharField(max_length=1024, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = datetime.now()
        super(Event, self).save(*args, **kwargs)

    def get_date_string(self):
        #   Saturday, December 11th, 2011 from 2 to 6 pm
        start_date = self.event_start_date
        end_date = self.event_end_date
        if not start_date:
            return ''

        ds = start_date.day
        if ds%10 == 1:
            ds = "%dst" % ds
        elif ds%10 == 2:
            ds = "%dnd" % ds
        elif ds%10 == 3:
            ds = "%drd" % ds
        else:
            ds = "%dth" % ds
        
        if start_date.year == end_date.year and start_date.month == end_date.month and start_date.day == end_date.day:
            #  Same day
            ds = start_date.strftime('%A, %B') + (" %s " % ds) + start_date.strftime('%Y') + " from"
            if start_date.strftime('%p') == end_date.strftime('%p'):
                ds = "%s %d to %d %s" % (ds, start_date.strftime('%I'), end_date.strftime('%I'), start_date.strftime('%p'))
            else:
                ds = "%s %d %s to %d %s" % (ds, start_date.strftime('%I'), start_date.strftime('%p'), end_date.strftime('%I'), end_date.strftime('%p'))
        else:
            ds = start_date.strftime('%A, %B') + " until " + end_date.strftime('%A, %B')
        return ds
        
    date_string = property(get_date_string)        