from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q


from .models import Product
from .forms import ProductForm

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')
    return redirect('main:login')

def show_main(request):
    context = {
        'app_name' : 'pandashop',
        'name': 'Alia Artanti 2406439425',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    return render(request, "register.html", {"form": form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        # set cookie utk last login
        resp = HttpResponseRedirect(reverse("main:product_list"))
        resp.set_cookie("last_login", timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
        return resp
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    resp = redirect("main:login")
    resp.delete_cookie("last_login")
    return resp



def products_json(request):
    return HttpResponse(
        serializers.serialize("json", Product.objects.all()),
        content_type="application/json",
    )


def products_xml(request):
    return HttpResponse(
        serializers.serialize("xml", Product.objects.all()),
        content_type="application/xml",
    )


def product_json_by_id(request, id):
    return HttpResponse(
        serializers.serialize("json", Product.objects.filter(pk=id)),
        content_type="application/json",
    )


def product_xml_by_id(request, id):
    return HttpResponse(
        serializers.serialize("xml", Product.objects.filter(pk=id)),
        content_type="application/xml",
    )

# Halaman product list
@login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user).order_by("-id")
    return render(request, "product_list.html", {"products": products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    return render(request, "product_detail.html", {"product": product})

# ADD, DELETE, EDIT, SEARCH FILTER
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)  
            obj.owner = request.user       
            obj.save()
            return redirect("main:product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form, "title": "Tambah Produk"})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)   
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("main:product_detail", pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form, "title": "Edit Produk"})

@login_required
def delete_product(request, pk):
    if request.method == "POST":
        get_object_or_404(Product, pk=pk, owner=request.user).delete()  # batasi milik sendiri
    return redirect("main:product_list")

@login_required
def product_filter_by_category(request):
    raw = request.GET.get('category', '').strip()
    products = Product.objects.filter(owner=request.user)

    if raw:
        cats = [c.strip() for c in raw.split(',') if c.strip()]
        if cats:
            q = Q()
            for c in cats:
                q |= Q(category__iexact=c)  
            products = products.filter(q)

    return render(
        request,
        "product_list.html",
        {"products": products, "active_category": raw}
    )