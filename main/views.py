from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from .models import Product
from .forms import ProductForm

def show_main(request):
    context = {
        'app_name' : 'pandashop',
        'name': 'Alia Artanti 2406439425',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)

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


# Halaman list produk
def product_list(request):
    products = Product.objects.all().order_by("-id")
    # tanpa "main/" karena file sejajar dg main.html
    return render(request, "product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


#  ADD, EDIT, DELETE, SEARCH 
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:product_list")  
    else:
        form = ProductForm()
    return render(
        request,
        "product_form.html",
        {"form": form, "title": "Tambah Produk"},
    )


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("main:product_detail", pk=pk)  
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "product_form.html",
        {"form": form, "title": "Edit Produk"},
    )


def delete_product(request, pk):
    if request.method == "POST":
        get_object_or_404(Product, pk=pk).delete()
    return redirect("main:product_list")

def product_filter_by_category(request):
    category = request.GET.get('category', '').strip()
    products = Product.objects.all()
    if category:
        products = products.filter(category__iexact=category)

    return render(request, 'product_list.html', {
        'products': products,
        'active_category': category,
    })


