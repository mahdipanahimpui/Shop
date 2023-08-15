from django.contrib import admin
from . models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('sub_category',)
    list_display = ('name', 'is_sub_category', 'slug')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)

    list_display = ('name', 'get_categories', 'available', 'price')

    def get_categories(self, obj):
        return "".join([c.name for c in obj.category.all()])