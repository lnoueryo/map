from django.contrib import admin
from .models import Price, Station, Line, Company
# Register your models here.
class MultiDBModelAdmin1(admin.ModelAdmin):
    using = 'price'
 
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
 
    def delete_model(self, request, obj):
        obj.delete(using=self.using)
 
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)
 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
 
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
class MultiDBModelAdmin2(admin.ModelAdmin):
    using = 'station'
 
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
 
    def delete_model(self, request, obj):
        obj.delete(using=self.using)
 
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)
 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
 
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

admin.site.register(Price)
admin.site.register(Station)
admin.site.register(Line)
admin.site.register(Company)