from django.contrib import admin

from .models import incomesource,category,item,finbook,textstream,datasource,sentmentlist,project,search
from import_export.admin import ImportExportModelAdmin


@admin.register(textstream)
class textstreamAdmin(ImportExportModelAdmin):

    list_display = ('mytext','impression','creationdate')
    ordering = ('-creationdate',)
    search_fields = ('mytext',)

@admin.register(finbook)
class finbookAdmin(ImportExportModelAdmin):

    list_display = ('amount','category','department')
    ordering = ('transactiondate',)
    search_fields = ('amount',)

class incomesourceAdmin(admin.ModelAdmin):
    list_display = ('sourcename','id')
    ordering = ('sourcename',)
    search_fields = ('sourcename',)

admin.site.register(incomesource, incomesourceAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ('categoryname','id')
    ordering = ('categoryname',)
    search_fields = ('categoryname',)

admin.site.register(category, categoryAdmin)

class itemAdmin(admin.ModelAdmin):
    list_display = ('itemname','id')
    ordering = ('itemname',)
    search_fields = ('itemname',)

admin.site.register(item, itemAdmin)


@admin.register(datasource)
class datasourceAdmin(ImportExportModelAdmin):

    list_display = ('sourcename',)
    ordering = ('sourcename',)
    search_fields = ('sourcename',)

@admin.register(sentmentlist)
class sentmentlistAdmin(ImportExportModelAdmin):

    list_display = ('myword','imporession',)
    ordering = ('myword',)
    search_fields = ('myword',)

@admin.register(project)
class projectAdmin(ImportExportModelAdmin):

    list_display = ('projectname',)
    ordering = ('projectname',)
    search_fields = ('projectname',)

@admin.register(search)
class searchAdmin(ImportExportModelAdmin):

    list_display = ('searchname',)
    ordering = ('searchname',)
    search_fields = ('searchname',)
