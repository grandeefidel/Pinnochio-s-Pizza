from django.http import HttpResponse, HttpResponseRedirect,Http404, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from decimal import *


from .models import RegisterForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "users/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            for msg in form.error_messages:
                message = form.error_messages[msg]
            return render(request, "users/register.html", {"message": message})
    form = RegisterForm
    return render(request, "users/register.html", context={"form":form})

@login_required()
def menuList(request):
    form_pizza = PizzaAddForm(request.POST or None)
    context = {
       "menu": menu.objects.all()
    }
    return render(request, 'users/menu.html', context)

@login_required()
def gotoMenu(request, page, message=""):
    print(f"menu: {request.GET.get('menu')}")
    # if request.method=='GET':
    page = 'users/'+page+'.html'
        # message = request.GET.get('message')
    form_pizza = PizzaAddForm(request.POST or None)
    regularPizza = PizzaType.objects.get(pk=1)
    Sicilian = PizzaType.objects.get(pk=2)
    context = {
       "RegularPizza": regularPizza,
       "SicilianPizza": Sicilian,
        "PizzaToppings": PizzaTopping.objects.all(),
        "Sub": SubType.objects.all(),
        "Pasta": PastaType.objects.all(),
        "Salad": SaladType.objects.all(),
        "Platter": PlatterType.objects.all(),
        "form_pizza": form_pizza,
        "message":message
    }
    return render(request, page.lower(), context)

@login_required()
def orderPizza(request):
    form_pizza = PizzaAddForm(request.POST or None)
    if form_pizza.is_valid():
        menu= request.POST["pizzatype"]
        form_pizza_size = form_pizza.cleaned_data["pizza_size"]
        form_topping_count = int(request.POST["no_of_toppings"])
        form_pizza_type = PizzaType.objects.get(name=request.POST["pizzatype"])
        form_pizza_toppings = form_pizza.cleaned_data["toppings"]
        toppings_count = form_pizza_toppings.count()
        print(f"toppings count {toppings_count} ")
        print(f"form_topping_count {form_topping_count}")
        form_pizza_add_by = request.user
        if toppings_count > form_topping_count:
            return redirect('gotoMenu', page=menu, message="number of toppings exceeded")
        new_pizza = Pizza(add_by=form_pizza_add_by, pizza_size=form_pizza_size, pizzatype=form_pizza_type, )
        new_pizza.save()
        new_pizza.toppings.set(form_pizza_toppings)
        print(f"{Pizza.objects.all()}")
        print(f"toppings count {new_pizza.toppings.all().count()}")
        new_pizza.calculate_price()
        new_pizza.save()
        form_pizza = PizzaAddForm()

        # return HttpResponseRedirect(reverse("gotoMenu")+'?menu='+menu+'&message=Pizza have been added')
        return redirect('gotoMenu', page=menu, message="Pizza have been added")

    # return HttpResponseRedirect(reverse("gotoMenu")+'?menu='+menu+'&message=Form not valid')
    return redirect('gotoMenu', page=menu, message="Form not valid")


@login_required()
def add_to_cart(request, item_type, item_id, item_bigger, add_cheese):
    menu = item_type
    if item_type == "subs":
        item_id = SubType.objects.get(id=item_id)
        new_sub = Sub(subtype=item_id, additional_cheese=add_cheese, subsize=item_bigger, add_by=request.user)
        new_sub.calculate_price()
        new_sub.save()
        message="Sub added!"

    elif item_type == "platters":
        item_id = PlatterType.objects.get(id=item_id)
        new_platter = Platter(plattertype=item_id, plattersize=item_bigger, add_by=request.user)
        new_platter.calculate_price()
        new_platter.save()
        message="Platter added!"

    elif item_type == "pasta":
        item_id = PastaType.objects.get(id=item_id)
        new_pasta = Pasta(pastatype=item_id, add_by=request.user)
        new_pasta.calculate_price()
        new_pasta.save()
        message="Pasta added!"

    elif item_type == "salads":
        item_id = SaladType.objects.get(id=item_id)
        new_salad = Salad(saladtype=item_id, add_by=request.user)
        new_salad.calculate_price()
        new_salad.save()
        message="Salad added!"

    else:
        return HttpResponseNotFound('<h1>Product not found</h1>')

    return redirect('gotoMenu', page=menu, message=message)


@login_required()
def make_order(request):
    new_proper_order = ProperOrder()
    new_proper_order.order_client = request.user
    new_proper_order.order_price = calculate_cart_price(request.user)
    new_proper_order.save()

    for item in Sub.objects.filter(add_by=request.user).filter(already_ordered=False):
        item.already_ordered = True
        item.in_order = new_proper_order
        item.save()

    for item in Pasta.objects.filter(add_by=request.user).filter(already_ordered=False):
        item.already_ordered = True
        item.in_order = new_proper_order
        item.save()

    for item in Salad.objects.filter(add_by=request.user).filter(already_ordered=False):
        item.already_ordered = True
        item.in_order = new_proper_order
        item.save()

    for item in Platter.objects.filter(add_by=request.user).filter(already_ordered=False):
        item.already_ordered = True
        item.in_order = new_proper_order
        item.save()

    for item in Pizza.objects.filter(add_by=request.user).filter(already_ordered=False):
        item.already_ordered = True
        item.in_order = new_proper_order
        item.save()

    # messages.add_message(request, messages.INFO, f"Order number {new_proper_order.id} send! If you have questions, contact us: 617-876-4897")
    return redirect(user_orders_view)


@login_required
def user_orders_view(request):
    context = {"orders": reversed(ProperOrder.objects.filter(order_client=request.user))}
    return render(request, 'users/my_orders.html', context)


def calculate_cart_price(username):
    price_all = 0
    for obj in Sub.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price
    for obj in Pasta.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price
    for obj in Salad.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price
    for obj in Platter.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price
    for obj in Pizza.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price
    return price_all



@login_required
def cart_view(request):
    price_all = Decimal(calculate_cart_price(request.user))
    context = {}
    context.update({"price_all": price_all})
    context.update({"Sub": Sub.objects.filter(add_by=request.user).filter(already_ordered=False)})
    context.update({"Pasta": Pasta.objects.filter(add_by=request.user).filter(already_ordered=False)})
    context.update({"Salad": Salad.objects.filter(add_by=request.user).filter(already_ordered=False)})
    context.update({"Platter": Platter.objects.filter(add_by=request.user).filter(already_ordered=False)})
    context.update({"Pizza": Pizza.objects.filter(add_by=request.user).filter(already_ordered=False)})
    print(f"content : {context}")
    return render(request, 'users/cart.html', context)

@login_required
def clear_cart(request):
    delete_all_user_orders(request.user)
    return redirect("cart_view")

def delete_all_user_orders(username):
    Sub.objects.filter(add_by=username).filter(already_ordered=False).delete()
    Pasta.objects.filter(add_by=username).filter(already_ordered=False).delete()
    Salad.objects.filter(add_by=username).filter(already_ordered=False).delete()
    Platter.objects.filter(add_by=username).filter(already_ordered=False).delete()
    Pizza.objects.filter(add_by=username).filter(already_ordered=False).delete()
    return True

@staff_member_required
def all_orders_view(request):
    context = {"orders": reversed(ProperOrder.objects.all())}
    return render(request, 'users/all_orders.html', context)

@staff_member_required
def mark_order_as_done(request, order_id):
    marked = ProperOrder.objects.get(id=order_id)
    marked.order_done = True
    marked.save()
    return redirect(all_orders_view)

