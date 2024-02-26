from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, date
from django.utils import timezone
# Create your models here.

class IpAddress(models.Model):
	ip = models.GenericIPAddressField(unique=True)

	def __str__(self):
		return self.ip

class Post(models.Model):
	title = models.CharField(max_length=150)
	poster = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='post-image/', blank=True, null=True)
	context = models.TextField()
	post_time = models.DateTimeField(auto_now=True)
	slug = models.SlugField(default="", null=False)

	post_class = [
		("LR","生活紀錄"),
		("CR","創作"),
	]

	classification = models.CharField(max_length=2, choices=post_class,default="LR")
	
	posterip = models.ForeignKey(IpAddress, related_name='posterip', on_delete=models.SET_NULL, null=True)
	viewersip = models.ManyToManyField(IpAddress,  related_name='viewersip', blank=True)

	def __str__(self):
		return self.title

	def get_viewersip_count(self):
		count = self.viewersip.count()
		return count


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment_text = models.TextField()

	def __str__(self):
		return f"{self.post} {self.user}"

