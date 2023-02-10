from django.contrib import admin
from .models import MusicInfo, Rating, Like, Comment, Basket, Vip, Image, History, Favorite
from django.utils.safestring import mark_safe


class RatingInline(admin.TabularInline):
    model = Rating


@admin.register(MusicInfo)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_rating', 'image', 'get_image')
    inlines = [RatingInline]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title', )}
    ordering = ['-created_at']
    list_filter = ['title']
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')

    get_image.short_description = 'Картинка'

    def get_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'like', 'is_liked')
    search_fields = ['author', 'like']
    ordering = ['-is_liked']
    list_filter = ['author']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'rating')
    search_fields = ['author', 'post']
    ordering = ['-rating']
    list_filter = ['author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'post', 'created_at', 'author')
    search_fields = ['comment', 'author']
    ordering = ['-created_at']
    list_filter = ['comment']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="60" height="60" />')

    get_image.short_description = 'Картинка'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('basket',)
    search_fields = ['basket', 'author']
    # ordering = ['-created_at']
    list_filter = ['basket']


@admin.register(Vip)
class VipAdmin(admin.ModelAdmin):
    list_display = ('money', 'created_at', 'author')
    search_fields = ['money', 'author']
    ordering = ['-created_at']
    list_filter = ['money']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'author', 'history')
    search_fields = ['history', 'author']
    ordering = ['-created_at']
    list_filter = ['history']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('author', 'favorite', 'is_favorite')
    search_fields = ['author', 'favorite']
    ordering = ['-is_favorite']
    list_filter = ['author']