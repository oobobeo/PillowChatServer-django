from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# models/settings
from django.conf import settings
from .models import *
# DRF
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from .utils import signin
from random import randint
from datetime import datetime as dt
from django.db.models import Q
# debug
import inspect
import datetime

class TIME():
	def __init__(self):
		self.today = datetime.datetime.now()
	@property
	def START_DATE(self):
		if self.today.hour >= settings.CHANNEL_CLOSE_HOUR:
			d = self.today
		else:
			d = self.today-datetime.timedelta(days=1)
		return datetime.datetime(self.today.year,self.today.month,d.day,2,0,0,0)	
		# d = datetime.date(today.year,today.month,d.day,2,0,0,0)	
		# return datetime.strptime(d, '%Y-%m-%d')
	@property
	def END_DATE(self):
		d = datetime.date(2099, 3, 31)
		# return datetime.strptime(d, '%Y-%m-%d')
		return datetime.datetime(self.today.year,self.today.month,d.day,2,0,0,0)	

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ['pk','name']

class ChannelSerializer(serializers.ModelSerializer):
	# tag_names = serializers.CharField(source='tags.name')
	tags = TagSerializer(read_only=True, many=True)
	class Meta:
		model = Channel
		fields = ['pk','title','description','limit','creator','created_at',
				   'start_at','end_at','tags']

class MessageSerializer(serializers.ModelSerializer):
	# tag_names = serializers.CharField(source='tags.name')
	channel = TagSerializer(read_only=True, many=True)
	class Meta:
		model = Message
		fields = ['pk','user','text','file_url','sent_at']

class UserSerializer(serializers.ModelSerializer):
	# tag_names = serializers.CharField(source='tags.name')
	tags = TagSerializer(read_only=True, many=True)
	class Meta:
		model = User
		fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields = '__all__'


