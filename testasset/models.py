from django.db import models
import datetime
from django.urls import reverse
# Create your models here.

    
class Department(models.Model):
        
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    
    GENDER = (('Male', 'Male'),
            ('Female', 'Female'),('Others', 'Others'),)
            
    LOCATION = (('PJ 5th', 'PJ 5th'),
            ('PJ 7th', 'PJ 7th'),
            ('PJ 11th', 'PJ 11th'),
            ('PG', 'PG'),('IPH', 'IPH'),('SBN', 'SBN'),('MLK', 'MLK'),('BP', 'BP'),('JB', 'JB'),
            ('KT', 'KT'),('Sabah', 'Sabah'),('SRK', 'SRK'),)            
    

    STATUS = (('Active', 'Active'),
            ('Resign', 'Resign'),)  
            
    POSITION = (('Executive', 'Executive'),
            ('Senior Executive', 'Senior Executive'), ('Team Lead', 'Team Lead'),('A.Manager', 'A.Manager'),
            ('Manager', 'Manager'), ('MD', 'MD'))                         

    employee_id = models.CharField(max_length=10, default=None, blank= True, null=True, unique=True )
    name = models.CharField(max_length=200, null=True )
    gender =  models.CharField(max_length=200, null=True, choices= GENDER)
    joining_date = models.DateField(null=True)
    email = models.CharField(max_length=200, null=True)
    department =  models.ForeignKey(Department, default=None, on_delete= models.PROTECT)
    position = models.CharField(max_length=200, null=True, choices= POSITION)
    description = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, choices= LOCATION)
    printer_pw = models.CharField(max_length=7, null=True)
    status = models.CharField(max_length=200, null=True, choices= STATUS, default=STATUS[0][0])

    def __str__(self):
        return self.employee_id
    

class Categories(models.Model):
        
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Asset(models.Model):

    STATUS = (('In Use', 'In Use'),
            ('Vacant', 'Vacant'),
            ('Disposed', 'Disposed'),
            ('Borrowed', 'Borrowed'),)

    LOCATION = (('PJ 5th', 'PJ 5th'),
            ('PJ 7th', 'PJ 7th'),
            ('PJ 11th', 'PJ 11th'),
            ('PG', 'PG'),('IPH', 'IPH'),('SBN', 'SBN'),('MLK', 'MLK'),('BP', 'BP'),('JB', 'JB'),
            ('KT', 'KT'),('Sabah', 'Sabah'),('SRK', 'SRK'),)            

    asset_no = models.CharField(max_length=10, default=None, blank= True, null=True, unique=True )
    name = models.CharField(max_length=200, null=True)
    brand = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, choices= LOCATION)
    status = models.CharField(max_length=200, null=True, choices= STATUS, default=STATUS[1][1])
    serial_no = models.CharField(max_length=200)
    warranty_start = models.DateField(null=True)     
    warranty_end = models.DateField(null=True)

    categories = models.ForeignKey(Categories, default=None, on_delete= models.PROTECT)
    staff = models.ForeignKey(Staff, blank= True, null=True ,default=None, on_delete= models.SET_DEFAULT)
       

    def __str__(self):
        return self.asset_no


class Predict(models.Model):

    department =  models.ForeignKey(Department, null=True, default=None, on_delete= models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    date_predict = models.DateField(default=datetime.date.today)      
    

    def __str__(self):
        return "predict-{}".format( self.date_predict)
#     self.department.name


class Event(models.Model):
    asset_no = models.CharField(max_length=100, default=None, blank= True, null=True,)
    description = models.TextField(null=True)
    warranty_start = models.DateField(null=True)
    warranty_end = models.DateField(null=True)


    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.asset_no} </a>'