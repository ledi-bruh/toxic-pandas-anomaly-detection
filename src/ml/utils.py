import librosa
import noisereduce as nr
import numpy as np
from scipy.signal import welch


def reduce_noise(audio, sample_rate):
    return nr.reduce_noise(y=audio, sr=sample_rate)


def extract_features(
    array: np.ndarray,
    sample_rate: int,
    channel: int | None = None,
):
    audio = array

    if channel is None:
        # моно
        audio = audio.mean(axis=0)
    elif channel < audio.shape[0]:
        # иначе извлекаем канал
        audio = audio[channel]

    # Удаление шума
    audio = reduce_noise(audio=audio, sample_rate=sample_rate)

    # Извлечение мелспектрограммы
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate, n_mels=40, fmax=8000)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    mel_features = np.mean(mel_spectrogram_db.T, axis=0)

    # Извлечение спектра Уэльса (PSD)
    freqs, psd = welch(audio, fs=sample_rate)

    # Объединение признаков в один вектор
    combined_features = np.hstack((mel_features, psd))

    return combined_features


def source_predict(features, pipeline) -> tuple[np.ndarray, int]:
    features = features.reshape(1, -1)
    probs = pipeline.predict_proba(features)
    return probs.squeeze(), int(probs.argmax().item())
