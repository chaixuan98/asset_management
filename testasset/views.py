from datetime import date
from msilib.schema import ListView
from pkgutil import get_data
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,  HttpResponseRedirect
from django.forms import formset_factory, inlineformset_factory
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib import messages
from qrcode import *
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from tablib import Dataset
from .resources import StaffResource, AssetResource

from django.db.models import Count

from .utils import Calendar
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
import calendar





# Create your views here.

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else: 
            messages.info(request, "Username OR password incorrect")
        

    context = {}

    return render(request,'testasset/login.html', context)

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name = 'normal staff')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username +' succesfully')

            return redirect('login')
        else:
            messages.info(request,form.errors )

    context = {'form':form}
    return render(request,'testasset/register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    
    staffs = Staff.objects.all()
    assets = Asset.objects.all()
    categories = Categories.objects.all()
    department = Department.objects.all()
    
    total_staffs = staffs.filter(status="Active").count()
    all_asset = assets.count()
    cat = categories.filter(asset__status="In Use").count()
    disposed = categories.filter(asset__status="Disposed").count()
    expired = assets.filter(warranty_end__lt = date.today()).count()


    dept_act  = Department.objects.filter(staff__status="Active").values('name').annotate(count_active=Count('staff')).values('name','count_active')
    dept_res  = Department.objects.filter(staff__status="Resign").values('name').annotate(count_resign=Count('staff')).values('name','count_resign')

    cat_inuse  = categories.filter(asset__status="In Use").values('name').annotate(count_inuse=Count('asset')).values('name','count_inuse')
    cat_vac  = categories.filter(asset__status="Vacant").values('name').annotate(count_vacant=Count('asset')).values('name','count_vacant')
    

    context = {'staffs': staffs, 'assets':assets, 'categories':categories, 'department':department, 'total_staffs':total_staffs, 'all_asset':all_asset, 'disposed':disposed, 'expired': expired,'cat':cat,
               'dept_act': dept_act, 'dept_res':dept_res, 'cat_vac':cat_vac, 'cat_inuse':cat_inuse }

    return render(request, 'testasset/dashboard.html', context)


@login_required(login_url='login')
@admin_only
def assets(request):
    assets = Asset.objects.all()
    categories = Categories.objects.all()
    department = Department.objects.all()

    CATID = request.GET.get('categories')
    if CATID:
        assets = Asset.objects.filter(categories = CATID)
        total_assets = assets.filter(categories=CATID).count()
        total_inuse = assets.filter(categories=CATID, status='In Use').count()
        total_borrowed = assets.filter(categories= CATID, status='Borrowed').count()
        total_disposed = assets.filter(categories= CATID, status='Disposed').count()
        total_vacant = assets.filter(categories=CATID, status='Vacant').count()
        expired = assets.filter(categories=CATID, warranty_end__lt = date.today()).count()

    else:
        assets = Asset.objects.all()
        total_assets = assets.count()
        total_inuse = assets.filter(status='In Use').count()
        total_borrowed = assets.filter( status='Borrowed').count()
        total_disposed = assets.filter( status='Disposed').count()
        total_vacant = assets.filter(status='Vacant').count()
        expired = assets.filter(warranty_end__lt = date.today()).count()



    context = {'assets':assets, 'categories':categories,'department':department,'total_assets':total_assets,'total_inuse':total_inuse, 'total_borrowed':total_borrowed,
    'total_disposed':total_disposed, 'total_vacant':total_vacant, 'expired':expired}

    return render(request, 'testasset/assets.html', context)


# def view_details(request, code = None):
#     if code is None:
#         return HttpResponse("Asset Code is Invalid")
#     else:
#         assets = Asset.objects.get(asset_no=code)

#     context = {'assets':assets,}    
#     return render(request, 'testasset/view_asset_details.html', context)


@login_required(login_url='login')
@admin_only
def viewScanner(request):
    
    return render(request, 'testasset/scanner.html')


@login_required(login_url='login')
@admin_only
def createAsset(request):

    form =  AssetForm()
    event_form =  EventForm()
    categories = Categories.objects.all()
    departments = Department.objects.all()
    # event = Event.objects.all()
    # assets = Asset.objects.all()
  

    if request.method == 'POST':
        form = AssetForm(request.POST)
        event_form = EventForm(request.POST)
        if form.is_valid() and event_form.is_valid():
       
            form = form.save()
            event_form.save() 
            # form = form.save(commit=False)
            
       
            # event= event_form.save(commit=False)
            # event.form = form
            # event.save()

            
            # HttpResponse("Asset has been added successfully")
            messages.success(request, 'Add Asset Sucessfully')
          
            return redirect('assets')
    else:
            form = AssetForm()
          

    context = {'form':form, 'categories':categories, 'departments':departments, 'event_form':event_form}
    return render(request, 'testasset/create_asset.html', context)

@login_required(login_url='login')
@admin_only
def updateAsset(request,pk):

    departments = Department.objects.all()
    asset = Asset.objects.get(asset_no=pk)
    categories = Categories.objects.all()
    form = AssetForm(instance=asset)

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()

            return redirect('/assets/')
        
    context = {'form':form, 'categories':categories, 'asset':asset, 'departments':departments}
    return render(request, 'testasset/update_asset.html', context)

@login_required(login_url='login')
@admin_only
def deleteAsset(request, pk):

    asset = Asset.objects.get(asset_no=pk)
    
    if request.method == 'POST':
        asset.delete()
        return redirect('/assets/')

    context = {'item':asset}
    return render(request, 'testasset/delete_asset.html', context )


@login_required(login_url='login')  
@admin_only
def importExcelAsset(request):
    if request.method == 'POST':
        asset_resource =AssetResource()
        dataset = Dataset()
        new_assets = request.FILES['asset_file']
        data_imported = dataset.load(new_assets.read())
        result = asset_resource.import_data(dataset,dry_run=True, raise_errors=True)
       
        if not result.has_errors():
            asset_resource.import_data(dataset,dry_run=False)
        
        return redirect('/assets')   
    return render(request, 'testasset/import_asset.html')

  
@login_required(login_url='login')
@admin_only
def allStaffs(request):
    staffs = Staff.objects.all()
    department = Department.objects.all()
    categories = Categories.objects.all()

    DEPID = request.GET.get('department')
    if DEPID:
        staffs = Staff.objects.filter(department = DEPID)
        total_active = staffs.filter(department=DEPID, status='Active').count()
        total_resign = staffs.filter(department=DEPID, status='Resign').count()
   
    else:
        staffs = Staff.objects.all()
        total_active = staffs.filter(status='Active').count()
        total_resign = staffs.filter(status='Resign').count()

    # active_count = staffs.filter(status='Active').count()
    # resign_count = staffs.filter(status='Resign').count()

    context = {'staffs':staffs, 'categories':categories,  'department':department, 
               'total_active':total_active, 'total_resign':total_resign }

    return render(request, 'testasset/all_staffs.html',context)
    
@login_required(login_url='login')
@admin_only
def staff(request, pk):
    staff =  Staff.objects.get(employee_id=pk)
    department = Department.objects.all()
    categories = Categories.objects.all()
    assets = staff.asset_set.all()
    assets_count = assets.count()

    context = {'staff':staff, 'categories':categories, 'assets':assets, 'assets_count':assets_count, 'department':department}

    return render(request, 'testasset/staff.html', context)

@login_required(login_url='login')
@admin_only
def createStaff(request):

    # staff = Staff.objects.all()
    categories = Categories.objects.all()
    department = Department.objects.all()
    form =  StaffForm()

    if request.method == 'POST':
        form = StaffForm(request.POST)

        if form.is_valid():
            # new_item = form.save(commit=False)
            # new_item.owner = request.user
            form.save()
            messages.success(request, 'Add staff sucessfully.')
            return redirect('/all_staffs')
    else:
            form = StaffForm()

    context = {'form':form, 'categories':categories, 'department':department}
    return render(request, 'testasset/create_staff.html', context)

@login_required(login_url='login')  
@admin_only
def updateStaff(request,pk):
    categories = Categories.objects.all()
    department = Department.objects.all()
    staff = Staff.objects.get(employee_id=pk)
    form = StaffForm(instance=staff)

    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('/all_staffs')
        
    context = {'form':form, 'categories':categories, 'department':department}
    return render(request, 'testasset/create_staff.html', context)

@login_required(login_url='login')  
@admin_only
def importExcelStaff(request):
    if request.method == 'POST':
        staff_resource =StaffResource()
        dataset = Dataset()
        new_staffs = request.FILES['my_file']
        data_imported = dataset.load(new_staffs.read())
        result = staff_resource.import_data(dataset,dry_run=True, raise_errors=True)
       
        if not result.has_errors():
            staff_resource.import_data(dataset,dry_run=False)
        
        return redirect('/all_staffs')   
    return render(request, 'testasset/import_staff.html')


class CalendarView(generic.ListView):
 
    model = Event
    template_name = 'testasset/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['categories'] = Categories.objects.all()
        context['department'] = Department.objects.all()
 
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, pk=None):
    categories = Categories.objects.all()
    department = Department.objects.all()
    instance = Event()
    if pk:
        instance = get_object_or_404(Event, pk=pk)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return redirect('/calendar')
    
    context = {'form':form, 'categories':categories, 'department':department}
    return render(request, 'testasset/event.html', context)


