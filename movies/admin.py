from django.contrib import admin
from .models import Movie, Genre


class MovieAdmin(admin.ModelAdmin):
    """ModelAdmin class for Movie to customize its admin interface"""

    list_display = ('name', 'director')
    search_fields = ('name', 'director')
    list_filter = ('genres',)
    filter_horizontal = ('genres',)


# Register Models on Admin Site
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
