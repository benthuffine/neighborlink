from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.utils.text import truncate_html_words
from django.conf import settings
from neighborlink.apps.content.models import *
from twitter import Api, TwitterError, CHARACTER_LIMIT, Status

class BetterApi(Api):
	def BetterPostUpdate(self, status, data={}):
		"""
			Allows for passing in other data for post
		"""
		if not self._oauth_consumer:
			raise TwitterError("The twitter.Api instance must be authenticated")
		
		url = '%s/statuses/update.json' % self.base_url

		if isinstance(status, unicode) or self._input_encoding is None:
			u_status = status
		else:
			u_status = unicode(status, self._input_encoding)
		
		if len(u_status) > CHARACTER_LIMIT:
			raise TwitterError("Text must be less than or equal to %d characters." % CHARACTER_LIMIT)
		
		data.update({'status': status})
		json = self._FetchUrl(url, post_data=data)
		data = self._ParseAndCheckTwitter(json)
		return Status.NewFromJsonDict(data)
	
	def GetConfig(self):
		url = '%s/help/configuration.json' % self.base_url

		json = self._FetchUrl(url)
		data = self._ParseAndCheckTwitter(json)
		return data

def update_twitter(title, url):
	api = BetterApi(consumer_key=settings.TWITTER_CONSUMER_KEY,
					consumer_secret=settings.TWITTER_CONSUMER_SECRET,
					access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
					access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
					)
	config = api.GetConfig()
	short_url_length = config['short_url_length']

	#	Trim the status back to CHARACTER_LIMIT - short_url_length - 1 (for space between)
	status_length = CHARACTER_LIMIT - short_url_length - 1
	title = title[:status_length]

	status = '%s %s' % (title, url)
	
	try:
		status = api.BetterPostUpdate(status, data={'wrap_links': True})
	except TwitterError:
		pass
	

def update_facebook(title, teaser, url):
	pass
	#print 'update facebook: %s %s %s' % (title, teaser, url)

def social_updates(instance, created):
	site = Site.objects.get_current()
	title = instance.title
	teaser = instance.teaser and instance.teaser or truncate_html_words(instance.content, 40)
	url = 'http://%s/%s' % (site.domain, instance.get_absolute_url())

	update_twitter(title, url)
	update_facebook(title, teaser, url)

@receiver(post_save, sender=AboutPage)
def about_social_updates(sender, instance, created, **kwargs):
	social_updates(instance, created)

@receiver(post_save, sender=ResourcePage)
def resource_social_updates(sender, instance, created, **kwargs):
	social_updates(instance, created)

@receiver(post_save, sender=CommunityAssocationPage)
def community_social_updates(sender, instance, created, **kwargs):
	social_updates(instance, created)

@receiver(post_save, sender=NewsEvent)
def news_social_updates(sender, instance, created, **kwargs):
	social_updates(instance, created)

