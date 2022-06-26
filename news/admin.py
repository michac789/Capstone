from django.contrib import admin
from django.forms import Textarea
from .models import Information

# Register your models here.
class InformationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "creator", "time_created")
    formfield_overrides = {
        Information.markdown: {'widget': Textarea(attrs = {
            'rows': 4, 'cols': 40})},
    } # TODO - textarea not working


admin.site.register(Information, InformationAdmin)
