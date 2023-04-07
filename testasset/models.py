from django.db import models

# Create your models here.

class Staff(models.Model):
    
    GENDER = (('Male', 'Male'),
            ('Female', 'Female'),('Others', 'Others'),)
    
    DEPARTMENT = (('ACC & Finance', 'ACC & Finance'),
                ('Admin', 'Admin'),
                ('Collection', 'Collection'),
                ('Credit', 'Credit'),('CS', 'CS'),('Marketing', 'Marketing'),('Mgmt', 'Mgmt'),
                ('HR', 'HR'),
                ('Mgmt', 'Mgmt'),('Planning', 'Planning'),('IT', 'IT'),)

    STATUS = (('Active', 'Active'),
            ('Resign', 'Resign'),)  
            
    POSITION = (('Executive', 'Executive'),
            ('Senior Executive', 'Senior Executive'), ('Team Lead', 'Team Lead'),('A.Manager', 'A.Manager'),
            ('Manager', 'Manager'), ('MD', 'MD'))                         

    employee_id = models.CharField(max_length=10, null=True )
    name = models.CharField(max_length=200, null=True )
    gender =  models.CharField(max_length=200, null=True, choices= GENDER)
    joining_date = models.DateField(null=True)
    email = models.CharField(max_length=200, null=True)
    department =  models.CharField(max_length=200, null=True, choices= DEPARTMENT)
    position = models.CharField(max_length=200, null=True, choices= POSITION)
    description = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, choices= STATUS, default=STATUS[0][0])

    def __str__(self):
        return self.employee_id
    
    
# class StaffResource(resources.ModelResource):

#     class Meta:
#         model = Staff
#         import_id_fields = '__all__'
#         # skip_unchanged = True
#         # use_bulk = True

class Categories(models.Model):
        
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Asset(models.Model):
#     CATEGORY = (('PC', 'PC'),
#                 ('Monitor', 'Monitor'),
#                 ('Headset', 'Headset'),
#                 ('Laptop', 'Laptop'),)

    STATUS = (('In Use', 'In Use'),
            ('Vacant', 'Vacant'),
            ('Disposed', 'Disposed'),
            ('Borrowed', 'Borrowed'),)

    LOCATION = (('PJ 5th', 'PJ 5th'),
            ('PJ 7th', 'PJ 7th'),
            ('PJ 11th', 'PJ 11th'),
            ('PG', 'PG'),('IPH', 'IPH'),('SBN', 'SBN'),('MLK', 'MLK'),('BP', 'BP'),('JB', 'JB'),
            ('KT', 'KT'),('Sabah', 'Sabah'),('SRK', 'SRK'),)            

    asset_no = models.CharField(max_length=200 )
    name = models.CharField(max_length=200, null=True)
    brand = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, choices= LOCATION)
    status = models.CharField(max_length=200, null=True, choices= STATUS, default=STATUS[1][1])
    serial_no = models.CharField(max_length=200)
    warranty_start = models.DateField(null=True)     
    warranty_end = models.DateField(null=True)

    categories = models.ForeignKey(Categories, null=True, on_delete = models.CASCADE)
    staff = models.ForeignKey(Staff, null=True, on_delete= models.SET_NULL)
       

    def __str__(self):
        return self.asset_no


# class Order(models.Model):
#     STATUS = (('In Use', 'In Use'),
#                 ('Vacant', 'Vacant'),
#                 ('Disposed', 'Disposed'),
#                 ('Borrowed', 'Borrowed'),)

#     staff = models.ForeignKey(Staff, null=True, on_delete= models.SET_NULL)
#     asset = models.ForeignKey(Asset, null=True, on_delete= models.SET_NULL)
#     date_assigned = models.DateField(default=datetime.date.today)      
#     status = models.CharField(max_length=200, null=True, choices= STATUS)

#     def __str__(self):
#         return self.asset.asset_no
