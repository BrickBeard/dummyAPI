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
    all_employees = requests.get(url_all).json()
    results = []
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            query = request.POST['search_query']
            for employee in all_employees:
                for (key, value) in employee.items():
                    if query in value:
                        results.append(employee)
            print("---Search query: "+query)
            print("---Total Results: {}".format(len(results)))
            if results == []:
                messages.warning(
                    request, 'Employee does not exist.  Please try again.')
                form = searchForm()
                return render(request, 'employees/index.html', {'form': form})

            employee_id = results[0]['id']
            print("---First Returned Employee: {}".format(employee_id))
            searchedEmployee = requests.get(url.format(employee_id)).json()
    else:
        form = searchForm()
        employee_id = all_employees[0]['id']
        searchedEmployee = requests.get(url.format(employee_id)).json()
        print("---First Employee ID: "+employee_id)
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
    context = {'employeeInfo': employeeInfo, 'form': form, 'results': results}
    return render(request, 'employees/index.html', context)


def allEmployees(request):
    url = 'http://dummy.restapiexample.com/api/v1/employees'
    response = requests.get(url).json()
    url_path = request.path
    context = {'results': response, 'url': url_path}
    print('---Rendered all {} employees'.format(len(response)))
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
            print("---Creating new Employee Instance: {}, {} years, ${}".format(
                employeeInfo['name'], employeeInfo['age'], employeeInfo['salary']))
            return render(request, 'employees/index.html', context)

    else:
        url = request.path
        form = create_form()
        context = {'url': url, 'form': form}
        return render(request, 'employees/editForm.html', context)
        print('---Initialized employee create form')
    return render(request, 'employees/editForm.html')


def updateForm(request, id):
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    update_url = 'http://dummy.restapiexample.com/api/v1/update/{}'
    if request.method == 'POST':
        form = update_form(request.POST)
        if form.is_valid():
            print("---Updating employee #{}".format(id))
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
            print("---Employee #{} was successfully updated.".format(id))
    elif requests.get(url.format(id)).json() == False:
        messages.warning(
            request, 'I\'m sorry, that employee does not exist. Please edit an existing employee. ')
        print('Employee #{} does not exist'.format(id))
        return redirect('index')
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
    print("---User # {} was successfully deleted".format(id))

    messages.success(
        request, 'You have succesfully deleted employee #{}'.format(id))
    return redirect('index')
