from django.db import models
from django.contrib.auth.models import User  # User는 장고엣 제공해주는 것이기 때문에
import os

# Create your models here.
# python manange.py startapp blog  => settings가서 추가하기
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # URL를 만들 떄 이용

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
        # 블로그 디테일은 pk를 썼는데 카테고리는 slug 이용

    class Meta:
        verbose_name_plural = 'Catogories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()  #글자 수 제한이 없음

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    #Y 2022, #y 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # author 추후 작성
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # SET_NULL 은 User가 지워져도 게시물은 남기겠다
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] # a.text 실행하면 a 하나 text 하나 따로 나온다. 확장에 해당되는 것은 마지막 text이다.