from django.urls import path

from . import views


urlpatterns = [



    path('fin/update/<pk>/', views.finbookUpdateView.as_view(), name='finupdate'),
    path('fin/new/', views.CreatefinbookView.as_view(), name='finnew'),
    path('fin/description/new', views.newdis, name='newdis'),
    path('fin/index', views.index, name='index'),
    path('fin/<pk>/', views.finbookDetailView.as_view(), name='transactiondetail'),
    path('fin/newdis/', views.newdis, name='newdis'),
    path('mytext/', views.mystream, name='mystream'),
    path('anova10/', views.anova, name='anova10'),
    path('twit/', views.fillsource, name='fillsource'),
    path('testtext/', views.testtext, name='testtext'),
    path('myimport/', views.myimport, name='myimport'),

    path('project/new/', views.projectnew, name='projectnew'),
    path('project/<pk>/', views.projectDetailView.as_view(), name='projectdetail'),
    path('project/<pk>/delete', views.projectDeleteView.as_view(), name='projectdelete'),
    path('project/', views.projectlist, name='projectlist'),
    path('project/update/<pk>/', views.projectUpdateView.as_view(), name='projectupdate'),

    path('search/new/<pk>/', views.searchnew, name='searchnew'),
    path('search/<pk>/', views.searchdetail, name='searchdetail'),
    path('search/<pk>/delete', views.searchDeleteView.as_view(), name='searchdelete'),
    path('search/', views.searchlist, name='searchlist'),
    path('search/update/<pk>/', views.searchUpdateView.as_view(), name='searchupdate'),
    path('searchrun/<pk>/', views.searchrun, name='searchrun'),
    path('searchrun2/<pk>/', views.searchrun2, name='searchrun2'),
    path('searchrun3', views.searchrun3, name='searchrun3'),

        ]
