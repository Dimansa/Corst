from django.contrib import admin
from .models import Annotation, Document
from .forms import Text


class AnnotationAdmin(admin.ModelAdmin):
    form = Text
    list_display = ('document', 'tag', 'owner', 'updated', 'created')



admin.site.register(Annotation, AnnotationAdmin)



class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'gender', 'major', 'course', 'is_marked', 'is_checked')


admin.site.register(Document, DocumentAdmin)


