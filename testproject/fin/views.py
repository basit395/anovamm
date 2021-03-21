from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from django.utils import timezone
from django.http import HttpResponseRedirect
import datetime
from datetime import timedelta
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import finbook,textstream,sentmentlist,project,search,searchdetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Count , Sum , Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from eventregistry import *
import json
from django.urls import reverse_lazy
from .filters import textstreamFilter
from .forms import finbookForm,projectForm,searchForm,searchrunForm
from django.shortcuts import get_object_or_404, render
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)



YOUTUBE_API_KEY ='AIzaSyAWSRZJ-Dhm0nVKK7GYp8siNSnWwnJUwYM'
def index(request):

    mysearch = textstream.objects.all().order_by('-id')
    myfilter = mysearchFilter(request.GET,queryset=mysearch)
    mysearch = myfilter.qs

    paginator = Paginator(mysearch,20)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)


    context = {'mysearch':mysearch,'opps':opps}
    return render(request, 'fin/textstream.html',context)
    # finlist = finbook.objects.all().order_by('-creationdate')
    # context = {'finlist':finlist}
    # return render(request, 'fin/index.html',context)

class finbookUpdateView(UpdateView):
    redirect_field_name = 'fin/finbook_detail.html'
    form_class = finbookForm
    model = finbook

class CreatefinbookView(CreateView):
    redirect_field_name = 'fin/finbook_detail.html'
    form_class = finbookForm
    model = finbook

class finbookDetailView(DetailView):
    model = finbook

def newdis(request):
    pass

def mystream(request):

    mysearch = textstream.objects.all().order_by('-id')
    myfilter = mysearchFilter(request.GET,queryset=mysearch)
    mysearch = myfilter.qs

    paginator = Paginator(mysearch,20)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)


    context = {'mysearch':mysearch,'opps':opps}
    return render(request, 'fin/textstream.html',context)

def anova(request):
    mysearch = textstream.objects.all()
    alltext = textstream.objects.all()

    pos = sentmentlist.objects.filter(imporession='Positive').values_list('myword')
    posall = sentmentlist.objects.filter(imporession='Positive')
    poslist=posall.values_list('imporession', flat=True)


    negall = sentmentlist.objects.filter(imporession='Negative')
    neglist=negall.values_list('imporession', flat=True)


    text1 = textstream.objects.filter(impression='Neutral').exclude(frequency=5)[0:1000]
    for text in text1:
        text.frequency = 5
        texts = text.mytext.split()
        for word in texts:
            if word.lower() in poslist:
                text.impression = 'Positive'

            elif word.lower() in neglist:
                text.impression = 'Negative'

        text.save()

    fre5 = textstream.objects.filter(impression='Neutral').exclude(frequency=5)
    myfilter = textstreamFilter(request.GET,queryset=mysearch)
    mysearch = myfilter.qs

    paginator = Paginator(mysearch,20)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    languager =  mysearch.values('lang').annotate(Total=Count('id')).order_by('-Total')[0:20]
    languageall = alltext.values('lang').annotate(Total=Count('id')).order_by('-Total')[0:20]
    locationr = mysearch.values('location').annotate(Total=Count('id')).order_by('-Total')[0:20]
    locationall = alltext.values('location').annotate(Total=Count('id')).order_by('-Total')[0:20]
    impr = mysearch.values('impression').annotate(Total=Count('id'))
    impall = alltext.values('impression').annotate(Total=Count('id'))
    emotionnull = textstream.objects.filter(emotion='No thing').exclude(impression='No thing')[0:50]
    for em in emotionnull:
        em.emotion = em.impression
        em.save()
    emall = alltext.values('emotion').annotate(Total=Count('id'))
    emotionnull = textstream.objects.filter(emotion='No thing').exclude(impression='No thing')

    context = {'fre5':fre5,'poslist':poslist,'posall':posall,'negall':negall,'pos':pos,'emotionnull':emotionnull,'emall':emall,'impr':impr,'impall':impall,'locationr':locationr,'locationall':locationall,'languageall':languageall,'mysearch':mysearch,'opps':opps,'myfilter':myfilter,'languager':languager}
    return render(request, 'fin/textstream.html',context)

def fillsource(request):
    pl = []
    nl = []
    alltext  = textstream.objects.filter(mytext__contains='kill').filter(impression = 'No thing')
    mypositive = sentmentlist.objects.filter(imporession='Positive').values('myword').distinct()
    mynegative = sentmentlist.objects.filter(imporession='Negative').values('myword').distinct()
    for zz in mypositive:
        pl.append(zz["myword"])
    for nn in mynegative:
        nl.append(nn["myword"])
    for dd in alltext:
        if dd.impression=='No thing':

            dds = dd.mytext.split()
            for dds1 in dds:
                dds1 = dds1.lower()
                if dds1 in pl :
                    dd.impression = 'Positive'
                    dd.save()
                    break
                elif dds1 in nl :
                    dd.impression = 'Negative'
                    dd.save()
                    break



    context = {'alltext':alltext,'mypositive':mypositive,'mynegative':mynegative,'pl':pl,'nl':nl}
    return render(request, 'fin/twit.html',context)

def testtext(request):
    posall = sentmentlist.objects.filter(imporession='Positive')
    poslist=posall.values_list('imporession', flat=True)

    negall = sentmentlist.objects.filter(imporession='Negative')
    neglist=negall.values_list('imporession', flat=True)

    nosent=[]
    nutraltext  = textstream.objects.filter(impression = 'Neutral')
    for text in nutraltext:
        texts = text.mytext.split()
        for word in set(texts):
            word = word.lower()
            if len(word) > 3:
                if word.isalpha():

                    if word not in poslist:
                        if word not in neglist:
                            if word not in nosent:
                                nosent.append(word)
    nosent.sort()
    nosentl = len(nosent)

    context = {'nutraltext':nutraltext,'nosent':nosent,'poslist':poslist,'nosentl':nosentl}
    return render(request, 'fin/testtext.html',context)

