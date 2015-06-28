from django.conf.urls import patterns, include, url
from django.contrib import admin
from kundli import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^api/get/sentiment/$',views.sentiment, name='sentiment'),
    url(r'^api/get/topics/$',views.topics, name='topics'),
    url(r'^api/get/sleep_pattern/$',views.sleep_pattern, name='sleep_pattern'),
    url(r'^api/get/top_tweets/$',views.top_tweets, name='top_tweets'),
    url(r'^api/get/topics_hear_about/$',views.topics_hear_about, name='topics_hear_about'),
    url(r'^api/get/topics_talk_about/$',views.topics, name='topics_talk_about'),
    url(r'^api/get/top_tweets/$',views.top_tweets, name='topics_talk_about'),
    url(r'^api/get/get_profile/$',views.get_profile, name='profile'),
    url(r'^api/get/get_interest/$',views.get_interest, name='profile'),
    url(r'^api/get/get_graph/$',views.get_graph, name='profil'),
    url(r'^api/get/get_location/$',views.get_location, name='profil'),
    url(r'^home/$',views.home, name='home'),


    ###### API ENDPOINTS ##########




)
