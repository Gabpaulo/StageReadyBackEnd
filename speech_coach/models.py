from django.db import models
from django.contrib.auth.models import User


class SpeechAnalysis(models.Model):
    """
    Model to store speech analysis results
    """
    CATEGORY_CHOICES = [
        ('informative', 'Informative'),
        ('motivational', 'Motivational'),
        ('persuasive', 'Persuasive'),
    ]

    # User and file info
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    audio_file = models.FileField(upload_to='speeches/', null=True, blank=True)

    # Audio features (extracted from audio)
    duration_s = models.FloatField(null=True, blank=True)
    loud_mean = models.FloatField(null=True, blank=True)
    loud_std = models.FloatField(null=True, blank=True)
    pause_ratio = models.FloatField(null=True, blank=True)
    pitch_mean = models.FloatField(null=True, blank=True)
    pitch_std = models.FloatField(null=True, blank=True)
    syllables_per_sec = models.FloatField(null=True, blank=True)
    spectral_centroid = models.FloatField(null=True, blank=True)
    spectral_rolloff = models.FloatField(null=True, blank=True)
    words_per_minute = models.FloatField(null=True, blank=True)
    zcr_mean = models.FloatField(null=True, blank=True)

    # MFCC features
    mfcc_1 = models.FloatField(null=True, blank=True)
    mfcc_2 = models.FloatField(null=True, blank=True)
    mfcc_3 = models.FloatField(null=True, blank=True)
    mfcc_4 = models.FloatField(null=True, blank=True)
    mfcc_5 = models.FloatField(null=True, blank=True)
    mfcc_6 = models.FloatField(null=True, blank=True)
    mfcc_7 = models.FloatField(null=True, blank=True)
    mfcc_8 = models.FloatField(null=True, blank=True)
    mfcc_9 = models.FloatField(null=True, blank=True)
    mfcc_10 = models.FloatField(null=True, blank=True)
    mfcc_11 = models.FloatField(null=True, blank=True)
    mfcc_12 = models.FloatField(null=True, blank=True)
    mfcc_13 = models.FloatField(null=True, blank=True)

    # Additional features
    spectral_bandwidth = models.FloatField(null=True, blank=True)
    spectral_flux = models.FloatField(null=True, blank=True)
    chroma_mean = models.FloatField(null=True, blank=True)

    # Predicted scores (1-5 scale) - ML model outputs
    speech_pace = models.IntegerField(null=True, blank=True)
    pausing_fluency = models.IntegerField(null=True, blank=True)
    loudness_control = models.IntegerField(null=True, blank=True)
    pitch_variation = models.IntegerField(null=True, blank=True)
    articulation_clarity = models.IntegerField(null=True, blank=True)
    expressive_emphasis = models.IntegerField(null=True, blank=True)
    filler_words = models.IntegerField(null=True, blank=True)
    overall = models.IntegerField(null=True, blank=True)

    # Feedback text
    strengths = models.TextField(blank=True, null=True)
    areas_for_improvement = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Speech Analysis'
        verbose_name_plural = 'Speech Analyses'

    def __str__(self):
        return f"{self.file_name} - Overall: {self.overall}/5"


class TrainingDataset(models.Model):
    """
    Model to store training dataset records
    """
    file_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=20)

    # All feature fields (same as SpeechAnalysis)
    loud_mean = models.FloatField()
    loud_std = models.FloatField()
    pause_ratio = models.FloatField()
    pitch_mean = models.FloatField()
    pitch_std = models.FloatField()
    syllables_per_sec = models.FloatField()
    spectral_centroid = models.FloatField()
    spectral_rolloff = models.FloatField()
    words_per_minute = models.FloatField(null=True, blank=True)
    zcr_mean = models.FloatField()

    # MFCC features
    mfcc_1 = models.FloatField()
    mfcc_2 = models.FloatField()
    mfcc_3 = models.FloatField()
    mfcc_4 = models.FloatField()
    mfcc_5 = models.FloatField()
    mfcc_6 = models.FloatField()
    mfcc_7 = models.FloatField()
    mfcc_8 = models.FloatField()
    mfcc_9 = models.FloatField()
    mfcc_10 = models.FloatField()
    mfcc_11 = models.FloatField()
    mfcc_12 = models.FloatField()
    mfcc_13 = models.FloatField()

    spectral_bandwidth = models.FloatField()
    spectral_flux = models.FloatField()
    chroma_mean = models.FloatField()

    # Expert labels
    speech_pace = models.IntegerField()
    pausing_fluency = models.IntegerField()
    loudness_control = models.IntegerField()
    pitch_variation = models.IntegerField()
    articulation_clarity = models.IntegerField()
    expressive_emphasis = models.IntegerField()
    filler_words = models.IntegerField()
    overall = models.IntegerField()

    strengths = models.TextField(blank=True, null=True)
    areas_for_improvement = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
