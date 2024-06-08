from django.contrib import admin
from .models import ScrapeJob, CoinData


@admin.register(ScrapeJob)
class ScrapeJobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'created_at')
    search_fields = ('job_id',)


@admin.register(CoinData)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ('job', 'coin', 'data')
    search_fields = ('job__job_id', 'coin')
