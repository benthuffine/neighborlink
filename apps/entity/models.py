from django.db import models
from django.contrib.auth.models import User

class Entity(models.Model):
	name = models.CharField(max_length=128)
	tagline = models.CharField(max_length=1024, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	website = models.URLField(verify_exists=True, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	facebook = models.URLField(verify_exists=True, null=True, blank=True)
	twitter = models.URLField(verify_exists=True, null=True, blank=True)
	addr1 = models.CharField(max_length=512, null=True, blank=True)
	addr2 = models.CharField(max_length=512, null=True, blank=True)
	city = models.CharField(max_length=128, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	phone = models.CharField(max_length=16, null=True, blank=True)
	zip = models.CharField(max_length=10, null=True, blank=True)
	year_founded = models.DateField(null=True, blank=True)
	featurable = models.BooleanField(default=False)
	readable_location = models.CharField(max_length=2046, null=True, blank=True)
	owners = models.ManyToManyField(User)

	def get_address(self, single_line=True):
		joiner = single_line and ' ' else '<br>'
		
		addr = [self.addr1,]
		if self.addr2:
			addr.append("%s," % self.addr2)
		else:
			addr[0] = "%s," % addr[0]
		
		if self.city:
			addr.append("%s," % self.city)
		
		if self.state:
			addr.append(self.state)
		
		if self.zip:
			addr.append(self.zip)

		return joiner.join(addr)

	def get_single_line_address(self):
		return self.get_address(single_line=True)
	single_line_address = property(get_single_line_address)

	def get_multi_line_address(self):
		return self.get_address(single_line=False)
	multi_line_address = property(get_multi_line_address)

		

class BusinessType(models.Model):
	name = models.CharField(max_length=128)

class Business(Entity):
	hours = models.CharField(max_length=1024)
	business_type = models.ForeignKeyField(BusinessType)
	features = models.CharField(max_length=1024)

class Church(Entity):
	pass

class Organization(Entity):
	pass


class Offer(models.Model):
	name = models.CharField(max_length=512)
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


