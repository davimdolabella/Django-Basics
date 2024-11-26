
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def View(request):
    return HttpResponse('Toma')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sobre/', View )
]
