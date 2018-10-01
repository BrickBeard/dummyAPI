from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from .forms import searchForm, create_form, update_form

# Create your views here.


def index(request):
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    url_all = 'http://dummy.restapiexample.com/api/v1/employees'
    results = []
    if request.method == 'POST':
        form = searchForm(request.POST)
        all_employees = requests.get(url_all).json()
        if form.is_valid():
            query = request.POST['search_query']
            for employee in all_employees:
                for (key, value) in employee.items():
                    if query in value:
                        results.append(employee)
            print("Search query: "+query)
            print(results)
            if results == []:
                messages.warning(
                    request, 'Employee does not exist.  Please try again.')
                form = searchForm()
                return render(request, 'employees/index.html', {'form': form})

            employee_id = results[0]['id']
            print(employee_id)
            searchedEmployee = requests.get(url.format(employee_id)).json()
    else:
        form = searchForm()
        employee_id = "64"
        searchedEmployee = requests.get(url.format(employee_id)).json()
        print("Index default with ID: "+employee_id)
        if searchedEmployee == False:
            messages.warning(
                request, 'Please enter a valid Employee ID:')
            return render(request, 'employees/index.html', {'form': form})
        results.append(searchedEmployee)

    employeeInfo = {
        'id': employee_id,
        'name': searchedEmployee['employee_name'],
        'age': searchedEmployee['employee_age'],
        'salary': searchedEmployee['employee_salary']
    }
    print(results)
    context = {'employeeInfo': employeeInfo, 'form': form, 'results': results}
    return render(request, 'employees/index.html', context)


def allEmployees(request):
    url = 'http://dummy.restapiexample.com/api/v1/employees'
    response = requests.get(url).json()
    url_path = request.path
    context = {'results': response, 'url': url_path}
    return render(request, 'employees/editForm.html', context)


def createForm(request):
    url = 'http://dummy.restapiexample.com/api/v1/create'
    if request.method == 'POST':
        form = create_form(request.POST)
        if form.is_valid():
            name = request.POST['name']
            age = request.POST['age']
            salary = request.POST['salary']
            employeeInfo = {'name': name, 'salary': salary, 'age': age}
            data = json.dumps(employeeInfo)
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            response = requests.request(
                'POST', url, data=data, headers=headers)
            messages.success(
                request, 'You have succesfully added a new user')
            search_url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
            new_id = response.json()['id']
            searchedEmployee = requests.get(search_url.format(new_id)).json()
            employeeInfo = {
                'id': new_id,
                'name': searchedEmployee['employee_name'],
                'age': searchedEmployee['employee_age'],
                'salary': searchedEmployee['employee_salary']
            }
            url_path = request.path
            context = {'employeeInfo': employeeInfo, 'url': url_path}
            return render(request, 'employees/index.html', context)

    else:
        url = request.path
        form = create_form()
        context = {'url': url, 'form': form}
        return render(request, 'employees/editForm.html', context)
    return render(request, 'employees/editForm.html')


def updateForm(request, id):
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    update_url = 'http://dummy.restapiexample.com/api/v1/update/{}'
    if request.method == 'POST':
        form = update_form(request.POST)
        if form.is_valid():
            update_url = update_url.format(id)
            name = request.POST['name']
            age = request.POST['age']
            salary = request.POST['salary']
            employeeInfo = {'name': name, 'salary': salary, 'age': age}
            data = json.dumps(employeeInfo)
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            requests.request(
                'PUT', update_url, data=data, headers=headers)
            messages.success(
                request, 'You succesfully updated employee #{}'.format(id))

    searchedEmployee = requests.get(url.format(id)).json()
    employeeInfo = {
        'id': id,
        'name': searchedEmployee['employee_name'],
        'age': searchedEmployee['employee_age'],
        'salary': searchedEmployee['employee_salary']
    }
    form = update_form()
    url_path = request.path
    context = {'employeeInfo': employeeInfo, 'form': form, 'url': url_path}
    return render(request, 'employees/editForm.html', context)


def deleteEmployee(request, id):
    url = 'http://dummy.restapiexample.com/api/v1/delete/{}'.format(id)
    response = requests.request('DELETE', url)
    print(response.text)
    messages.success(
        request, 'You have succesfully deleted employee #{}'.format(id))
    return redirect('index')
