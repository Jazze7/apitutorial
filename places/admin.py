from django.contrib import admin
from places.models import Place, Category, Gallery,Comment

# Register your models here.
class GalleryAdmin(admin.TabularInline):
    list_display = ('name', 'image')
    model=Gallery
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','place')

    inlines=[GalleryAdmin]

admin.site.register(Place,PlaceAdmin)


admin.site.register(Category)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','place','comment')

admin.site.register(Comment,CommentAdmin)
