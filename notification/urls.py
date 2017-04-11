from django.conf.urls import url

from notification.views import notices, mark_all_seen, single

urlpatterns = [
    url(r'^$', notices, name='notification_notices'),
    url(r'^(\d+)/$', single, name='notification_notice'),
    #url(r'^feed/$', feed_for_user, name="notification_feed_for_user"),
    url(r'^mark_all_seen/$', mark_all_seen, name='notification_mark_all_seen'),
]
