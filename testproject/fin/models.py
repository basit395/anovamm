from django.db import models

import datetime
from datetime import timedelta
from datetime import date
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import  get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count , Sum , Avg


def defaultcategory():
    return category.objects.get(id=1)

def defaultsearch():
    return search.objects.get(id=1)

class incomesource(models.Model):
    sourcename =  models.CharField("Income Source",max_length=30)

    def __str__(self):
        return self.sourcename

class category(models.Model):
    categoryname =  models.CharField("Category Name",max_length=30)

    def __str__(self):
        return self.categoryname

class item(models.Model):
    itemname =  models.CharField("Item Name",max_length=30)
    category = models.ForeignKey(category,null=True , on_delete=models.CASCADE,related_name='item_factory',default=defaultcategory)

    def __str__(self):
        return self.itemname

class finbook(models.Model):

    # fincat = (
    #         ('expenses', 'expenses'),
    #         ('income', 'income'),
    #         )
    description = models.CharField("Discreption",max_length=2000)
    clarification = models.CharField("Clarification",max_length=2000,default="No thing")
    transactionc = models.CharField("Transaction Category",max_length=20,default="No thing")
    amount = models.DecimalField(max_digits=9, decimal_places=2,default=0)
    creationdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now=True)
    transactiondate = models.DateField("Transaction Date",default=timezone.now())
    incomesource = models.CharField(max_length=20,default="No thing")
    category = models.ForeignKey(category,null=True , on_delete=models.CASCADE,related_name='category_fin',default=defaultcategory)
    department = models.CharField(max_length=20,default="No thing")
    subdepartment = models.CharField(max_length=20,default="No thing")
    note = models.CharField("Note",max_length=200,null=True,blank=True)
    fyear = models.IntegerField(default=0)
    fmonth = models.IntegerField(default=0)
    fday = models.IntegerField(default=0)




    def save(self, *args, **kwargs):
         list1 = ["سحب","مشتريات","شراء","مدفوعات","حوالة صادرة"]
         for ex in list1 :
             if ex in self.description:
                 self.transactionc ="expenses"
                 break

         list2 = ["حوالة واردة","ايداع"]
         for ex in list2 :
             if ex in self.description:
                 self.transactionc ="income"
                 break

         self.note = self.description.split()
         rr = "مبلغ:"
         if rr in self.note:
             xx = self.note.index("مبلغ:")
             yy = xx+1
             self.amount = self.note[yy]

         for mm in self.note:
             if '/' in mm:

                    self.transactiondate = datetime.date(int(mm[0:4]), int(mm[5:7]), int(mm[8:10]))

         if self.clarification == 'ncc':
             self.transactionc ="income"
             self.amount = 17500

         if "MAMA NOURA" in self.description:
             self.category = 'Food'

         if 'me' in self.clarification:
             self.department = 'Me'
             self.subdepartment = 'Me'

         if 'batool' in self.clarification:
             self.department = 'H1'
             self.subdepartment = 'Batool'

         if 'h1' in self.clarification:

             self.department = 'H1'
             self.subdepartment = 'H1'

         if 'h2' in self.clarification:

             self.department = 'H2'
             self.subdepartment = 'H2'
             self.amount = self.clarification.split()[1]



         super(finbook, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.amount)

    def get_absolute_url(self):
        return reverse('transactiondetail',kwargs={'pk':self.pk})


class project(models.Model):
    projectname = models.CharField("Project",max_length=200)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_projects',verbose_name ='Creator')
    creationdate = models.DateTimeField(auto_now_add=True)
    note = models.CharField("Note",max_length=200)

    def __str__(self):
        return self.projectname

    def get_absolute_url(self):
        return reverse('projectdetail',kwargs={'pk':self.pk})

class search(models.Model):
    searchname = models.CharField("Search",max_length=200)
    project = models.ForeignKey(project,on_delete=models.CASCADE,related_name='project_searches',verbose_name ='Search')
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_searches',verbose_name ='Creator')
    creationdate = models.DateTimeField(auto_now_add=True)
    note = models.CharField("Note",max_length=20,default=" ")

    def __str__(self):
        return self.searchname


class textstream(models.Model):
    source = models.CharField("Source",max_length=200)
    mytext = models.TextField("Text",null=True,blank=True)
    impression = models.CharField("Impression",max_length=2000,default="Neutral")
    emotion = models.CharField("Emotion",max_length=200,default="No thing")
    score = models.IntegerField(default=0)
    mylength = models.IntegerField(null=True,blank=True)
    frequency = models.IntegerField(null=True,blank=True)
    lang = models.CharField("Language",max_length=20,default="No thing")
    location = models.CharField("Location",max_length=20,default="No thing")
    note = models.CharField("Note",max_length=20,default="")
    creationdate = models.DateTimeField(auto_now_add=True)
    textdomain = models.CharField("Domain",max_length=200,default="No thing")
    search = models.ForeignKey(search,on_delete=models.CASCADE,related_name='search_texts',verbose_name ='Search',default=defaultsearch)
    keyword1 = models.CharField("keyword1",max_length=200,null=True,blank=True)
    keyword2 = models.CharField("keyword2",max_length=200,null=True,blank=True)
    maxitems = models.IntegerField(default=10)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_textstream',verbose_name ='Creator')

    class Meta:
        ordering = ['-creationdate']

    def __str__(self):
        return self.mytext


class datasource(models.Model):
    sourcename = models.CharField("Source Name",max_length=200)

    def __str__(self):
        return self.sourcename

class projectarea(models.Model):
    projectname = models.CharField("Project Name",max_length=200)
    datasource = models.ForeignKey(datasource,null=True , on_delete=models.CASCADE,related_name='source_project')

    def __str__(self):
        return self.projectname

class sentmentlist(models.Model):
    myword = models.CharField("Word",max_length=200,unique=True)
    imporession = models.CharField("Impression",max_length=200)

    def __str__(self):
        return self.myword

class searchdetails(models.Model):

    keyword1 = models.CharField("keyword1",max_length=200,null=True,blank=True)
    keyword2 = models.CharField("keyword2",max_length=200,null=True,blank=True)
    maxitems = models.IntegerField(default=10)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_searchdetails',verbose_name ='Creator')
    creationdate = models.DateTimeField(auto_now_add=True)
    search = models.ForeignKey(search,on_delete=models.CASCADE,related_name='search_searchdetails',verbose_name ='Search',default=defaultsearch )
