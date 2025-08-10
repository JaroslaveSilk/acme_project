from django.contrib import admin

from .models import Birthday, Congratulation, Tag



admin.site.register(Tag)
admin.site.register(Birthday)
admin.site.register(Congratulation)
