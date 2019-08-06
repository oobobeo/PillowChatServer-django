from django.db import models
from django.contrib.auth.models import AbstractUser
# from django_mysql.models import JSONField
from django.conf import settings

class Tag(models.Model):
	name = models.CharField(max_length=15)
	def __str__(self):
		return f'TAG|name:{self.name}'
		# return f'TAG:{self.name}'

class User(AbstractUser):
	# username = models.CharField(max_length=150)
	# password = models.CharField(max_length=10)
	# email = models.EmailField(max_length=255, unique=True)
	joined_at = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, blank=True)
	color = models.CharField(max_length=7,blank=True,null=True)
	def __str__(self):
		return f'USER|username:{self.username}|email:{self.email}|joined_at:{self.joined_at}'
		# return f'USER:{self.username}'

class Channel(models.Model):
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	limit = models.SmallIntegerField(default=4)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	start_at = models.DateTimeField()
	end_at = models.DateTimeField()
	tags = models.ManyToManyField(Tag,blank=True)
	def __str__(self):
		return f'CHENNEL|title:{self.title}|description:{self.description}|limit:{self.limit}\
		|creator_id:{self.creator_id}|created_at:{self.created_at}|start_at:{self.start_at}\
		|end_at:{self.end_at}'
		# return f'CHANNEL:{self.title}'

class Participant(models.Model):
	channel = models.ForeignKey(Channel, blank=False, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,on_delete=models.CASCADE)
	joined_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'PARTICIPANT|channel:{self.channel_id}|user:{self.user_id}|joined_at:{self.joined_at}'
		# return f'PARTICIPANT:{self.user_id}'

class Message(models.Model):
	channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	text = models.CharField(max_length=500,blank=True)
	file_url = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY,null=True,blank=True)
	sent_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'MESSAGE|channel_id:{self.channel_id}|user_id:{self.user_id}|text:{self.text}\
		|file_url:{self.file_url}|sent_at:{self.sent_at}'
		# return f'MESSAGE:{self.text}'

class Notification(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
	content = models.CharField(max_length=400,blank=True,null=True)
	notify_at = models.DateTimeField(blank=True,null=True)
	is_read = models.BooleanField(default=False)
	def __str__(self):
		return f'NOTIFICATION|user_id:{self.user}|content:{self.content}|notify_at:{self.notify_at}\
		|is_read:{self.is_read}'
		# return f'NOTIFICATION:{self.content}'







# class UserTag(models.Model):
# 	user_id = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
# 	tag_id = models.ManyToManyField(Tag, blank=True)
# 	def __str__(self):
# 		return f'USERTAG|user_id:{self.user_id}|tag_id:{self.tag_id}'
# 		# return f'USERTAG:{self.tag_id}'

# class ChannelTag(models.Model):
# 	channel_id = models.ManyToManyField(Channel, blank=False)
# 	tag_id = models.ManyToManyField(Tag, blank=True)
# 	def __str__(self):
# 		return f'CHANNELTAG|channel_id:{self.channel_id}|tag_id:{self.tag_id}'
# 		# return f'CHNNELTAG:{self.tag_id}'

# class Profile(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
# 	color = models.CharField(max_length=10)
# 	def __str__(self):
# 		return f'PROFILE|user_id:{self.user_id}|color:{self.color}'
# 		# return f'PROFILE'

