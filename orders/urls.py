from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("pizza_menu", views.menuList, name="pizza_menu"),
    path("gotoMenu/<str:page>/<str:message>", views.gotoMenu, name="gotoMenu"),
    path("gotoMenu/<str:page>", views.gotoMenu, name="gotoMenu"),
    path("orderPizza", views.orderPizza, name="orderPizza"),
    path("user_orders_view", views.user_orders_view, name="user_orders_view"),
    path("cart_view", views.cart_view, name="cart_view"),
    path("make_order", views.make_order, name="make_order"),
    path("clear_cart", views.clear_cart, name="clear_cart"),
    path("add/<str:item_type>/<int:item_id>/<str:item_bigger>/<int:add_cheese>", views.add_to_cart, name="add_to_cart"),
    path("all_orders_view", views.all_orders_view, name="all_orders_view"),
    path("order/<int:order_id>/done", views.mark_order_as_done, name="mark_order_as_done"),
]
