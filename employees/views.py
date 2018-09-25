from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from .forms import idForm, create_form, update_form

# Create your views here.


def index(request):
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    if request.method == 'POST':
        form = idForm(request.POST)
        if form.is_valid():
            employee_id = request.POST['id_form']
            print("Input ID: "+employee_id)
            if employee_id.isnumeric():
                searchedEmployee = requests.get(url.format(employee_id)).json()
                print(searchedEmployee)
                if searchedEmployee == False:
                    messages.warning(
                        request, 'Employee does not exist.  Please try again.')
                    form = idForm()
                    return render(request, 'employees/index.html', {'form': form})
            else:
                messages.warning(
                    request, 'Invalid input.  You must enter a number')
                form = idForm()
                return render(request, 'employees/index.html', {'form': form})
    else:
        form = idForm()
        employee_id = "1"
        searchedEmployee = requests.get(url.format(employee_id)).json()
        print("Index default with ID: "+employee_id)
        print(searchedEmployee)
        if searchedEmployee == False:
            messages.warning(
                request, 'Please enter a valid Employee ID:')
            return render(request, 'employees/index.html', {'form': form})

    employeeInfo = {
        'id': employee_id,
        'name': searchedEmployee['employee_name'],
        'age': searchedEmployee['employee_age'],
        'salary': searchedEmployee['employee_salary']
    }
    context = {'employeeInfo': employeeInfo, 'form': form}
    return render(request, 'employees/index.html', context)


def createForm(request):
    url = 'http://dummy.restapiexample.com/api/v1/create'
    if request.method == 'POST':
        form = create_form(request.POST)
        if form.is_valid():
            name = str(request.POST['name'])
            age = request.POST['age']
            salary = request.POST['salary']
            employeeInfo = {'name': name, 'salary': salary, 'age': age}
            data = json.dumps(employeeInfo)
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            print(employeeInfo)
#            response = requests.request('post', url, data=employeeInfo)
            response = requests.request(
                'POST', url, data=data, headers=headers)
            print(response.text[id])
            messages.success(
                request, 'You have succesfully added a new user')

            return redirect('index')

    else:
        url = request.path
        form = create_form()
        context = {'url': url, 'form': form}
    return render(request, 'employees/editForm.html', context)


def updateForm(request, id):
    employee_id = request.GET.get('id')
    print(employee_id)
    return render(request, 'employees/editForm.html')
