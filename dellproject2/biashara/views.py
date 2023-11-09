from django.shortcuts import render, redirect
from biashara.models import Member
from biashara.forms import ProductsForm
from biashara.models import Product


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
