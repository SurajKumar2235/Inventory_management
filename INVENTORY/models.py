from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# ======================================================================

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
# ======================================================================
class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

    class Meta:
        db_table='Category'
# ======================================================================


class Employees(models.Model):
    name=models.CharField(max_length=200,null=False,blank=False)
    quantity=models.IntegerField()
    category=models.ForeignKey('Category',on_delete=models.SET_NULL,blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name   

    class Meta:
        db_table='employee'

# ======================================================================

class inventory_History(models.Model):
    item_name=models.CharField(max_length=200,null=False,blank=False)
    item=models.ForeignKey(Inventory,on_delete=models.SET_NULL, blank=True, null=True)
    qty_purchased=models.IntegerField()
    price=models.ForeignKey('Category',on_delete=models.SET_NULL,blank=True,null=True)
    date_of_purchased=models.DateTimeField(auto_now_add=True)
    employee=models.ForeignKey(Employees,on_delete=models.CASCADE)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table='Inventory_history'

