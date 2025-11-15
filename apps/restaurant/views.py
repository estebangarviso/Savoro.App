from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Dish, Category
from .forms import DishForm, CategoryForm, LoginForm


# Authentication
def login_view(request):
    form = LoginForm(request.POST or None)
    context = {"message": None, "form": form}
    if request.POST and form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("restaurant:index")
            else:
                context["message"] = "El usuario ha sido desactivado"
        else:
            context["message"] = "Usuario o contraseña incorrecta"
    return render(request, "restaurant/login.html", context)


@login_required(login_url="/")
def log_out(request):
    logout(request)
    return redirect("restaurant:login")


# Dish CRUD
@login_required(login_url="/")
def index(request):
    dishes = Dish.objects.filter(deleted=False).prefetch_related("tags")
    return render(request, "restaurant/index.html", {"dishes": dishes})


@login_required(login_url="/")
def detail(request, id):
    dish = get_object_or_404(Dish, pk=id, deleted=False)
    return render(request, "restaurant/detail.html", {"dish": dish})


@login_required(login_url="/")
def create(request):
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Plato creado exitosamente")
            return redirect("restaurant:index")
    else:
        form = DishForm()
    return render(
        request, "restaurant/form.html", {"form": form, "title": "Crear Plato"}
    )


@login_required(login_url="/")
def update(request, id):
    dish = get_object_or_404(Dish, pk=id, deleted=False)
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, "Plato actualizado exitosamente")
            return redirect("restaurant:detail", id=dish.id)
    else:
        form = DishForm(instance=dish)
    return render(
        request, "restaurant/form.html", {"form": form, "title": "Editar Plato"}
    )


@login_required(login_url="/")
def delete(request, id):
    dish = get_object_or_404(Dish, pk=id, deleted=False)
    if request.method == "POST":
        dish.deleted = True
        dish.save()
        messages.success(request, "Plato eliminado exitosamente")
        return redirect("restaurant:index")
    return render(request, "restaurant/detail.html", {"dish": dish})


# Category views
@login_required(login_url="/")
def category_list(request):
    categories = Category.objects.filter(deleted=False)
    return render(
        request, "restaurant/category/category_list.html", {"categories": categories}
    )


@login_required(login_url="/")
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente")
            return redirect("restaurant:category_list")
    else:
        form = CategoryForm()
    return render(
        request, "restaurant/form.html", {"form": form, "title": "Crear Categoría"}
    )


@login_required(login_url="/")
def category_update(request, id):
    category = get_object_or_404(Category, pk=id, deleted=False)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente")
            return redirect("restaurant:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request, "restaurant/form.html", {"form": form, "title": "Editar Categoría"}
    )


@login_required(login_url="/")
def category_delete(request, id):
    category = get_object_or_404(Category, pk=id, deleted=False)
    if request.method == "POST":
        category.deleted = True
        category.save()
        messages.success(request, "Categoría eliminada exitosamente")
        return redirect("restaurant:category_list")
    return redirect("restaurant:category_list")
