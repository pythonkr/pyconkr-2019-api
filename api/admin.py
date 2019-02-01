from django.contrib import admin
from api.models.program import Conference, Presentation
from api.models.program import Place, Category, Difficulty


admin.site.register(Conference)
admin.site.register(Presentation)
admin.site.register(Place)
admin.site.register(Category)
admin.site.register(Difficulty)