def home(request):

    myprojects = project.objects.filter(creator=request.user)
    context = {'myprojects':myprojects}
    return render(request,'fin/home.html',context)

def myimport(request):
    aa = 'Saudi Arabia'
    er = EventRegistry(apiKey = 'f97425bc-cc68-4da2-a302-9be8eb8ad153')
    bb = ''
    q = QueryArticlesIter(
        keywords = QueryItems.OR([aa, bb]),
        dataType = ["news", "blog"])
    # obtain at most 500 newest articles or blog posts
    q1 = q.execQuery(er, sortBy = "date", maxItems = 10)
    context = {'q1':q1}
    return render(request, 'fin/myimport.html',context)

# project=========================

def projectnew(request):
    if request.method=='POST':
        form = projectForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user

            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('projectdetail', args=(pk,)))

    else:
        form = projectForm()
    return render(request, 'fin/project_form.html',{'form':form})

class projectDetailView(DetailView):
    model = project

class projectDeleteView(DeleteView):
    model = project
    success_url = reverse_lazy('projectlist')

@login_required
def projectlist(request):
    projectlist = project.objects.filter(creator=request.user).order_by('-creationdate')
    context = {'projectlist':projectlist}
    return render(request, 'fin/projectlist.html',context)

class projectUpdateView(UpdateView):
    redirect_field_name = 'fin/project_detail.html'
    form_class = projectForm
    model = project


# Search============================


def searchnew(request,pk):
    if request.method=='POST':
        form = searchForm(request.POST)
        myproject = get_object_or_404(project,pk=pk)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.project = myproject

            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('searchdetail', args=(pk,)))

    else:
        form = searchForm()
    return render(request, 'fin/search_form.html',{'form':form})

def searchdetail(request,pk):
    searchnow = get_object_or_404(search,pk=pk)
    searchtexts = searchnow.search_texts.all()
    languager =  searchtexts.values('lang').annotate(Total=Count('id')).order_by('-Total')
    impr = searchtexts.values('impression').annotate(Total=Count('id')).order_by('-Total')
    context = {'searchnow':searchnow,'searchtexts':searchtexts,'languager':languager,'impr':impr}
    return render(request, 'fin/search_detail.html',context)

class searchDeleteView(DeleteView):
    model = search
    success_url = reverse_lazy('searchlist')

@login_required
def searchlist(request):
    searchlist = search.objects.filter(creator=request.user).order_by('-creationdate')
    context = {'searchlist':searchlist}
    return render(request, 'fin/searchlist.html',context)

class searchUpdateView(UpdateView):
    redirect_field_name = 'fin/search_detail.html'
    form_class = searchForm
    model = search


def searchrun(request,pk):
    if request.method=='POST':
        form = searchrunForm(request.POST)
        form.save()
        thesearch = get_object_or_404(search,pk=pk)
        word1 = form.cleaned_data['keyword1']

        word2 = form.cleaned_data['keyword2']
        maxi = form.cleaned_data['maxitems']

        if form.is_valid():

            myform = form.save(commit=False)
            myform.creator=request.user
            myform.search = thesearch
            myform.save()

            er = EventRegistry(apiKey = 'f97425bc-cc68-4da2-a302-9be8eb8ad153')
            q = QueryArticlesIter(
            keywords = QueryItems.OR([word1, word2]),
            dataType = ["news", "blog"])
        # obtain at most 500 newest articles or blog posts
            for art in q.execQuery(er, sortBy = "date", maxItems = maxi):

                textstream.objects.create(creator=request.user,source='aa',omytest=art['body'],impression=art['sentiment'],search=thesearch)

            return HttpResponseRedirect(reverse('searchdetail', args=(pk,)))

    else:
        form = searchrunForm()
    return render(request, 'fin/searchdetails_form.html',{'form':form})

def searchrun2(request,pk):


    if  request.method=='POST':


        form = searchrunForm(request.POST)

        thesearch = get_object_or_404(search,pk=pk)
        if form.is_valid():
            word1 = form.cleaned_data.get('word1')
            word2 = form.cleaned_data.get('word2')
            maxi = form.cleaned_data.get('maxi')




            er = EventRegistry(apiKey = 'f97425bc-cc68-4da2-a302-9be8eb8ad153')
            q = QueryArticlesIter(
            keywords = QueryItems.OR([word1, word2]),
            dataType = ["news", "blog"])

            for art in q.execQuery(er, sortBy = "date", maxItems = maxi):


                if not art['sentiment']:
                    imp1 ='Neutral'
                else:
                    if art['sentiment'] > 0:
                        imp1 = 'Positive'
                    else:
                        imp1 = 'Negative'


                textstream.objects.create(lang=art['lang'],source=art['source']['uri'],mytext=art['body'],impression=imp1,search=thesearch,creator=request.user)
        return HttpResponseRedirect(reverse('searchdetail', args=(pk,)))
    else:
        form = searchrunForm()
    return render(request, 'fin/searchdetails_form.html',{'form':form})

def searchrun3(request):
    er = EventRegistry(apiKey = 'f97425bc-cc68-4da2-a302-9be8eb8ad153')
    q = QueryArticlesIter(
        keywords = QueryItems.OR(["USA", "Canada"]),
        dataType = ["news", "blog"])
    # obtain at most 500 newest articles or blog posts
    result1 =  q.execQuery(er, sortBy = "date", maxItems = 1)
    return render(request, 'fin/result.html',{'result1':result1})
