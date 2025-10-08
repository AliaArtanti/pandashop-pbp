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
from django.db.models import Q
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie


from .models import Product
from .forms import ProductForm

def _product_to_dict(p: Product):
    return {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "thumbnail": p.thumbnail,
        "category": p.category,
        "is_featured": p.is_featured,
    }


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



@login_required
def products_json(request):
    data = Product.objects.filter(owner=request.user)
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json",
    )

@login_required
def products_xml(request):
    data = Product.objects.filter(owner=request.user)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml",
    )

@login_required
def product_json_by_id(request, id):
    data = Product.objects.filter(pk=id, owner=request.user)
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json",
    )

@login_required
def product_xml_by_id(request, id):
    data = Product.objects.filter(pk=id, owner=request.user)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml",
    )

# Halaman product list
@ensure_csrf_cookie
@login_required
def product_list(request):
    return render(request, "product_list.html")

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

@require_http_methods(["GET", "POST"])
@login_required
def api_products_list_create(request):
    if request.method == "GET":
        qs = Product.objects.filter(owner=request.user).order_by("-id")

        raw = (request.GET.get('category') or '').strip()
        if raw:
            cats = [c.strip() for c in raw.split(',') if c.strip()]
            if cats:
                q = Q()
                for c in cats:
                    q |= Q(category__iexact=c)
                qs = qs.filter(q)

        data = [_product_to_dict(p) for p in qs]
        return JsonResponse({"ok": True, "data": data})

    # POST create 
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    name = (payload.get("name") or "").strip()
    if not name:
        return JsonResponse({"ok": False, "error": "Nama wajib diisi."}, status=400)

    p = Product.objects.create(
        name=name,
        price=payload.get("price") or 0,
        description=payload.get("description") or "",
        thumbnail=payload.get("thumbnail") or "",
        category=payload.get("category") or "",
        is_featured=bool(payload.get("is_featured", False)),
        owner=request.user,
    )
    return JsonResponse({"ok": True, "message": "Product created.", "data": _product_to_dict(p)}, status=201)


@require_http_methods(["GET", "PUT", "DELETE"])
@login_required
def api_products_detail_update_delete(request, pk):
    try:
        # Batasi ke produk milik user sendiri
        p = Product.objects.get(pk=pk, owner=request.user)
    except ObjectDoesNotExist:
        return JsonResponse({"ok": False, "error": "Not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({"ok": True, "data": _product_to_dict(p)})

    if request.method == "DELETE":
        p.delete()
        return JsonResponse({"ok": True, "message": "Product deleted."})

    # PUT update
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    # Update field yang dikirim
    for field in ["name", "price", "description", "thumbnail", "category", "is_featured"]:
        if field in payload:
            setattr(p, field, payload[field])
    p.save()
    return JsonResponse({"ok": True, "message": "Product updated.", "data": _product_to_dict(p)})

@require_http_methods(["POST"])
def api_register(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    username = (payload.get("username") or "").strip()
    # Form register kirim password1 & password2
    password1 = payload.get("password1") or payload.get("password") or ""
    password2 = payload.get("password2") or payload.get("password") or ""

    # Validasi basic
    if not username or not password1 or not password2:
        return JsonResponse({"ok": False, "error": "Username dan kedua password wajib diisi."}, status=400)

    if password1 != password2:
        return JsonResponse({"ok": False, "error": "Password dan konfirmasi tidak sama."}, status=400)

    if len(password1) < 8:
        return JsonResponse({"ok": False, "error": "Password minimal 8 karakter."}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"ok": False, "error": "Username sudah dipakai."}, status=400)

    # Buat user
    User.objects.create_user(username=username, password=password1)
    return JsonResponse({"ok": True, "message": "Register sukses. Silakan login."}, status=201)


@require_http_methods(["POST"])
def api_login(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    user = authenticate(request, username=payload.get("username",""), password=payload.get("password",""))
    if user is None:
        return JsonResponse({"ok": False, "error": "Username/password salah."}, status=400)

    login(request, user)
    # set cookie last_login 
    resp = JsonResponse({"ok": True, "message": "Login sukses."})
    resp.set_cookie("last_login", timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    return resp


@require_http_methods(["POST"])
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
    resp = JsonResponse({"ok": True, "message": "Logout sukses."})
    resp.delete_cookie("last_login")
    return resp
