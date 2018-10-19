from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import searchForm, create_form, update_form, UserRegisterForm
import requests
import json


def index(request):
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    url_all = 'http://dummy.restapiexample.com/api/v1/employees'
    url_pic = 'https://randomuser.me/api/'
    all_employees = requests.get(url_all).json()
    results = []
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            query = request.POST['search_query'].lower().strip()
            for employee in all_employees:
                for (key, value) in employee.items():
                    if query in value.lower():
                        results.append(employee)
            if results == []:
                messages.warning(
                    request, 'Employee does not exist.  Please try again.', fail_silently=True,)
                form = searchForm()
                url_path = request.path
                return render(request, 'employees/index.html', {'form': form, 'url': url_path})

            employee_id = results[0]['id']
            searchedEmployee = requests.get(url.format(employee_id)).json()
    else:
        form = searchForm()
        if request.GET.get('id'):
            employee_id = request.GET.get('id')
        else:
            employee_id = all_employees[0]['id']
        searchedEmployee = requests.get(url.format(employee_id)).json()
        if searchedEmployee == False:
            messages.warning(
                request, 'Please enter a valid Employee ID:', fail_silently=True,)
            return render(request, 'employees/index.html', {'form': form})
        results.append(searchedEmployee)
    image = (requests.get(url_pic).json())['results'][0]['picture']['medium']
    employeeInfo = {
        'id': employee_id,
        'name': searchedEmployee['employee_name'],
        'age': searchedEmployee['employee_age'],
        'salary': searchedEmployee['employee_salary'],
        'image': image,
    }
    url_path = request.path
    context = {'employeeInfo': employeeInfo,
               'form': form, 'results': results, 'url': url_path}
    return render(request, 'employees/index.html', context)


# Trying out Classes instead of Functions (Might not be necessary here, but practice)
class AllEmployees(View):
    url = 'http://dummy.restapiexample.com/api/v1/employees'
    results = requests.get(url).json()

    def get(self, request):
        url_path = request.path
        context = {'url': url_path, 'results': self.results}
        return render(request, 'employees/index.html', context=context)


class FilteredEmployees(AllEmployees):
    def get(self, request, filter_by):
        url_path = request.path
        results = sorted(
            self.results, key=lambda e: e[f'employee_{filter_by}'])
        context = {'url': url_path, 'results': results}
        return render(request, 'employees/index.html', context=context)

# ----- Original Function-Based allEmployees Views -----

# def allEmployees(request):
#     url = 'http://dummy.restapiexample.com/api/v1/employees'
#     results = requests.get(url).json()
#     url_path = request.path
#     context = {'results': results, 'url': url_path}
#     print(f'---Rendered all {len(results)} employees by Id (FBV)')
#     return render(request, 'employees/index.html', context)

# def filteredEmployees(request, filter_by):
#     url = 'http://dummy.restapiexample.com/api/v1/employees'
#     response = requests.get(url).json()
#     if filter_by == 'name':
#         results = sorted(response, key=lambda e: e["employee_name"])
#     elif filter_by == 'age':
#         results = sorted(response, key=lambda e: e["employee_age"])
#     elif filter_by == 'salary':
#         results = sorted(response, key=lambda e: e["employee_salary"])
#     else:
#         results = response
#     url_path = request.path
#     context = {'results': results, 'url': url_path}
#     print(f'---Rendered all {len(response)} employees by {filter_by} (FBV)')
#     return render(request, 'employees/index.html', context)


