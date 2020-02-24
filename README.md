# Project 3

Web Programming with Python and JavaScript


# Pinnochio’s Pizza 



Inside this repo, you can find web application (made with Django framework) for Pinnochio’s Pizza & Subs

In this app, you can (**as user**)

* register and log in/out (necessary when making order)

* access Pinnochio’s Pizza menu with serval food types and proper customization

* make multiple orders combining all available dishes

* see all your orders with status from Pinnochio’s Pizza

 

As Pinnochio’s Pizza staff, you can also:

* do all things above

* see registered orders with possibility of mark them as finished

* access admin panel

 

Within admin panel, there is possibility of:

* managing registered users

* modifying orders in all aspects

* modifying food's types in all aspects



## Requirements


* **Menu**: Your web application should support all of the available menu items for Pinnochio’s Pizza & Subs (a popular pizza place in Cambridge). It’s up to you, based on analyzing the menu and the various types of possible ordered items (small vs. large, toppings, additions, etc.) to decide how to construct your models to best represent the information. Add your models to orders/models.py, make the necessary migration files, and apply those migrations.

* **Adding Items**: Using Django Admin, site administrators (restaurant owners) should be able to add, update, and remove items on the menu. Add all of the items from the Pinnochio’s menu into your database using either the Admin UI or by running Python commands in Django’s shell.

* **Registration, Login, Logout:** Site users (customers) should be able to register for your web application with a username, password, first name, last name, and email address. Customers should then be able to log in and log out of your website.

* **Shopping Cart:** Once logged in, users should see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping should be saved even if a user closes the window, or logs out and logs back in again.

* **Placing an Order:** Once there is at least one item in a user’s shopping cart, they should be able to place an order, whereby the user is asked to confirm the items in the shopping cart, and the total (no need to worry about tax!) before placing an order.

* **Viewing Orders:** Site administrators should have access to a page where they can view any orders that have already been placed.

* **Personal Touch:** Add at least one additional feature of your choosing to the web application. Possibilities include: allowing site administrators to mark orders as complete and allowing users to see the status of their pending or completed orders.


## Models

All types of dishes have its own class, ending with *Type* (i.e. PizzaType), where you can store information like name, possible additions or prices. From this class, you can form proper models (f.e. Pizza) with available options specific to dish type. Proper Order model is for storing information about your order.


## Views

A user will have to register or login if had already registered to be able to order. The pages are easy to navigate through, depnding on what the user is ordering.


Menu view shows the list of all available menu.

 

All order lists (for both user and staff) are also automatically generated. In admin form, you can check orders to inform users, that they order is done.

 

In cart, beside list of all product, you will see price of your order and buttons for making it or delete all items in cart.


## What is pecial Pizza
SuperPizza, available in menu, is special kind of pizza with up to 4 toppings