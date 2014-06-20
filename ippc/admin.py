# https://gist.github.com/renyi/3596248
from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.models import Page, RichTextPage
from mezzanine.pages.admin import PageAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import TabularDynamicInlineAdmin, StackedDynamicInlineAdmin

from .models import PestStatus, PestReport, CountryPage, WorkAreaPage, PublicationLibrary, Publication, ReportingObligation,EventReporting,PestFreeArea,ImplementationISPM,ImplementationISPMVersion, TransPublicationLibraryPage#, File
from django.contrib.auth.models import User

from mezzanine.pages.models import RichTextPage, Link
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from models import TransRichTextPage, TransLinkPage

# Publications -----------------

# class FileInline(TabularDynamicInlineAdmin):
#     model = File


#
# Publication Library
#
# class TransPublicationLibraryPageInline(TabularDynamicInlineAdmin):
#     model  = TransPublicationLibraryPage
#     fields = ("lang", "title", "content")
#
# class TransPublicationLibraryPageAdmin(admin.ModelAdmin):
#     inlines   = (TransInline,)
#
# admin.site.unregister(PublicationLibrary)
# admin.site.register(PublicationLibrary, TransPublicationLibraryPageAdmin)


class PublicationInline(StackedDynamicInlineAdmin):
    model = Publication
    prepopulated_fields = { 'slug': ['title'] }
    # exclude = ('author',) # http://stackoverflow.com/a/7588194/412329
    
    # def queryset(self, request):
    #     return Publication.objects.filter(author=request.user)
    # 
    # def save_model(self, request, obj, form, change):
    #     obj.author = request.user
    #     obj.author_id = request.user.id
    #     obj.save()


    # #
    # # Richtext
    # #
    # class TransInline(TabularDynamicInlineAdmin):
    #     model  = TransRichTextPage
    #     fields = ("lang", "title", "content")
    #
    # class TransPageAdmin(PageAdmin):
    #     inlines   = (TransInline,)
    #
    # admin.site.unregister(RichTextPage)
    # admin.site.register(RichTextPage, TransPageAdmin)



class TransPublicationLibraryPageAdmin(StackedDynamicInlineAdmin):
    model = TransPublicationLibraryPage
    fields = ("lang", "title", "content")
    # fk_name = 'parent' # http://stackoverflow.com/a/2409118
    # prepopulated_fields = { 'slug': ['title'] }

class PublicationLibraryAdmin(PageAdmin):
    inlines = (PublicationInline, TransPublicationLibraryPageAdmin,)

admin.site.register(PublicationLibrary, PublicationLibraryAdmin)





# Country Pages ----------------- 
# http://mezzanine.jupo.org/docs/content-architecture.html#creating-custom-content-types
countrypages_extra_fieldsets = ((None, {"fields": ("name", "country_slug", "iso", "iso3", "contact_point", "editors", )}),)

class CountryPageAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + countrypages_extra_fieldsets
    prepopulated_fields = { 'country_slug': ['name'] }
    # list_display = ('continent','name','iso','iso3', 'languages', 'currency_name')
    # list_display_links = ('name',)

admin.site.register(CountryPage, CountryPageAdmin)





# Work Area Pages -----------------

workareapages_extra_fieldsets = ((None, {"fields": ("users", "groups", "content")}),)
# class WorkAreaFileInline(admin.TabularInline):
#     model = WorkAreaPage
class WorkAreaPageAdmin(PageAdmin):
    # inlines = (WorkAreaFileInline,)
    fieldsets = deepcopy(PageAdmin.fieldsets) + workareapages_extra_fieldsets

admin.site.register(WorkAreaPage, WorkAreaPageAdmin)





# Pages -----------------
# =todo: get this to work

# admin.site.unregister(Page)
#
# class CustomPageAdmin(PageAdmin):
#     save_on_top = True
#     list_display = ('title', 'publish_date', 'status')
#     list_filter = ('title', 'publish_date', 'status')
#     search_fields = ('title', 'content')
#
# admin.site.register(Page, CustomPageAdmin)




# Pest Reports -----------------

class PestStatusAdmin(admin.ModelAdmin):
    """Options for the pest status field of Pest Reports"""
    save_on_top = True
        
