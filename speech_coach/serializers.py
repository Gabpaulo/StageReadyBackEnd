from rest_framework import serializers
from .models import SpeechAnalysis


class SpeechAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for SpeechAnalysis model
    """
    class Meta:
        model = SpeechAnalysis
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SpeechPredictionInputSerializer(serializers.Serializer):
    """
    Serializer for speech prediction input (audio features)
    """
    # Required features
    category = serializers.ChoiceField(
        choices=['Informative', 'Motivational', 'Persuasive'],
        required=False,
        allow_blank=True
    )
    loud_mean = serializers.FloatField()
    loud_std = serializers.FloatField()
    pause_ratio = serializers.FloatField()
    pitch_mean = serializers.FloatField()
    pitch_std = serializers.FloatField()
    syllables_per_sec = serializers.FloatField()
    spectral_centroid = serializers.FloatField()
    spectral_rolloff = serializers.FloatField()
    zcr_mean = serializers.FloatField()

    # MFCC features
    mfcc_1 = serializers.FloatField()
    mfcc_2 = serializers.FloatField()
    mfcc_3 = serializers.FloatField()
    mfcc_4 = serializers.FloatField()
    mfcc_5 = serializers.FloatField()
    mfcc_6 = serializers.FloatField()
    mfcc_7 = serializers.FloatField()
    mfcc_8 = serializers.FloatField()
    mfcc_9 = serializers.FloatField()
    mfcc_10 = serializers.FloatField()
    mfcc_11 = serializers.FloatField()
    mfcc_12 = serializers.FloatField()
    mfcc_13 = serializers.FloatField()

    # Additional features
    spectral_bandwidth = serializers.FloatField()
    spectral_flux = serializers.FloatField()
    chroma_mean = serializers.FloatField()

    # Optional
    words_per_minute = serializers.FloatField(required=False, allow_null=True)
    file_name = serializers.CharField(required=False, allow_blank=True)


class SpeechPredictionOutputSerializer(serializers.Serializer):
    """
    Serializer for speech prediction output
    """
    speech_pace = serializers.IntegerField()
    pausing_fluency = serializers.IntegerField()
    loudness_control = serializers.IntegerField()
    pitch_variation = serializers.IntegerField()
    articulation_clarity = serializers.IntegerField()
    expressive_emphasis = serializers.IntegerField()
    filler_words = serializers.IntegerField()
    overall = serializers.IntegerField()

    # Additional info
    feedback = serializers.DictField(required=False)
    recommendations = serializers.ListField(required=False)


class AudioFileAnalysisSerializer(serializers.Serializer):
    """
    Serializer for audio file upload and analysis
    """
    audio_file = serializers.FileField(required=True)
    category = serializers.CharField(required=False, allow_blank=True)
