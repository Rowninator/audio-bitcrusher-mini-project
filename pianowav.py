import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import resample_poly
from scipy.fft import rfft, rfftfreq

audio, sample_rate = sf.read("paino.wav")

print("Sample rate:", sample_rate)
print("Shape:", audio.shape)
print("Duration:", len(audio) / sample_rate, "seconds")
print(audio[:5])

# 4 bit quntization

delta = 0.125
quantized_audio = np.round(audio / delta) * delta

e = audio - quantized_audio

print("Original min/max:", audio.min(), audio.max())
print("Quantized min/max:", quantized_audio.min(), quantized_audio.max())
print("Max quantization error:", np.max(np.abs(e)))

# 8 bit quantization
delta_8bit = 0.0078125

quantized_audio_8bit = np.round(audio / delta_8bit) * delta_8bit
e_8bit = audio - quantized_audio_8bit

print("Max 8-bit quantization error:", np.max(np.abs(e_8bit)))

# x4 crude rate reduction
every_4th = audio[::4]
repeated_samples = np.repeat(every_4th, 4, axis=0)[:len(audio)]

print("Original shape:", audio.shape)
print("Repeated shape:", repeated_samples.shape)

# filter and downsample by 4
proper_down = resample_poly(audio, 1, 4, axis=0)

print("Original shape:", audio.shape)
print("Proper-downsampled shape:", proper_down.shape)


# combined 4bit x4 bitcrusher
crushed_amp = np.round(audio / 0.125) * 0.125

every_4th_crushed = crushed_amp[::4]
repeated_samples_crushed = np.repeat(
    every_4th_crushed, 4, axis=0
)[:len(audio)]

print("Original:", audio.shape)
print("Combined:", repeated_samples_crushed.shape)


# combined 8bit x4 bitcrusher
every_4th_8bit = quantized_audio_8bit[::4]
repeated_samples_8bit = np.repeat(
    every_4th_8bit, 4, axis=0
)[:len(audio)]

print("Original:", audio.shape)
print("Combined 8-bit:", repeated_samples_8bit.shape)