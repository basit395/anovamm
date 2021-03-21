from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class department(models.Model):
    departmentname = models.CharField("Department Name",max_length=25,null=True) #new
    def __str__(self):
        return str(self.departmentname)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    phone = models.CharField("Phon No",max_length=100,null=True)
    jobtitle = models.CharField("Job Title",max_length=100,null=True)
    department = models.ForeignKey(department,blank=True,null=True,on_delete=models.CASCADE,related_name='department_users',verbose_name ='Department') #new


    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