@login_required
def createForm(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, 'You must be logged in to create new employees.', fail_silently=True,)
        return redirect('login')
    url = 'http://dummy.restapiexample.com/api/v1/create'
    url_pic = 'https://randomuser.me/api/'
    if request.method == 'POST':
        form = create_form(request.POST)
        if form.is_valid():
            name, age, salary = request.POST['name'], request.POST['age'], request.POST['salary']
            data = json.dumps({'name': name, 'salary': salary, 'age': age})
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            response = requests.request(
                'POST', url, data=data, headers=headers)
            messages.success(
                request, 'You have succesfully added a new user', fail_silently=True,)
            search_url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
            searchedEmployee = requests.get(
                search_url.format(response.json()['id'])).json()
            image = (requests.get(url_pic).json())[
                'results'][0]['picture']['medium']
            employeeInfo = {
                'id': response.json()['id'],
                'name': searchedEmployee['employee_name'],
                'age': searchedEmployee['employee_age'],
                'salary': searchedEmployee['employee_salary'],
                'image': image
            }
            url_path = request.path
            print(
                f"---Creating new Employee Instance: {employeeInfo['name']}, {employeeInfo['age']} years, ${employeeInfo['salary']}")
            return redirect(f"/update/{employeeInfo['id']}")

    else:
        url_path = request.path
        form = create_form()
        context = {'url': url_path, 'form': form}
        return render(request, 'employees/index.html', context)


@login_required
def updateForm(request, id):
    if not request.user.is_authenticated:
        messages.warning(
            request, 'You must be logged in to edit employee information.', fail_silently=True,)
        return redirect('login')
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    update_url = 'http://dummy.restapiexample.com/api/v1/update/{}'
    url_pic = 'https://randomuser.me/api/'
    searchedEmployee = requests.get(url.format(id)).json()
    if request.method == 'POST':
        form = update_form(request.POST)
        if form.is_valid():
            update_url = update_url.format(id)
            if request.POST['name']:
                name = request.POST['name']
            else:
                name = searchedEmployee['employee_name']
            if request.POST['age']:
                age = request.POST['age']
            else:
                age = searchedEmployee['employee_age']
            if request.POST['salary']:
                salary = request.POST['salary']
            else:
                salary = searchedEmployee['employee_salary']
            employeeInfo = {'name': name, 'salary': salary, 'age': age}
            data = json.dumps(employeeInfo)
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            requests.request(
                'PUT', update_url, data=data, headers=headers)
            messages.success(
                request, 'You succesfully updated employee #{}'.format(id), fail_silently=True,)
            print("---Employee #{} was successfully updated.".format(id))
    elif requests.get(url.format(id)).json() == False:
        messages.warning(
            request, 'I\'m sorry, that employee does not exist. Please edit an existing employee. ', fail_silently=True,)
        return redirect('index')
    searchedEmployee = requests.get(url.format(id)).json()
    image = (requests.get(url_pic).json())['results'][0]['picture']['medium']
    employeeInfo = {
        'id': id,
        'name': searchedEmployee['employee_name'],
        'age': searchedEmployee['employee_age'],
        'salary': searchedEmployee['employee_salary'],
        'image': image
    }
    form = update_form()
    url_path = request.path
    context = {'employeeInfo': employeeInfo, 'form': form, 'url': url_path}
    return render(request, 'employees/index.html', context)


@login_required
def deleteEmployee(request, id):
    url = 'http://dummy.restapiexample.com/api/v1/delete/{}'.format(id)
    requests.request('DELETE', url)
    print("---User # {} was successfully deleted".format(id))
    messages.success(
        request, 'You have succesfully deleted employee #{}'.format(id), fail_silently=True,)
    return redirect('index')


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request, f'Thanks for joining us {username}.  You can now create, update, and delete employees.', fail_silently=True,)
                return redirect('index')
            else:
                messages.warning(
                    request, 'Invalid input.  Please try again.', fail_silently=True,)
        form = UserRegisterForm()
        url = request.path
        context = {'form': form, 'url': url}
        return render(request, 'registration/register.html', context)
    messages.success(request, 'You are already logged in!',
                     fail_silently=True,)
    return redirect('index')

    def login(request):
        if request.user.is_authenticated():
            messages.success(
                request, 'You are already logged in!', fail_silently=True,)
            return redirect('index')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(
                    request, 'You have successfully logged in!', fail_silently=True,)
                return redirect('index')

            else:
                messages.success(
                    request, 'Oops! Wrong username or password. Try again.', fail_silently=True,)

        return render(request, 'registration/login.html')
