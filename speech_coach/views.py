from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from pathlib import Path
import sys

from .models import SpeechAnalysis
from .serializers import (
    SpeechAnalysisSerializer,
    SpeechPredictionInputSerializer,
    SpeechPredictionOutputSerializer,
    AudioFileAnalysisSerializer
)

# Add ml_models to path
sys.path.append(str(Path(settings.BASE_DIR) / 'ml_models'))
from speech_predictor import SpeechPredictor
from audio_processor import AudioFeatureExtractor


class SpeechAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing speech analysis records
    """
    queryset = SpeechAnalysis.objects.all()
    serializer_class = SpeechAnalysisSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.predictor = None
        self._load_model()

    def _load_model(self):
        """Load the trained ML model"""
        try:
            model_dir = settings.ML_MODELS_DIR
            if Path(model_dir).exists():
                self.predictor = SpeechPredictor()
                self.predictor.load(model_dir)
                print("ML model loaded successfully")
            else:
                print(f"Warning: Model directory not found at {model_dir}")
                print("Please train the model first using: python ml_models/train_model.py")
        except Exception as e:
            print(f"Error loading model: {e}")

    @action(detail=False, methods=['post'])
    def predict(self, request):
        """
        Predict speech quality scores from audio features

        POST /api/speech-analysis/predict/
        Body: Audio features (JSON)
        Returns: Predicted scores (1-5 scale)
        """
        # Validate input
        input_serializer = SpeechPredictionInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(
                {'error': 'Invalid input', 'details': input_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if model is loaded
        if self.predictor is None or not self.predictor.is_trained:
            return Response(
                {'error': 'ML model not loaded. Please train the model first.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Get predictions
        try:
            features = input_serializer.validated_data
            predictions = self.predictor.predict(features)

            # Generate feedback
            feedback = self._generate_feedback(predictions, features)
            recommendations = self._generate_recommendations(predictions)

            # Prepare response
            response_data = {
                **predictions,
                'feedback': feedback,
                'recommendations': recommendations
            }

            output_serializer = SpeechPredictionOutputSerializer(data=response_data)
            if output_serializer.is_valid():
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'Prediction failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """
        Analyze audio file and predict speech quality scores

        POST /api/speech-analysis/analyze/
        Body: FormData with audio_file and category
        Returns: Predicted scores (1-5 scale) with feedback
        """
        # Debug logging
        print("=== Analyze Endpoint Called ===")
        print(f"Request data keys: {request.data.keys()}")
        print(f"Request FILES: {request.FILES.keys()}")
        print(f"Category: {request.data.get('category', 'Not provided')}")

        # Validate input
        input_serializer = AudioFileAnalysisSerializer(data=request.data)
        if not input_serializer.is_valid():
            print(f"Validation errors: {input_serializer.errors}")
            return Response(
                {'error': 'Invalid input', 'details': input_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if model is loaded
        if self.predictor is None or not self.predictor.is_trained:
            return Response(
                {'error': 'ML model not loaded. Please train the model first.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            # Get uploaded file
            audio_file = input_serializer.validated_data['audio_file']
            category = input_serializer.validated_data.get('category', '')

            # Extract features from audio file
            audio_extractor = AudioFeatureExtractor()
            audio_bytes = audio_file.read()

            # Determine file extension
            file_name = audio_file.name
            file_extension = file_name.split('.')[-1] if '.' in file_name else 'webm'

            # Extract features
            features = audio_extractor.extract_features_from_bytes(
                audio_bytes,
                file_extension=file_extension
            )

            # Add category if provided
            if category:
                features['category'] = category

            # Get predictions
            predictions = self.predictor.predict(features)

            # Generate feedback
            feedback = self._generate_feedback(predictions, features)
            recommendations = self._generate_recommendations(predictions)

            # Prepare response
            response_data = {
                **predictions,
                'feedback': feedback,
                'recommendations': recommendations
            }

            output_serializer = SpeechPredictionOutputSerializer(data=response_data)
            if output_serializer.is_valid():
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': 'Analysis failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def model_info(self, request):
        """
        Get information about the loaded ML model

        GET /api/speech-analysis/model_info/
        """
        if self.predictor is None:
            return Response(
                {'status': 'Model not loaded'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            info = {
                'model_type': self.predictor.model_type,
                'is_trained': self.predictor.is_trained,
                'features': self.predictor.FEATURE_COLUMNS,
                'targets': self.predictor.TARGET_COLUMNS,
            }

            # Get feature importance if available
            if self.predictor.model_type == 'random_forest' and self.predictor.is_trained:
                importance_df = self.predictor.get_feature_importance()
                info['feature_importance'] = importance_df.to_dict('records')

            return Response(info, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _generate_feedback(self, predictions, features):
        """Generate human-readable feedback based on predictions"""
        feedback = {
            'overall_assessment': self._get_overall_assessment(predictions['overall']),
            'detailed_scores': {}
        }

        score_descriptions = {
            'speech_pace': {
                1: 'Too slow - consider increasing your speaking rate',
                2: 'Somewhat slow - try to pick up the pace slightly',
                3: 'Adequate pace - could be improved',
                4: 'Good pace - easy to follow',
                5: 'Excellent pace - perfectly balanced'
            },
            'pausing_fluency': {
                1: 'Poor pausing - work on strategic pauses',
                2: 'Below average fluency - practice smoother transitions',
                3: 'Adequate pausing - room for improvement',
                4: 'Good use of pauses - natural flow',
                5: 'Excellent fluency - masterful use of pauses'
            },
            'loudness_control': {
                1: 'Poor volume control - work on projection',
                2: 'Inconsistent volume - practice control',
                3: 'Adequate volume - could be more dynamic',
                4: 'Good volume control - well modulated',
                5: 'Excellent volume control - perfect projection'
            },
            'pitch_variation': {
                1: 'Monotonous - add vocal variety',
                2: 'Limited variation - practice intonation',
                3: 'Some variation - could be more expressive',
                4: 'Good pitch variation - engaging delivery',
                5: 'Excellent vocal variety - very expressive'
            },
            'articulation_clarity': {
                1: 'Poor articulation - focus on clarity',
                2: 'Unclear at times - improve enunciation',
                3: 'Generally clear - some improvement needed',
                4: 'Clear articulation - easy to understand',
                5: 'Excellent clarity - perfectly articulated'
            },
            'expressive_emphasis': {
                1: 'Lacks expression - work on emphasis',
                2: 'Limited expression - add more emotion',
                3: 'Some expression - could be more impactful',
                4: 'Good expression - engaging delivery',
                5: 'Highly expressive - captivating emphasis'
            },
            'filler_words': {
                1: 'Excessive fillers - significant improvement needed',
                2: 'Too many fillers - practice reducing them',
                3: 'Some fillers present - work on elimination',
                4: 'Few fillers - minimal distraction',
                5: 'No fillers - clean, professional delivery'
            }
        }

        for metric, score in predictions.items():
            if metric != 'overall' and metric in score_descriptions:
                feedback['detailed_scores'][metric] = {
                    'score': score,
                    'description': score_descriptions[metric].get(score, 'N/A')
                }

        return feedback

    def _generate_recommendations(self, predictions):
        """Generate actionable recommendations based on scores"""
        recommendations = []

        # Check each score and provide targeted advice
        if predictions['speech_pace'] <= 3:
            recommendations.append({
                'category': 'Speech Pace',
                'issue': 'Pacing needs improvement',
                'suggestion': 'Practice speaking at a consistent rate of 140-160 words per minute. Use a timer during practice.'
            })

        if predictions['pausing_fluency'] <= 3:
            recommendations.append({
                'category': 'Pausing & Fluency',
                'issue': 'Inconsistent pausing',
                'suggestion': 'Use strategic pauses after key points. Pause for 1-2 seconds between major ideas.'
            })

        if predictions['loudness_control'] <= 3:
            recommendations.append({
                'category': 'Volume Control',
                'issue': 'Volume inconsistency',
                'suggestion': 'Practice projecting from your diaphragm. Vary volume for emphasis but maintain audibility.'
            })

        if predictions['pitch_variation'] <= 3:
            recommendations.append({
                'category': 'Pitch Variation',
                'issue': 'Limited vocal variety',
                'suggestion': 'Practice varying your pitch to emphasize key words. Avoid monotone delivery.'
            })

        if predictions['articulation_clarity'] <= 3:
            recommendations.append({
                'category': 'Articulation',
                'issue': 'Clarity needs work',
                'suggestion': 'Practice tongue twisters and enunciate consonants clearly. Slow down if needed for clarity.'
            })

        if predictions['expressive_emphasis'] <= 3:
            recommendations.append({
                'category': 'Expression',
                'issue': 'Lacks emotional impact',
                'suggestion': 'Connect emotionally with your content. Use vocal variety to convey passion and conviction.'
            })

        if predictions['filler_words'] <= 3:
            recommendations.append({
                'category': 'Filler Words',
                'issue': 'Too many filler words',
                'suggestion': 'Practice pausing instead of using "um", "uh", "like". Record yourself to identify patterns.'
            })

        # Add general recommendations
        if predictions['overall'] >= 4:
            recommendations.append({
                'category': 'Overall',
                'issue': 'Strong performance',
                'suggestion': 'Great job! Continue refining your skills with regular practice and seek diverse speaking opportunities.'
            })
        elif predictions['overall'] <= 2:
            recommendations.append({
                'category': 'Overall',
                'issue': 'Needs significant improvement',
                'suggestion': 'Focus on fundamentals: clear articulation, consistent pacing, and regular practice. Consider joining a public speaking group.'
            })

        return recommendations

    def _get_overall_assessment(self, score):
        """Get overall assessment text based on score"""
        assessments = {
            1: 'Needs significant improvement - Focus on fundamentals',
            2: 'Below average - Practice key speaking techniques',
            3: 'Average performance - Room for growth',
            4: 'Good performance - Strong speaking skills',
            5: 'Excellent performance - Outstanding speaker'
        }
        return assessments.get(score, 'N/A')
