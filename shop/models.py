from pyexpat import model
from unicodedata import category, name
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True) # blank는 비어있어도 된다는 의미. // 필수요소가 아님을 나타냄
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    # slug = url에 사용된다. // 모든 문자를 down-casting 하고 공백을 hypen(-)으로 대체하여 생성.

    class Meta:
        ordering = ['name']
        verbose_name = 'category'               # 단수형
        verbose_name_plural = 'categories'      # 복수형

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    # on_delete=models.SET_NULL - 카테고리가 지워졌어도 제품은 그대로 내버려둘 때 사용, 카테고리는 NULL로 변경
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # decimal_places = 소숫점 몇째짜리까지 출력할지 설정
    stock = models.PositiveBigIntegerField
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = model.models.DateTimeField(auto_now=True)

    class Meta: # Model 안의 Meta에는 검색옵션, 디스플레이된 이름 등의 정보가 들어갑니다.
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]
        # index_together = 두개를 병합해서 index 기준을 잡아주는 역할

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    