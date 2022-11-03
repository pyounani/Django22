from django.contrib import admin
from .models import Post, Category

# Register your models here.
# 관리자 페이지에 모델 등록
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)