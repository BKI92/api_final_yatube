from django.contrib import admin
from .models import Post, Group, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "following")
    list_filter = ("user",)
    empty_value_display = '-пусто-'


# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)

from django.contrib import admin

# Register your models here.
