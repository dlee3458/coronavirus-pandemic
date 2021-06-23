from django.contrib import admin
from .models import Record, Country, Unemployment, ChartConfirmedData, ChartDeathData, ChartVaccinationData, HistoricalConfirmedData, HistoricalDeathData, HistoricalVaccinationData

admin.site.register(Record)
admin.site.register(Country)
admin.site.register(Unemployment)
admin.site.register(ChartConfirmedData)
admin.site.register(ChartDeathData)
admin.site.register(ChartVaccinationData)
admin.site.register(HistoricalConfirmedData)
admin.site.register(HistoricalDeathData)
admin.site.register(HistoricalVaccinationData)
