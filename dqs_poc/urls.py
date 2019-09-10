from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from dqs_poc_app.views import db_select, get_tables, login_validation, runProcedure, getTablesHealth,getProfileResults
from django.conf.urls.static import static
from django.conf import settings

app_name = 'dqs_poc_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dqs_poc_app/', include('dqs_poc_app.urls')),
    path('dqs_poc_app/', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', TemplateView.as_view(template_name='login.html'), name='login'),
    path('getDatabases/', db_select, name='db_select'),
    path('getTables/', get_tables, name='get_tables'),
    path('login/', login_validation, name='login_validation'),
    path('runProcedure/', runProcedure, name='runProcedure'),
    path('getTablesHealth/', getTablesHealth, name='getTablesHealth'),
    path('getProfileResults/', getProfileResults, name='getProfileResults'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)