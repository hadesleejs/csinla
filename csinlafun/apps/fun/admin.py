from django.contrib import admin
from fun.models import *


admin.site.register(Hoster)
class ActivityTimeItemInline(admin.StackedInline):
  	model = ActivityTimeItem
  	can_delete = True
  	verbose_name_plural = 'activitytimeitem'
  	extra=0

class ParagraphInline(admin.StackedInline):
  	model = Paragraph
  	can_delete = True
  	verbose_name_plural = 'paragraph'
  	extra=0

class ActivityAdmin(admin.ModelAdmin):
	inlines =(ActivityTimeItemInline,ParagraphInline)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(ActivityTimeItem)
admin.site.register(ActivityOrder)
