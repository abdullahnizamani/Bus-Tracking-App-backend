from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST #
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError,ObjectDoesNotExist 
from users.serializers import LoginSerializer
from users.models import User, Driver, Student
from transport.models import Bus, Route
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import BusForm, UserForm, UpdateUserForm
import json
from django.contrib.auth.hashers import make_password
import csv
from django.urls import reverse
from firebase_admin import db
from BusCore import firebase  # ensures Firebase is initialized

# Create your views here.

@login_required(login_url='login')
def index(request):
    student_count = User.objects.filter(role="student").count()
    driver_count = User.objects.filter(role="driver").count()
    buses_count = Bus.objects.count()
    ref = db.reference() 
    buses = ref.get() or {}
    active_bus_count = sum(
        1
        for bus in buses.get('buses', {}).values()
        if bus.get('status', {}).get('isActive') is True
    )
    ctx = {"student_count":student_count, "driver_count":driver_count, "buses_count":buses_count, 'buses':active_bus_count}
    return render(request, 'index.html', ctx)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect username or password")
            return redirect('login')
        if not user.is_staff:
            messages.error(request, "You are not authorized to access this area")
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, "Login successful")
        return redirect('dashboard')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def buses(request):
    busObj = Bus.objects.all()
    return render(request, 'buses.html', {"busObj":busObj})

@login_required(login_url='login')
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        route_json = request.POST.get('coordinates')  # JSON from Mapbox
        route_str = request.POST.get('route_str')      # Optional: descriptive route string
        if form.is_valid():
            bus = form.save()
            Route.objects.create(
                    bus=bus,
                    path=json.loads(route_json),
                    route_str=route_str
                )
        return redirect('buses')
    else:
        form = BusForm()
        return render(request, "add_bus.html", {"form": form})
    
@require_POST
def delete_bus(request):
        id = request.POST.getlist('checkbox-delete')
        if not id:
            messages.error(request, "No buses selected")

            return redirect('buses')
        else:
            deleted_objs, details= Bus.objects.filter(id__in=id).delete()
            buses_deleted = details.get('transport.Bus', 0)
            if buses_deleted >= 1:
                messages.success(request, f'Successfully deleted {buses_deleted} buses')
                return redirect('buses')
            else:
                messages.error(request, "there was an error deleting the buses")

                return redirect('buses')

@login_required(login_url='login')
def students(request):
    students = Student.objects.select_related('user')
    buses = Bus.objects.all()
    # students = Student.objects.select_related('user', 'bus_id')

    search = request.GET.get('search')
    bus = request.GET.get('bus')
    status = request.GET.get('status')

    if search:
        students = students.filter(
            Q(user__first_name__icontains=search) |
            Q(student_id__icontains=search)
        )

    if bus:
        students = students.filter(bus_id__id=bus)

    if status:
        students = students.filter(user__is_active=(status == "Active"))

    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    p = Paginator(students, page_size)
    page_obj = p.get_page(page_number)
    ctx = {
        'students':page_obj,
        'page_obj':page_obj,
        'paginator':page_obj,
        'buses':buses,
    }
    return render(request, 'students.html', ctx)