def qs_to_json_data(qs,sort='accuracy',page=1,type='Channel'):
	# type = 'Channel','User','Message','Tag'

	# SORT
	if type == 'Channel':
		if value == 'popularity':
			# NEED SOCKET DATA
			# qs_all = something
			pass
		elif value == 'recommend':
			# SESSION DATA -> TAGS
			# qs_all = something				
			pass
		elif value == 'recent':
			# SORT BY CREATED_AT				
			channels.order_by('-created_at')
		elif value == 'accuracy':
			# DONT DO ANYTHING. PASS ALONG
			pass
	# PAGE INDEX
	# if type == 'Channel':
		l = len(qs)
		if l == 1:
			pass
		elif page > ((l-1)//10)+1:
			return {}
		elif page<=((l-1)//10):
			qs = qs[(page-1)*10:(page-1)*10+9]
		else:
			qs = qs[(page-1)*10:]

	# SERIALIZE
	if type=='Channel':
		json = ChannelSerializer(qs,many=True,read_only=True)
	elif type=='Tag':
		json = TagSerializer(qs,many=True,read_only=True)
	elif type=='Message':
		json = MessageSerializer(qs,many=True,read_only=True)
	elif type=='User':
		json = UserSerializer(qs,many=True,read_only=True)
	elif type=='Notification':
		json = NotificationSerializer(qs,many=True,read_only=True)
	return json.data

# HTML FORM METHOD ONLY SUPPORTS 'GET','POST'
@api_view(['GET','POST','DELETE','PUT'])
def home(re):
	print(re.method)
	print(dir(re))
	# for i in dir(re):
	# 	print(eval('re.'+i))
	return render(re, "core/home.html")

def channels(re):
	json = {}
	page = re.GET.get('page')
	sort = re.GET.get('sort')
	if re.method == 'GET':
		query = list(re.GET.items())
		channels = Channel.objects.filter(created_at__range=(TIME().START_DATE, TIME().END_DATE))
		participant = Participant.objects.filter()
		if not query:
			json_data = qs_to_json_data(qs,sort='',page=page)
			return JsonResponse(json_data,safe=False)

		if 'search' in re.GET.keys():
			# HANDLE QUERY HERE
			# NEED TO ADD TAG SEARCH
			print(re.GET)
			qs_all = None
			for query_string in value.split('|'):
				query_string = ' '.join(query_string.split('+'))
				qs = channels.filter((Q(title__icontains='query_string') & Q(title__icontains='query_string'))|
									 (Q(title__icontains='query_string') & Q(description__icontains='query_string'))|
									 (Q(description__icontains='query_string') & Q(title__icontains='query_string'))|
									 (Q(description__icontains='query_string') & Q(description__icontains='query_string')))
				if qs_all:
					qs_all = qs_all | qs # merge querysets
				else:
					qs_all = qs

			json_data = qs_to_json_data(qs_all,sort=sort,page=page,type='Channel')
			return JsonResponse(json_data,safe=False)
		elif 'user' in re.GET.keys():
			qs = channels.get(creator=User.objects.get(pk=id))
			json_data = qs_to_json_data(qs,sort=sort,page=page,type='Channel')
			return JsonResponse(json_data,safe=False)
		elif 'participant' in re.GET.keys():
			qs = channels.filter(creator=User.objects.get(pk=id))
			json_data = qs_to_json_data(qs,sort=sort,page=page,type='Channel')
			return JsonResponse(json_data,safe=False)


	elif re.method =='POST':
		c = Channel.objects.create(title=re.POST['title'],description=re.POST['description'],
								   limit=re.POST['limit'],creator=User.objects.get(pk=id),
								   start_at=re.POST['start_at'],end_at=re.POST['end_at'])
		# create new tags -> add from Tag(db)
		# NEED POST response format FROM FRONT TO CONTINUE

		return JsonResponse(json_data,safe=False)

@api_view(['GET','POST','DELETE','PUT'])
def channels_id(re,id):
	# channels = Channel.objects.filter(created_at__range=(TIME().START_DATE, TIME().END_DATE))
	channel = Channel.objects.get(pk=id)
	json = {}
	if re.method == 'GET':
		json_data = qs_to_json_data(channel,type='Channel')
		return JsonResponse(json_data,safe=False)
	elif re.method == 'PUT':
		# NEED RE.BODY FORMAT
		if 'title' in re.data:
			channel.title = re.data.get('title')
		if 'description' in re.data:
			channel.description = re.data.get('description')
		if 'limit' in re.data:
			channel.limit = re.data.get('limit')
		if 'start_at' in re.data:
			channel.start_at = re.data.get('start_at')
		if 'end_at' in re.data:
			channel.end_at = re.data.get('end_at')
		if 'tags' in re.data:
			tags = re.data.get('tags')
			tag_list = [Tag.objects.get(name=tag_name) for tag_name in tags]
			channel.tags.clear()
			channel.tags.add(*tag_list)
		channel.save()
		json_data = qs_to_json_data(channel,type='Channel')
		return JsonResponse(json_data, safe=False)
	elif re.method == 'DELETE':
		channel.delete()
		return JsonResponse({},safe=False)

def channels_id_users(re,id):
	json = {}
	if re.method != 'GET':
		return HttpResponse('bad request')
	# paricipants = Participant.objects.filter(joined_at__range=(TIME().START_DATE, TIME().END_DATE))
	participants = Participant.objects.filter(channel=Channel.objects.get(pk=id))
	user_list = participants.user
	json_data = qs_to_json_data(user_list,type='User',page=re.data.get('page'))
	return JsonResponse(json_data,safe=False)

###########################################################################
def messages(re):
	json = {}
	if re.method != 'GET':
		return HttpResponse('bad request')
	if 'channel' in re.GET.keys():
		channel_id = re.GET['channel']
		messages = Message.objects.filter(channel=Channel.objects.get(pk=channel_id))
		json_data = qs_to_json_data(messages,type='Message')
		return JsonResponse(json_data,safe=False)
	else:
		pass
		return JsonResponse(json_data,safe=False)

def messages_id(re,message_id):
	json_data = {}
	if re.method != 'GET':
		return HttpResponse('bad request')
	return JsonResponse(json_data)

@api_view(['GET','POST','DELETE','PUT'])
def users_id(re,id):
	json = {}
	user = User.objects.get(pk=id)
	if re.method == 'GET':	
		json_data = qs_to_json_data(user,type='User')
		return JsonResponse(json_data)
	elif re.method == 'PUT':
		# NEED RE.BODY FORMAT
		if 'username' in re.data:
			user.title = re.data.get('username')
		if 'email' in re.data:
			user.description = re.data.get('email')
		if 'password' in re.data:
			user.limit = re.data.get('password')
		if 'color' in re.data:
			user.end_at = re.data.get('color')
		if 'tags' in re.data:
			tags = re.data.get('tags')
			tag_list = [Tag.objects.get(name=tag_name) for tag_name in tags]
			user.tags.clear()
			user.tags.add(*tag_list)
		user.save()
		json_data = qs_to_json_data(user,type='Channel')
		return JsonResponse(json_data, safe=False)
	elif re.method == 'DELETE':
		user.delete()
		return JsonResponse(json_data)

def users_id_tags(re,id):
	json = {}
	if re.method != 'GET':
		return HttpResponse('bad request')
	tag_list = User.objects.get(pk=id).tags
	json_data = qs_to_json_data(tag_list,type='Tag')
	return JsonResponse(json_data)

def users_id_notifications(re,id):
	json_data = {}
	if re.method == 'GET':
		notifications = Notification(user=User.objects.get(pk=id)).filter(is_read=False)
		json_data = qs_to_json_data(Notifications,type='Notification')
		return JsonResponse(json_data)
	if re.method == 'POST':
		pass
		# WHAT
		return JsonResponse(json_data)

# ***************************  ACCOUNTS  **********************************
def accounts_login(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accouts_logout(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accounts_password_change(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accounts_password_change_done(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accounts_password_reset(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accounts_password_reset_done(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accounts_reset_uidb64_token(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)

def accounts_reset_done(re):
	json = {}
	re.POST
	return JsonResponse(json_data,safe=False)




# ************************ FOR PRODUCTION ONLY ****************************
def filldb(request):
	print('*****filling db******')

	#6 tags
	tags = ['game', 'sports', 'music', 'travel', 'relationships', 'food']
	#10 messages
	messages = ['m1','m2','m3','받아치기알아보기','받아치기 받아치기','받아치기','안녕하살법 받아치기','안녕하살법', '선댓글 후감상', 'hello',]
	#10 users
	usernames = ['u1','u2','u3','u4','u5','u6','u7','u8','u9','u10']
	#6 colors
	colors = ['#ffffff','#ddffdd','#eeaaee','#00ff00','#ff00ff','#ffdd00']


	# 6 tags
	for tag in tags:
		Tag.objects.create(name=tag)
	print('Tag created')

	# 10 users
	for name in usernames:
		u = User.objects.create(username=name,password='pw',email='abc@naver.com',color=colors[randint(0,5)])
		u.tags.add(*Tag.objects.all()[randint(0,2):randint(3,5)])
	print('User created')

	# 100 channels
	for i in range(100):
		c = Channel.objects.create(title=f'ch{i}',description=f'des{i}',limit=5,
							   creator=User.objects.get(pk=randint(1,10)),start_at=dt.now(),end_at=dt.now())
		c.tags.add(*Tag.objects.all()[randint(0,2):randint(3,5)])
	print('Channel created')

	# Participant: <10 participants for each channel
	for c in Channel.objects.all():
		for u_id in range(randint(1,5),randint(6,11)):
			Participant.objects.create(channel=c,user=User.objects.get(pk=u_id))
	print('Participant created')

	# Message: 20 messages for each channel,
	for c in Channel.objects.all():
		p_qs = Participant.objects.filter(channel=c)
		for _ in range(20):
			Message.objects.create(channel=c,
								   user=p_qs.order_by('?')[0].user,
								   text=messages[randint(0,9)])
	print('Message created')

	# Notification: 5 notifications for each user
	for u in User.objects.all():
		for i in range(5):
			n = Notification.objects.create(user=u,content=f'noti{i}',notify_at=dt.now())
	print('Notification created')

	print('**** db filled ****')
	return JsonResponse(request.GET)

def fill_usertag(request):
	from random import randint
	from datetime import datetime as dt
	from django.db.models import Q
	tags = Tag.objects.all()
	for u_id in User.objects.all():
		instance = UserTag.objects.create()
		instance.user_id.add(u_id)
		instance.tag_id.add( *tags[randint(0,2):randint(3,5)] )
		instance.save()
	# for 
		# WRITE VALID CODE HERE
	for i in User.objects.get():
		print(i)
	print('UserTag created')

	# >> cheese_pizza = Pizza.objects.create(name='Cheese')
	# >> mozzarella = Topping.objects.create(name='mozzarella')
	# >> mozzarella.pizza_set.add(cheese_pizza)
	# >> mozzarella.pizza_set.all()

def showdb(request):
	data = '**************** All the db ****************\n'
	users = '\n\n\n******************User***********************\n'
	channels = '\n\n\n******************Channel***********************\n'
	participants = '\n\n\n******************Participant***********************\n'
	tags = '\n\n\n******************Tag***********************\n'
	messages = '\n\n\n******************Message***********************\n'
	profiles = '\n\n\n******************Profile***********************\n'
	notifications = '\n\n\n******************Notification***********************\n'
	for u in User.objects.all():
		users+=str(u)
		users+='\n'
	for u in Channel.objects.all():
		channels+=str(u)
		channels+='\n'
	for u in Participant.objects.all():
		participants+=str(u)
		participants+='\n'
	for u in Tag.objects.all():
		tags+=str(u)
		tags+='\n'
	for u in Message.objects.all():
		messages+=str(u)
		messages+='\n'
	for u in Notification.objects.all():
		notifications+=str(u)
		notifications+='\n'
	data = data+users+channels+participants+tags+messages+profiles+notifications
	return HttpResponse(data)

def showdb_for_debug():
	data = '**************** All the db ****************\n'
	users = '\n\n\n******************User***********************\n'
	channels = '\n\n\n******************Channel***********************\n'
	participants = '\n\n\n******************Participant***********************\n'
	tags = '\n\n\n******************Tag***********************\n'
	channeltags = '\n\n\n******************ChannelTag***********************\n'
	usertags = '\n\n\n******************UserTag***********************\n'
	messages = '\n\n\n******************Message***********************\n'
	profiles = '\n\n\n******************Profile***********************\n'
	notifications = '\n\n\n******************Notification***********************\n'
	for u in User.objects.all():
		users+=str(u)
		users+='\n'
	for u in Channel.objects.all():
		channels+=str(u)
		channels+='\n'
	for u in Participant.objects.all():
		participants+=str(u)
		participants+='\n'
	for u in Tag.objects.all():
		tags+=str(u)
		tags+='\n'
	for u in ChannelTag.objects.all():
		channeltags+=str(u)
		channeltags+='\n'
	for u in UserTag.objects.all():
		usertags+=str(u)
		usertags+='\n'
	for u in Message.objects.all():
		messages+=str(u)
		messages+='\n'
	for u in Profile.objects.all():
		profiles+=str(u)
		profiles+='\n'
	for u in Notification.objects.all():
		notifications+=str(u)
		notifications+='\n'
	data = data+users+channels+participants+tags+channeltags+usertags+messages+profiles+notifications
	with open('all_of_db.txt','w+') as f:
		f.write(data)
	return data

def create_one_channel(request):
	for i in range(1):
		c = Channel.objects.create(title=f'ch{i}',description=f'des{i}',limit=5,
						   creator=User.objects.get(pk=randint(1,10)),start_at=dt.now(),end_at=dt.now())
	c.tags.add(*Tag.objects.all()[randint(0,2):randint(3,5)])
	print('Channel created')
	return HttpResponse('')


