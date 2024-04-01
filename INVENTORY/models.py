from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Inventory(models.Model):
    name=models.CharField(max_length=200,null=False,blank=False)
    quantity=models.IntegerField()
    category=models.ForeignKey('Category',on_delete=models.SET_NULL,blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table='Inventory'

class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

    class Meta:
        db_table='Category'