class PestReportAdmin(admin.ModelAdmin):
    # http://stackoverflow.com/a/8393130
    # def has_add_permission(self, request):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_change_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    save_on_top = True
    list_display = ('title', 'publish_date', 'modify_date', 'status', 'country')
    list_filter = ('title', 'publish_date', 'modify_date', 'status', 'country')
    search_fields = ('title', 'summary')
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(PestStatus, PestStatusAdmin)
admin.site.register(PestReport, PestReportAdmin)


class ReportingObligationAdmin(admin.ModelAdmin):
    # http://stackoverflow.com/a/8393130
    # def has_add_permission(self, request):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_change_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(ReportingObligation, ReportingObligationAdmin)

class EventReportingAdmin(admin.ModelAdmin):
    # http://stackoverflow.com/a/8393130
    # def has_add_permission(self, request):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_change_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(EventReporting, EventReportingAdmin)

class PestFreeAreaAdmin(admin.ModelAdmin):
    # http://stackoverflow.com/a/8393130
    # def has_add_permission(self, request):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_change_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(PestFreeArea, PestFreeAreaAdmin)

class ImplementationISPMAdmin(admin.ModelAdmin):
    # http://stackoverflow.com/a/8393130
    # def has_add_permission(self, request):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_change_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.groups.filter(name='Developers').exists()
    save_on_top = True
    list_display = ('title', 'publication_date', 'modify_date',   'country')
    list_filter = ('title', 'publication_date', 'modify_date',  'country')
    search_fields = ('title', 'short_description')
    prepopulated_fields = { 'slug': ['title'] }
admin.site.register(ImplementationISPM, ImplementationISPMAdmin)


class ImplementationISPMVersionAdmin(admin.ModelAdmin):
    """Options for ImplementationISPMVersion field of ImplementationISPM"""
    save_on_top = True
admin.site.register(ImplementationISPMVersion, ImplementationISPMVersionAdmin)  
    
# Translatable user-content  -----------------
if "mezzanine.pages" in settings.INSTALLED_APPS:


    #
    # Richtext
    #
    class TransInline(TabularDynamicInlineAdmin):
        model  = TransRichTextPage
        fields = ("lang", "title", "content")

    class TransPageAdmin(PageAdmin):
        inlines   = (TransInline,)

    admin.site.unregister(RichTextPage)
    admin.site.register(RichTextPage, TransPageAdmin)
    


    #
    # Link
    #
    class TransLinkInline(TabularDynamicInlineAdmin):
        model = TransLinkPage
        fields = ("lang", "title", "slug")

    class TransLinkAdmin(LinkAdmin):
        inlines  = (TransLinkInline,)

    admin.site.unregister(Link)
    admin.site.register(Link, TransLinkAdmin)

if "mezzanine.forms" in settings.INSTALLED_APPS:
    from mezzanine.forms.models import Form, Field
    from mezzanine.forms.admin import FormAdmin, FieldAdmin
    from models import TransField, TransForm

    #
    # Form
    #
    class TransFormInline(TabularDynamicInlineAdmin):
        model = TransForm
        fields = ("lang", "title", "content", "button_text", "response")

    class TransFormAdmin(FormAdmin):
        inlines = (FieldAdmin, TransFormInline)

    admin.site.unregister(Form)
    admin.site.register(Form, TransFormAdmin)

    class TransFieldInline(TabularDynamicInlineAdmin):
        model = TransField
        fields = ("lang", "original", "label", "choices", "default", "help_text")

    class TransFieldAdmin(admin.ModelAdmin):
        inlines = (TransFieldInline, )
        fields = ("label", "choices", "default", "help_text")
    admin.site.register(Field, TransFieldAdmin)

    #
    # Gallery
    #
if "mezzanine.galleries" in settings.INSTALLED_APPS:
    from mezzanine.galleries.models import Gallery, GalleryImage
    from mezzanine.galleries.admin import GalleryAdmin, GalleryImageInline
    from models import TransGallery, TransGalleryImage

    class TransGalleryInline(TabularDynamicInlineAdmin):
        model  = TransGallery
        fields = ("lang", "title", "content", )

    class TransGalleryAdmin(GalleryAdmin):
        inlines = (GalleryImageInline, TransGalleryInline, )

    admin.site.unregister(Gallery)
    admin.site.register(Gallery, TransGalleryAdmin)