@login_required(login_url='login')
@admin_only
def viewCategories(request):
    staffs = Staff.objects.all()
    department = Department.objects.all()
    cat = Categories.objects.all()

    total_categories = cat.count()

    context = {'staffs':staffs, 'cat':cat,  'department':department, 'total_categories':total_categories }

    return render(request, 'testasset/view_categories.html',context)


@login_required(login_url='login')
@admin_only
def addCategories(request):

    categories = Categories.objects.all()
    department = Department.objects.all()
    form =  AddCategoriesForm()

    if request.method == 'POST':
        form = AddCategoriesForm(request.POST)

        if form.is_valid():
         
            form.save()
            messages.success(request, 'Add Categories sucessfully.')
            return redirect('/view_categories')
    else:
            form = AddCategoriesForm()

    context = {'form':form, 'categories':categories, 'department':department}
    return render(request, 'testasset/add_categories.html', context)

@login_required(login_url='login')
@admin_only
def updateCategories(request,pk):

    departments = Department.objects.all()
    asset = Asset.objects.all()
    cat = Categories.objects.get(name=pk)
    form = CategoriesForm(instance=cat)

    if request.method == 'POST':
        form = CategoriesForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Categories sucessfully.')
            return redirect('/view_categories/')
        
    context = {'form':form, 'cat':cat, 'asset':asset, 'departments':departments}
    return render(request, 'testasset/add_categories.html', context)

