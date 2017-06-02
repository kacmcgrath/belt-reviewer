from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="reg"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^books$', views.books, name='books'),
    url(r'^add$', views.add, name='add'),
    url(r'^process$', views.process, name='process'),
    url(r'^book/(?P<id>\d+)$', views.book, name='book'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review, name='delete_review'),
]
