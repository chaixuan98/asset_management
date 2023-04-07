from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import StaffForm, AssetForm, CreateUserForm
from django.contrib import messages
from qrcode import *
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from tablib import Dataset
from .resources import StaffResource



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

    context = {'form':form}
    return render(request,'testasset/register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    # orders = Order.objects.all()
    staffs = Staff.objects.all()
    assets = Asset.objects.all()
    categories = Categories.objects.all()

    # total_staffs = staffs.count()
    # total_orders = orders.count()
    # in_use = orders.filter(status='In Use').count()
    # vacant = orders.filter(status='Vacant').count()
    
    CATID = request.GET.get('categories')
    if CATID:
        assets = Asset.objects.filter(categories = CATID)
    else:
        assets = Asset.objects.all()

    context = {'staffs': staffs, 'assets':assets, 'categories':categories, }

    return render(request, 'testasset/dashboard.html', context)

@login_required(login_url='login')
@admin_only
def assets(request):
    assets = Asset.objects.all()
    categories = Categories.objects.all()

    CATID = request.GET.get('categories')
    if CATID:
        assets = Asset.objects.filter(categories = CATID)
        total_assets = assets.filter(categories=CATID).count()
        total_inuse = assets.filter(categories=CATID, status='In Use').count()
        total_borrowed = assets.filter(categories= CATID, status='Borrowed').count()
        total_disposed = assets.filter(categories= CATID, status='Disposed').count()
        total_vacant = assets.filter(categories=CATID, status='Vacant').count()
    else:
        assets = Asset.objects.all()
        total_assets = assets.count()
        total_inuse = assets.filter(status='In Use').count()
        total_borrowed = assets.filter( status='Borrowed').count()
        total_disposed = assets.filter( status='Disposed').count()
        total_vacant = assets.filter(status='Vacant').count()


    context = {'assets':assets, 'categories':categories,'total_assets':total_assets,'total_inuse':total_inuse, 'total_borrowed':total_borrowed,
    'total_disposed':total_disposed, 'total_vacant':total_vacant}

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
    categories = Categories.objects.all()
    

    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            HttpResponse("Asset has been added successfully")
            messages.success(request, 'Sucessfully added asset.')
            # img = make(data)
            # img_name = 'qr' +  + '.png'
            # img.save("static/image/test.png")
            return redirect('assets')
    else:
            form = AssetForm()

    context = {'form':form, 'categories':categories,}
    return render(request, 'testasset/create_asset.html', context)

@login_required(login_url='login')
@admin_only
def updateAsset(request,pk):

    asset = Asset.objects.get(asset_no=pk)
    categories = Categories.objects.all()
    form = AssetForm(instance=asset)

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()

            return redirect('/assets/')
        
    context = {'form':form, 'categories':categories, 'asset':asset}
    return render(request, 'testasset/update_asset.html', context)

@login_required(login_url='login')
@admin_only
def deleteAsset(request, pk):

    asset = Asset.objects.get(asset_no=pk)
    
    if request.method == 'POST':
        asset.delete()
        return redirect('/assets/')

    context = {'item':asset, }
    return render(request, 'testasset/delete_asset.html', context)

  
@login_required(login_url='login')
@admin_only
def allStaffs(request):
    staffs = Staff.objects.all()
    categories = Categories.objects.all()

    context = {'staffs':staffs, 'categories':categories }

    return render(request, 'testasset/all_staffs.html',context)
    
@login_required(login_url='login')
@admin_only
def staff(request, pk):
    staff =  Staff.objects.get(employee_id=pk)
    categories = Categories.objects.all()
    assets = staff.asset_set.all()
    assets_count = assets.count()

    # orders = staff.order_set.all()
    # order_count = orders.count()

    context = {'staff':staff, 'categories':categories, 'assets':assets, 'assets_count':assets_count}

    return render(request, 'testasset/staff.html', context)

@login_required(login_url='login')
@admin_only
def createStaff(request):

    # staff = Staff.objects.all()
    categories = Categories.objects.all()
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

    context = {'form':form, 'categories':categories,}
    return render(request, 'testasset/create_staff.html', context)

@login_required(login_url='login')  
@admin_only
def updateStaff(request,pk):
    categories = Categories.objects.all()
    staff = Staff.objects.get(employee_id=pk)
    form = StaffForm(instance=staff)

    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('/all_staffs')
        
    context = {'form':form, 'categories':categories,}
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