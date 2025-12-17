from django.contrib import admin
from .models import SpeechAnalysis, TrainingDataset


@admin.register(SpeechAnalysis)
class SpeechAnalysisAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'category', 'overall', 'created_at']
    list_filter = ['category', 'overall', 'created_at']
    search_fields = ['file_name', 'strengths', 'areas_for_improvement']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TrainingDataset)
class TrainingDatasetAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'category', 'overall', 'created_at']
    list_filter = ['category', 'overall']
    search_fields = ['file_name']
