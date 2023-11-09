import base64

from django.shortcuts import render, redirect
from biashara.models import Member
from biashara.forms import ProductsForm
from biashara.models import Product
from biashara.forms import MpesaPaymentForm
import requests


# Create your views here.
def register(request):
    if request.method == 'POST':
        member = Member(firstName=request.POST['firstName'], lastName=request.POST['lastName'],
                        username=request.POST['username'],
                        password=request.POST['password'], email=request.POST['email'])
        member.save()
        return redirect('home')
    else:
        return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def home(request):
    if request.method == 'POST':
        if Member.objects.filter(username=request.POST['username'], password=request.POST['password']).extra():
            member = Member.objects.get(username=request.POST['username'], password=request.POST['password'])
            return render(request, 'index.html', {'member': member})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def inner_page(request):
    return render(request, 'inner-page.html')


def about(request):
    return render(request, 'about.html')


def service(request):
    return render(request, 'services.html')


def doctors(request):
    return render(request, 'doctors.html')


def appointments(request):
    return render(request, 'appointment.html')


def contact(request):
    return render(request, 'contact.html')


def departments(request):
    return render(request, 'departments.html')


def addproducts(request):
    if request.method == "POST":
        form = ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addproducts')
    else:
        form = ProductsForm
        return render(request, 'addproduct.html', {'form': form})


def show(request):
    products = Product.objects.all
    return render(request, 'show.html', {'products': products})


def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('/show')


def edit(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'edit.html', {'product': product})


def update(request, id):
    product = Product.objects.get(id=id)
    form = ProductsForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html', {'product': product})


def make_payment(request):
    if request.method == 'POST':
        form = MpesaPaymentForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = float(form.cleaned_data['amount'])

            # Define the M-Pesa API endpoint and authentication credentials
            api_url = 'https://mydomain.com/path'  # Replace with the actual API endpoint
            consumer_key = 'OIAq5GGl6Gdl3ZwTJg8MwqLhG1y4PJPm'
            consumer_secret = 'IVouUUah8FgzKpG2'

            # Set up the request headers and payload
            # Set up the request headers and payload
            headers = {
                'Authorization': f'Basic {base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()}',
                'Content-Type': 'application/json',
            }

            payload = {
                'phone_number': phone_number,
                'amount': amount,
                "BusinessShortCode": "174379",
                "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
                "TransactionType": "CustomerPayBillOnline",
                "AccountReference": "Glory",
                "TransactionDesc": "Product"

                # Add any other required parameters according to the API documentation
            }

            # Make the API call
            response = requests.post(api_url, headers=headers, json=payload)

            if response.status_code == 200:
                # Payment was successful
                return render(request, 'success.html')
            else:
                # Payment failed, handle the error
                error_message = response.json().get('error_message')
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = MpesaPaymentForm()

    return render(request, 'pay.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def error(request):
    return render(request, 'error.html')
