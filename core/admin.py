from django.contrib import admin
from .models import Category, User, Word 
# Register your models here.


class WordAdmin(admin.ModelAdmin):
    list_display = ['category','english', 'persian', 'user']

class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'username']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']

admin.site.register(Word, WordAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)