from django.urls import path
from . import views
from .views import*

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('dashboard/', views.AdminDashoard, name='dashboard'),
    path('register/', views.signup, name='register'),
    path('login/', views.enter, name="login"),
    path('logout/', views.getout, name="logout"),

    path('product/<int:pk>/', productDetailView.as_view(), name='detailview'),
    path('product/create/', ProductCreateView.as_view(), name='createnewproduct'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='productupdate'),
    path('orders/', OrderListView.as_view(), name='orders')
]
