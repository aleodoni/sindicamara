from django.contrib import admin

from .models import Filiado, SituacaoFuncional, Setor, Cargo, Ramal

def custom_titled_filter(title):
	class Wrapper(admin.FieldListFilter):
		def __new__(cls, *args, **kwargs):
			instance = admin.FieldListFilter.create(*args, **kwargs)
			instance.title = title
			return instance
	return Wrapper

class RamalInline(admin.TabularInline):
	model = Ramal
	extra = 2
	verbose_name_plural = 'ramais'


class FiliadoAdmin(admin.ModelAdmin):
	list_display = ['matricula', 'nome']
	search_fields = ['matricula', 'nome']
	list_filter = [('situacao_funcional__nome', custom_titled_filter('Situação Funcional')),'situacao_sindical', ('setor__nome', custom_titled_filter('Setor')), ('cargo__nome', custom_titled_filter('Cargo'))]

	inlines = [RamalInline]


class SituacaoFuncionalAdmin(admin.ModelAdmin):
	list_display = ['nome']
	search_fields = ['nome']	


class SetorAdmin(admin.ModelAdmin):
	list_display = ['nome']
	search_fields = ['nome']		


class CargoAdmin(admin.ModelAdmin):
	list_display = ['nome']
	search_fields = ['nome']	


admin.site.register(Filiado, FiliadoAdmin)	
admin.site.register(SituacaoFuncional, SituacaoFuncionalAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Cargo, CargoAdmin)