@login_required(login_url='login')
@admin_only
def deleteCategories(request, pk):

    categories = Categories.objects.get(name=pk)
    
    if request.method == 'POST':
        categories.delete()
        messages.success(request, 'Delete Categories sucessfully.')
        return redirect('/view_categories/')

    context = {'item':categories}
    return render(request, 'testasset/delete_categories.html', context )


@login_required(login_url='login')
@admin_only
def viewDepartment(request):
    staffs = Staff.objects.all()
    department = Department.objects.all()
    categories = Categories.objects.all()

    total_departments = department.count()

    context = {'staffs':staffs, 'categories':categories,  'department':department, 'total_departments':total_departments }

    return render(request, 'testasset/view_departments.html',context)
    

@login_required(login_url='login')
@admin_only
def addDepartment(request):

    categories = Categories.objects.all()
    department = Department.objects.all()
    form =  AddDepartmentForm()

    if request.method == 'POST':
        form = AddDepartmentForm(request.POST)

        if form.is_valid():
         
            form.save()
            messages.success(request, 'Add Department sucessfully.')
            return redirect('/view_department')
    else:
            form = AddDepartmentForm()

    context = {'form':form, 'categories':categories, 'department':department}
    return render(request, 'testasset/add_department.html', context)

@login_required(login_url='login')
@admin_only
def updateDepartment(request,pk):

    departments = Department.objects.get(name=pk)
    asset = Asset.objects.all()
    categories = Categories.objects.all()
    form = DepartmentForm(instance=departments)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=departments)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Department sucessfully.')
            return redirect('/view_department/')
        
    context = {'form':form, 'categories':categories, 'asset':asset, 'departments':departments}
    return render(request, 'testasset/add_department.html', context)

