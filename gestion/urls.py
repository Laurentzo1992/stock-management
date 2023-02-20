from django.urls import path
from . import views
from .views import change_password


urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('index', views.index, name='index'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('change-password/', change_password, name='change_password'),
    path('vue/<int:pk>', views.vue, name='vue'),
    path('add_product', views.add_product, name='add_product'),
    path('operation', views.operation, name='operation'),
    path('entree', views.entree, name='entree'),
    path('sorti', views.sorti, name='sorti'),
    path('pdf_view<int:pk>', views.pdf_view, name='pdf_view'),
    path('approvisionement/<int:pk>', views.approvisionement, name='approvisionement'),
    path('liste', views.liste, name='liste'),
    path('etat', views.etat, name='etat'),
    path('statistique', views.statistique, name='statistique'),
    path('product_detail/<int:pk>', views.product_detail, name='product_detail'),
    path('product_detail2/<int:pk>', views.product_detail2, name='product_detail2'),
    path('product_plus_stock/<int:pk>', views.product_plus_stock, name='product_plus_stock'),
    path('product_minus_stock/<int:pk>', views.product_minus_stock, name='product_minus_stock'),
]