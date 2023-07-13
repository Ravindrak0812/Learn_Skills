
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("myapp.urls"))
]

admin.site.site_header = "LearnSkills"
admin.site.site_title = "LearnSkills Admin Portal"
admin.site.index_title = "Welcome to LearnSkills Portal"