from django.contrib import admin
from .models import Course, Tag, Learning, Prerequisite, Payment, UserCourse
from .video import Video
from .models import Contact

@admin.register(Contact)
# Register your models here.
# admin.site.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','email','mobile','message']


class TagAdmin(admin.TabularInline):
    model = Tag

class VideoAdmin(admin.TabularInline):
    model = Video

class LearningAdmin(admin.TabularInline):
    model = Learning

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, LearningAdmin, PrerequisiteAdmin, VideoAdmin]

admin.site.register(Course , CourseAdmin)

admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(UserCourse)
