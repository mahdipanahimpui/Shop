from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Category(models.Model):
    is_sub_category = models.BooleanField(default=False)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', blank=True, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category' # the model name used in admin panel
        verbose_name_plural = 'Categories' # to show in admin pannel (plural name use in admin pannel)

    def __str__(self):
        return self.name
    


class Product(models.Model):
    category = models.ManyToManyField(Category,  related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/') # error in removing obj from buckets
    # image = models.ImageField() 
    # needs to pip install pillow

    # description = models.TextField()

    ## How use ckeditor:
    # pip install django-ckeditor
    # add 'ckeditor' in isntalled app in settings.py
    # add | safe in templates
    # to modify add CKEDITOR_CONFIGS in settings.py
    description = RichTextField()




    # price = models.DecimalField(max_digits=4, decimal_places=2) # 1234.12
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Media:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:product_detail', args=(self.slug,))
