from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from .forms import idForm

# Create your views here.


def index(request):
    url = 'http://dummy.restapiexample.com/api/v1/employee/{}'
    if request.method == 'POST':
        form = idForm(request.POST)
        if form.is_valid():
            employee_id = request.POST['id_form']
            print(employee_id)
            print(type(employee_id))
            if employee_id.isnumeric():
                searchedEmployee = requests.get(url.format(employee_id)).json()
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
        employee_id = "25710"
        searchedEmployee = requests.get(url.format(employee_id)).json()
    print(employee_id)
    print(searchedEmployee)
    employeeInfo = {
        'id': employee_id,
        'name': searchedEmployee['employee_name'],
        'age': searchedEmployee['employee_age'],
        'salary': searchedEmployee['employee_salary']
    }

    context = {'employeeInfo': employeeInfo, 'form': form}

    return render(request, 'employees/index.html', context)