@login_required(login_url='login')
@admin_only
def deleteDepartment(request, pk):

    departments = Department.objects.get(name=pk)
    
    if request.method == 'POST':
        departments.delete()
        messages.success(request, 'Delete Department sucessfully.')
        return redirect('/view_department/')

    context = {'item':departments}
    return render(request, 'testasset/delete_department.html', context )



@login_required(login_url='login')
@admin_only
def predictAsset(request):

    department = Department.objects.all()
    categories = Categories.objects.all()

    
    # PredictFormSet = inlineformset_factory(Department, Predict, fields=('quantity','department',),extra=3)

    # formset =  PredictFormSet(queryset=Department.objects.none()) #if queryset will no display exist asset, extra 3


    # form =  PredictForm()

    PredictFormSet = formset_factory(PredictForm, extra = 8)
    formset = PredictFormSet(request.POST or None)

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = PredictForm(request.POST)
        formset =  PredictFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                # print(form)
                # form.save()
                print(form.cleaned_data)
               
            # return redirect('predict_asset')
                if form["department"] == 'Collection':
                    print('true')
                    print(categories.filter(name='Laptop').count)
                    # totalcat -= 1
                    # print(totalcat)
      
            # for form in formset:
                # print(formset.cleaned_data)

                # if formset.cleaned_data.department == 'Collection':
                #     totalcat = categories.filter(name='Laptop').count
                #     totalcat -= 1
                #     print(totalcat)
        
    # else:
    #          PredictFormSet = formset_factory(PredictForm, extra = 8)



    context = { 'formset':formset}
    return render(request, 'testasset/predict_asset.html', context)



# @login_required(login_url='login')
# @admin_only
# def assignAsset(request, pk):
#     OrderFormSet = inlineformset_factory(Staff, Order, fields=('asset', 'status'),extra=3)
#     staff = Staff.objects.get(employee_id=pk)
#     formset =  OrderFormSet(queryset=Order.objects.none(),instance=staff) #if queryset will no display exist asset, extra 3
#     # form =  OrderForm(initial= {'customer':customer})

#     if request.method == 'POST':
#         # print('Printing POST:', request.POST)
#         # form = OrderForm(request.POST)
#         formset =  OrderFormSet(request.POST, instance=staff)
#         if formset.is_valid():
#             formset.save()
#             return redirect('all_staffs')

#     context = {'formset':formset}
#     return render(request, 'testasset/asset_assign_form.html', context)

# @login_required(login_url='login')
# @admin_only
# def updateAssignAsset(request,pk):

#     order = Order.objects.get(id=pk)
#     form = OrderForm(instance=order)

#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('all_staffs')
        
#     context = {'form':form}
#     return render(request, 'testasset/update_assign_asset.html', context)

# @login_required(login_url='login')   
# @admin_only
# def deleteAssignAsset(request, pk):

#     order = Order.objects.get(id=pk)
    
#     if request.method == 'POST':
#         order.delete()
#         return redirect('all_staffs')

#     context = {'item':order}
#     return render(request, 'testasset/delete_asset_assign.html', context)