from django.urls import path
from . import views
from .views import store,cart,checkout,ProductDetail,Rate


urlpatterns = [
    path('',views.store,name='store' ),
    path('cart/',views.cart,name='cart' ),
    path('checkout/',views.checkout,name='checkout' ),
    path('product/<int:pk>/',views.ProductDetail, name='detail' ),
    path('product/<int:pk>/rate',views.Rate, name='rate' ),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),



]