@login_required(login_url='login')
def add_student(request):
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_role_form':

            form = UserForm(request.POST, request.FILES)
            student_id = request.POST.get('Student_id')
            bus_id = request.POST.get('bus')
            if form.is_valid():
                user = form.save(commit=False)
                user.username = student_id
                user.password = make_password(student_id)  # Ensure the password is hashed
                user.role = 'student'
                try:
                    user.save()  # Save the user to the database
                    bus = Bus.objects.get(id=bus_id)
                    Student.objects.create(student_id=student_id, bus=bus, user=user)
                    messages.success(request, 'Successfully created student')
                    return redirect('students')
                except Bus.DoesNotExist:
                    messages.error(request, f"Bus with ID {bus_id} does not exist.")
                    return redirect('add_students')
                except IntegrityError:
                    messages.error(request, f"User with username {student_id} already exists.")
                    return redirect('add_students')
                except Exception as e:
                    messages.error(request, f"An unexpected error occurred: {e}")
                    return redirect('add_students')
            else:
                return redirect('add_students')
        else:
            csv_file = request.FILES['csv_file']
            data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=',')
            users_to_create = []
            students_to_create = []
            bus_mapping = {}  # Caching buses to avoid multiple DB hits
            header = True  # Flag to skip the header row
            for row in data:
                if header:  # Skip the header row
                    header = False
                    continue

            # for row in data:
                first_name, last_name, email, phone, student_id, bus_id = row
                try:
                    bus_id = int(bus_id)
                except ValueError:
                    messages.error(request, f"Invalid bus_id value: {bus_id}. Skipping this record.")
                    continue  # Skip this row if bus_id is invalid

                # Prepare user profile data
                user_profile = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=student_id,
                    password=make_password(student_id),
                    role='student',
                    email=email,
                    phone=phone,
                )
                users_to_create.append(user_profile)
                if bus_id not in bus_mapping:
                    try:
                        bus_mapping[bus_id] = Bus.objects.get(id=bus_id)
                    except Bus.DoesNotExist:
                        messages.error(request, f"Bus with ID {bus_id} does not exist. Skipping student.")
                        continue  # Skip this row if bus does not exist

                bus = bus_mapping[bus_id]
                student = Student(
                    student_id=student_id,
                    bus_id=bus,
                    user=user_profile
                )
                students_to_create.append(student)
            try:
                with transaction.atomic():
                    User.objects.bulk_create(users_to_create)
                    Student.objects.bulk_create(students_to_create)
                messages.success(request, 'Successfully added students from CSV file.')
                return redirect('students')
            except IntegrityError as e:
                messages.error(request, f"Error: Integrity issue - {str(e)}. Could not add some users.")
            except ValidationError as e:
                messages.error(request, f"Error: Validation error - {str(e)}.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                return redirect('add_students')
    buses = Bus.objects.all()
    form = UserForm()
    ctx = {'role':'Student', 'form':form, 'buses':buses}
    return render(request, 'add_users.html', ctx)



@login_required(login_url='login')
def drivers(request):
    drivers = Driver.objects.select_related('user').prefetch_related('bus')

    search = request.GET.get('search')
    bus = request.GET.get('bus')
    status = request.GET.get('status')

    if search:
        drivers = drivers.filter(
            Q(user__first_name__icontains=search) |
            Q(license_id__icontains=search)
        )

    if bus:
        drivers = drivers.filter(bus__id=bus)

    if status:
        drivers = drivers.filter(user__is_active=(status == "Active"))

    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    p = Paginator(drivers, page_size)

    page_obj = p.get_page(page_number)
    ctx = {
        'drivers':page_obj,
        'page_obj':page_obj,
        'paginator':page_obj,
        'buses': Bus.objects.all(),
    }
    return render(request, 'drivers.html', ctx)


@login_required(login_url='login')
def add_driver(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_role_form':


            form = UserForm(request.POST, request.FILES)
            driver_id = request.POST.get('Driver_id')
            license_id = request.POST.get('license_id')
            if driver_id=='' or license_id=='':
                messages.error(request, 'Make sure to fill the required fields')
                return redirect('add_drivers')
            if form.is_valid():
                user = form.save(commit=False)
                user.username = driver_id
                user.password = make_password(driver_id)  # Ensure the password is hashed
                user.role = 'driver'
                user.save()  # Save the user to the database
                Driver.objects.create(employee_id=driver_id, license_id=license_id, user=user)
                messages.success(request, 'Successfully created driver')
                return redirect('drivers')
            else:
                return redirect('add_students')

        else:
            csv_file = request.FILES['csv_file']
            data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=',')
            users_to_create = [] 
            drivers_to_create = []
            header = True  # Flag to skip the header row
            for row in data:
                if header:  # Skip the header row
                    header = False
                    continue

            # for row in data:
                first_name, last_name, email, phone, driver_id, license_id = row

                # Prepare user profile data
                user_profile = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=driver_id,
                    password=make_password(driver_id),
                    role='driver',
                    email=email,
                    phone=phone,
                )
                users_to_create.append(user_profile)

                driver = Driver(
                    employee_id=driver_id,
                    license_id=license_id,
                    user=user_profile
                )
                drivers_to_create.append(driver)
            try:
                with transaction.atomic():
                    User.objects.bulk_create(users_to_create)
                    Driver.objects.bulk_create(drivers_to_create)
                messages.success(request, 'Successfully added drivers from CSV file.')
                return redirect('drivers')
            except IntegrityError as e:
                messages.error(request, f"Error: Integrity issue - {str(e)}. Could not add some users.")
            except ValidationError as e:
                messages.error(request, f"Error: Validation error - {str(e)}.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                return redirect('add_drivers')
 
    buses = Bus.objects.all()
    form = UserForm()
    ctx = {'role':'Driver', 'form':form, 'buses':buses}
    return render(request, 'add_users.html', ctx)

@require_POST
def bulk_delete(request):
    
    ids = request.POST.get('ids').split(',')
    role = request.POST.get('role')
    data = User.objects.filter(username__in=ids, is_superuser=False).delete()
    # print(data)
    if not ids:
        messages.error(request, "No users selected.")
        return redirect('students' if role == 'student' else 'drivers')
    if data[0]>0:
        users_deleted = data[1]['users.User']
        if users_deleted>0:
            messages.success(request, f'Successfully deleted {users_deleted} users')
            return redirect('students' if role == 'student' else 'drivers')
        else:
            messages.error(request, f'There was an issue deleting the users')
            return redirect('students' if role == 'student' else 'drivers')
    else:
            messages.error(request, f'There was an issue deleting the users')

            return redirect('students' if role == 'student' else 'drivers')
    

@require_POST
def bulk_assign(request):
    ids = request.POST.get('ids').split(',')
    bus_id = request.POST.get('bus_id')
    bus = Bus.objects.get(id=bus_id)
    data = Student.objects.filter(student_id__in=ids).update(bus_id=bus)
    if data > 0:
            messages.success(request, f'Successfully assigned the selected bus to {data} users')
            return redirect('students')        
    else:
            messages.error(request, f'There was an issue assigning the buses')
            return redirect('students')
    


@require_POST
def bulk_remove_bus(request):
    ids = request.POST.get('ids').split(',')
    role = request.POST.get('role')
    if role == 'student':
        data = Student.objects.filter(student_id__in=ids).update(bus_id=None)
        if data>0:
                messages.success(request, f'Successfully removed bus assignments of {data} users')
                return redirect('students' if role == 'student' else 'drivers')
        else:
                messages.error(request, f'There was an issue deleting the assignments')
                return redirect('students' if role == 'student' else 'drivers')
    else:
        driver_ids = Driver.objects.filter(employee_id__in=ids).values_list('id', flat=True)

        data = Bus.objects.filter(driver_id__in=driver_ids).update(driver_id=None)

        if data>0:
                messages.success(request, f'Successfully removed bus assignments of {data} users')
                return redirect('drivers')
        else:
                messages.error(request, f'There was an issue deleting the assignments')
                return redirect('drivers')

@login_required(login_url='login')
def profile(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated your profile')
            return redirect('profile')
        else:
             messages.error(request, 'There was an error updating your profile. Please check the form below.')
    else:
        form = UpdateUserForm(instance=request.user)
    ctx = {'form':form}
    return render(request, 'profile.html', ctx)


@require_POST
def password_reset(request):
    role = request.POST.get('role')
    id = request.POST.get('ids')
    user = User.objects.filter(username=id).update(password=make_password(id))
    if user>0:
        messages.success(request, 'Successfully reset the password')
        return redirect('students' if role=='student' else 'drivers')

    else:
        messages.error(request, 'There was an error resetting the password please try again later')
        return redirect('students' if role=='student' else 'drivers')
 


@login_required(login_url='login')
def edit_driver(request, id):
    

    user = get_object_or_404(User, username=id)

    if user.role=='student':
        messages.error(request, 'The user must be a driver')
        return redirect('drivers')
    else:
        if request.method == 'POST':
            form = UpdateUserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                
                form.save()
                new_id = form.cleaned_data['username']
                Driver.objects.filter(employee_id=id).update(employee_id=new_id)
                messages.success(request, 'Successfully updated the driver profile')
                return redirect(reverse('edit_driver', args=[new_id]))
            else:
                messages.error(request, 'There was an error updating the profile. Please check the form below.')
        else:

            form = UpdateUserForm(instance=user)
        ctx = {'form':form, 'role':'Driver', 'user':user}
        return render(request, 'user_profile.html', ctx)

@login_required(login_url='login')
def edit_student(request, id):
    user = get_object_or_404(User, username=id)

    if user.role=='driver':
        messages.error(request, 'The user must be a student')
        return redirect('students')
    else:

        if request.method == 'POST':
            form = UpdateUserForm(request.POST, request.FILES, instance=user)
            
            if form.is_valid():
                
                form.save()
                new_id = form.cleaned_data['username']
                Student.objects.filter(student_id=id).update(student_id=new_id)
                messages.success(request, 'Successfully updated the student profile')
                return redirect(reverse('edit_student', args=[new_id]))
            else:
                messages.error(request, 'There was an error updating the profile. Please check the form below.')
        else:

            form = UpdateUserForm(instance=user)
        ctx = {'form':form, 'role':'Student', 'user':user}
        return render(request, 'user_profile.html', ctx)


@login_required(login_url='login')
def live_map(request):
    return render(request, 'live_map.html')


@login_required(login_url='login')
def edit_bus(request, pk):
    bus = get_object_or_404(Bus, pk=pk)

    if request.method == "POST":
        form = BusForm(request.POST, instance=bus)

        if form.is_valid():
            bus = form.save()

            try:
                route = bus.route
            except ObjectDoesNotExist:
                route = Route(bus=bus)

            route.route_str = request.POST.get('route_str', "")

            coords_json = request.POST.get('coordinates')
            if coords_json:
                try:
                    route.path = json.loads(coords_json)
                except json.JSONDecodeError:
                    pass

            route.save()
            
            messages.success(request, "Bus details updated successfully.")
            return redirect('buses')
        else:
            messages.error(request, "Error updating bus. Please check the form details.")

    else:
        form = BusForm(instance=bus)

    return render(request, 'edit_bus.html', {
        'form': form,
        'bus': bus,
    })