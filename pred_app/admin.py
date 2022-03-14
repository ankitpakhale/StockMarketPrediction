from django.contrib import admin
from .models import NseData,UserDetails, Contact
# Register your models here.
admin.site.register(NseData)
admin.site.register(UserDetails)
admin.site.register(Contact)
admin.site.site_header = 'Stock market Administration'                   
admin.site.index_title = 'Administration Panel'                
admin.site.site_title = 'Stock market prediction Admin' 