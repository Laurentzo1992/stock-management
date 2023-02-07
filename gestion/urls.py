from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('index', views.index, name='index'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('vue/<int:pk>', views.vue, name='vue'),
    path('add_product', views.add_product, name='add_product'),
    path('operation', views.operation, name='operation'),
    path('entree', views.entree, name='entree'),
    path('sorti', views.sorti, name='sorti'),
    path('some_view', views.some_view, name='some_view'),
    path('generate_pdf', views.generate_pdf, name='generate_pdf'),
    path('product_detail/<int:pk>', views.product_detail, name='product_detail'),
    path('product_detail2/<int:pk>', views.product_detail2, name='product_detail2'),
    path('product_plus_stock/<int:pk>', views.product_plus_stock, name='product_plus_stock'),
    path('product_minus_stock/<int:pk>', views.product_minus_stock, name='product_minus_stock'),
]