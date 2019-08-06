from django.urls import path, include
from . import views
# from utils import router


urlpatterns = [
    path('', views.home),

    # Search for channels
    path('channels',views.channels),

    # enter/alter/delete a certain channel
    path('channels/<int:id>',views.channels_id),
    path('channels/<int:id>/users',views.channels_id_users),

    # search for messages
    path('messages',views.messages),
    path('messages/<int:id>',views.messages_id),

    # profile: search, update, delete
    path('users/<int:id>',views.users_id),
    path('users/<int:id>/tags',views.users_id_tags),

    # notifications
    path('users/<int:id>/notifications',views.users_id_notifications),

    #accounts
    path('accounts/login',views.accounts_login),
    path('accounts/logout',views.accouts_logout),
    path('accounts/password_change',views.accounts_password_change),
    path('accounts/password_change/done',views.accounts_password_change_done),
    path('accounts/password_reset',views.accounts_password_reset),
    path('accounts/password_reset/done',views.accounts_password_reset_done),
    path('accounts/reset/<uidb64>/<token>',views.accounts_reset_uidb64_token),
    path('accounts/reset/done',views.accounts_reset_done),

    #create/show data
    path('filldb',views.filldb),
    path('showdb', views.showdb),
    path('fill_usertag',views.fill_usertag),
    path('create_one_channel',views.create_one_channel)

]
