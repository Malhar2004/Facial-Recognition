from django.contrib import admin
from .models import Person, Detected_person

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ("Name", "Name_encoding")

admin.site.register(Person, PersonAdmin)

class Detected_PersonAmdin(admin.ModelAdmin):
    list_display = ("Name", "Date", "Time")
admin.site.register(Detected_person, Detected_PersonAmdin)
