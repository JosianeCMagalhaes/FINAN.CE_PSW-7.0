from django.urls import path
from . import views


urlpatterns = [
    path('novo_valor/', views.novo_valor, name="novo_valor"),
    path('view_extrato/', views.view_extrato, name="view_extrato"),
    path('limpar_filtros/', views.limpar_filtros, name="limpar_filtros"),
    path('exportar_pdf/', views.exportar_pdf, name="exportar_pdf"),
]
