from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clac.urls')),  # ✅ include a URL *list*, not a module
]
