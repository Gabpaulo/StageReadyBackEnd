"""
Audio Feature Extraction Utilities
Extracts speech features from audio files for ML model prediction
"""
import librosa
import numpy as np
from pathlib import Path
import speech_recognition as sr


class AudioFeatureExtractor:
    """Extract features from audio files for speech analysis"""

    def __init__(self):
        self.sr = 22050  # Sample rate for librosa
        self.recognizer = sr.Recognizer()

    def extract_features(self, audio_path):
        """
        Extract all required features from an audio file

        Args:
            audio_path: Path to audio file

        Returns:
            dict: Dictionary of extracted features
        """
        # Load audio file
        y, sr = librosa.load(audio_path, sr=self.sr)

        # Basic audio metrics
        duration = librosa.get_duration(y=y, sr=sr)

        # Loudness (RMS Energy)
        rms = librosa.feature.rms(y=y)[0]
        loud_mean = float(np.mean(rms))
        loud_std = float(np.std(rms))

        # Pitch (Fundamental Frequency)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Only use non-zero pitches
                pitch_values.append(pitch)

        pitch_mean = float(np.mean(pitch_values)) if pitch_values else 0.0
        pitch_std = float(np.std(pitch_values)) if pitch_values else 0.0

        # Pause Detection (using silence detection)
        # Non-silent intervals
        intervals = librosa.effects.split(y, top_db=20)
        non_silent_duration = sum([interval[1] - interval[0] for interval in intervals]) / sr
        pause_duration = duration - non_silent_duration
        pause_ratio = float(pause_duration / duration) if duration > 0 else 0.0

        # Speech Rate (syllables per second - approximation using onset strength)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        syllables_per_sec = float(len(onset_frames) / duration) if duration > 0 else 0.0

        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_centroid = float(np.mean(spectral_centroids))

        spectral_rolloffs = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_rolloff = float(np.mean(spectral_rolloffs))

        spectral_bandwidths = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        spectral_bandwidth = float(np.mean(spectral_bandwidths))

        # Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = float(np.mean(zcr))

        # MFCCs (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_features = {}
        for i in range(13):
            mfcc_features[f'mfcc_{i+1}'] = float(np.mean(mfccs[i]))

        # Chroma features
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = float(np.mean(chroma))

        # Spectral Flux (approximation using spectral contrast)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_flux = float(np.mean(spectral_contrast))

        # Compile all features
        features = {
            'duration': duration,  # Audio duration in seconds
            'loud_mean': loud_mean,
            'loud_std': loud_std,
            'pause_ratio': pause_ratio,
            'pitch_mean': pitch_mean,
            'pitch_std': pitch_std,
            'syllables_per_sec': syllables_per_sec,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'zcr_mean': zcr_mean,
            'spectral_bandwidth': spectral_bandwidth,
            'spectral_flux': spectral_flux,
            'chroma_mean': chroma_mean,
            **mfcc_features,  # Adds mfcc_1 through mfcc_13
        }

        return features

    def extract_transcript(self, audio_path):
        """
        Extract transcript from audio file using speech recognition

        Args:
            audio_path: Path to audio file

        Returns:
            str: Transcribed text
        """
        try:
            # Convert audio to WAV format if needed for better compatibility
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                # Use Google Speech Recognition (free)
                transcript = self.recognizer.recognize_google(audio_data)
                return transcript
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error during transcription: {str(e)}"

    def extract_transcript_from_bytes(self, audio_bytes, file_extension='wav'):
        """
        Extract transcript from audio file bytes

        Args:
            audio_bytes: Audio file as bytes
            file_extension: File extension (wav, webm, mp3, etc.)

        Returns:
            str: Transcribed text
        """
        import tempfile
        import os
        from pydub import AudioSegment

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        try:
            # Convert to WAV if not already
            if file_extension.lower() != 'wav':
                audio = AudioSegment.from_file(temp_path, format=file_extension)
                wav_path = temp_path.replace(f'.{file_extension}', '.wav')
                audio.export(wav_path, format='wav')
                transcript = self.extract_transcript(wav_path)
                os.unlink(wav_path)
            else:
                transcript = self.extract_transcript(temp_path)

            return transcript
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def extract_features_from_bytes(self, audio_bytes, file_extension='wav'):
        """
        Extract features from audio file bytes

        Args:
            audio_bytes: Audio file as bytes
            file_extension: File extension (wav, webm, mp3, etc.)

        Returns:
            dict: Dictionary of extracted features
        """
        import tempfile
        import os

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        try:
            # Extract features
            features = self.extract_features(temp_path)
            return features
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def extract_audio_features(audio_path_or_bytes, is_bytes=False, file_extension='wav'):
    """
    Convenience function to extract features from audio

    Args:
        audio_path_or_bytes: Path to audio file or audio bytes
        is_bytes: Whether input is bytes (True) or path (False)
        file_extension: File extension if is_bytes=True

    Returns:
        dict: Dictionary of extracted features
    """
    extractor = AudioFeatureExtractor()

    if is_bytes:
        return extractor.extract_features_from_bytes(audio_path_or_bytes, file_extension)
    else:
        return extractor.extract_features(audio_path_or_bytes)
