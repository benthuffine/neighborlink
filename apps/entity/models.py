from django.db import models

class Entity(models.Model):
	name = models.CharField(max_length=128)
	tagline = models.CharField(max_length=1024, null=True, blank=True)
	website = models.URLField(verify_exists=True, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	facebook = models.URLField(verify_exists=True, null=True, blank=True)
	twitter = models.URLField(verify_exists=True, null=True, blank=True)
	addr1 = models.CharField(max_length=512, null=True, blank=True)
	addr2 = models.CharField(max_length=512, null=True, blank=True)
	phone = models.CharField(max_length=16, null=True, blank=True)
	year_founded = models.DateField(null=True, blank=True)
	featurable = models.BooleanField(default=False)


class Business(Entity):
	hours = models.CharField(max_length=1024)
	
	

class Church(Entity):
	pass

class Organization(Entity):
	pass


class Offer(models.Model):
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	description = models.TextField()
	models.ForeignKeyField(Business)	

class Comment(models.Model):
	insert_date = models.DateField(auto_now_add=True)
	rating = models.BooleanField(default=True)
	comment = models.TextField()
	entity = models.ForeignKeyField(Entity)	

class Featured(models.Model):
	entity = models.ForeignKeyField(Entity)
	date_featured = models.DateField()


