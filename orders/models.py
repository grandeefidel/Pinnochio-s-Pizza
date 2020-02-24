from django.db import models

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import decimal

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class menu(models.Model):
    title  = models.CharField(max_length=64, unique=True)
    img_name  = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class PizzaType(models.Model):
    name = models.CharField(max_length=60, unique=True)
    small_0 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    small_1 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    small_2 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    small_3 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    small_4 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    large_0 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    large_1 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    large_2 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    large_3 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    large_4 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
    

class ProperOrder(models.Model):
    order_client = models.ForeignKey(User, on_delete=models.CASCADE)
    order_timestamp = models.DateTimeField(auto_now_add=True)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    order_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Order number {self.id}"



class PizzaTopping(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name



class Pizza(models.Model):
    in_order = models.ForeignKey(ProperOrder, on_delete=models.CASCADE, null=True, blank=True, related_name="pizzas")
    already_ordered = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pizza_size = models.CharField(
        max_length=5,
        choices=(
            ("small", "small"),
            ("large", "large")
        ),
    )
    pizzatype = models.ForeignKey(PizzaType, on_delete=models.CASCADE, null=True)
    toppings = models.ManyToManyField(PizzaTopping, blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def calculate_price(self):
        if self.toppings.all().count() > 4:
            pizza_topping_amount = 4
        else:
            pizza_topping_amount = self.toppings.all().count()
        self.price = eval("self.pizzatype." +
                          str(self.pizza_size) + "_" +
                          str(pizza_topping_amount))
        print(f"price {self.price}")
    def __str__(self):
        return f"Pizza: {self.pizzatype.name} {self.get_pizza_size_display()} with {self.toppings.all().count()} topping(s)"


class PizzaAddForm(forms.ModelForm):

    class Meta:
        model = Pizza
        fields = (
            'pizza_size',
            'toppings',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['toppings'].widget.attrs.update({'size': '7'})




class SubType(models.Model):
    name = models.CharField(max_length=60, unique=True)
    small_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    large_price = models.DecimalField(max_digits=4, decimal_places=2)
    only_big_size = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(SubType, self).save(*args, **kwargs)
        if self.small_price is None:
            self.only_big_size = True
        super(SubType, self).save(*args, **kwargs)



class Sub(models.Model):
    in_order = models.ForeignKey(ProperOrder, on_delete=models.CASCADE, null=True, related_name="subs")
    already_ordered = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subtype = models.ForeignKey(SubType, on_delete=models.CASCADE)
    additional_cheese = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)
    subsize = models.CharField(choices=(("small", "small"), ("large", "large")), max_length=60, default="small")

    def calculate_price(self):
        if not self.subtype.only_big_size:
            if self.subsize == "small":
                self.price = self.subtype.small_price
            elif self.subsize == "large":
                self.price = self.subtype.large_price
        else:
            self.price = self.subtype.large_price

        if self.additional_cheese == True:
            self.price += decimal.Decimal(0.5)
        # print(f"Price for {self.subtype} version of Sub is {self.price}")

    def __str__(self):
        if self.additional_cheese is False:
            return f"Sub: {str(self.subtype)} {self.subsize}"
        else:
            return f"Sub: {str(self.subtype)} {self.subsize} with extra cheese"



class PastaType(models.Model):
    name = models.CharField(max_length=60, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Pasta(models.Model):
    in_order = models.ForeignKey(ProperOrder, on_delete=models.CASCADE, null=True, related_name="pastas")
    already_ordered = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pastatype = models.ForeignKey(PastaType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def calculate_price(self):
        self.price = self.pastatype.price

    def __str__(self):
        return f"Pasta: {str(self.pastatype)}"


class SaladType(models.Model):
    name = models.CharField(max_length=60, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name



class Salad(models.Model):
    in_order = models.ForeignKey(ProperOrder, on_delete=models.CASCADE, null=True, related_name="salads")
    already_ordered = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    saladtype = models.ForeignKey(SaladType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)

    def calculate_price(self):
        self.price = self.saladtype.price

    def __str__(self):
        return f"Salad: {str(self.saladtype)}"


class PlatterType(models.Model):
    name = models.CharField(max_length=60, unique=True)
    small_price = models.DecimalField(max_digits=4, decimal_places=2)
    large_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Platter(models.Model):
    in_order = models.ForeignKey(ProperOrder, on_delete=models.CASCADE, null=True, related_name="platters")
    already_ordered = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    plattertype = models.ForeignKey(PlatterType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)
    plattersize = models.CharField(choices=(("small", "small"), ("large", "large")), max_length=60, default="small")

    def calculate_price(self):
        print(self.plattersize)
        if self.plattersize == "small":
            self.price = self.plattertype.small_price
        elif self.plattersize == "large":
            self.price = self.plattertype.large_price

    def __str__(self):
        return f"Platter: {str(self.plattertype)}"





