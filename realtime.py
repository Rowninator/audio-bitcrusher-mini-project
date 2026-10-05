import sounddevice as sd
import soundfile as sf
import numpy as np

def bitcrush(chunk, bit_depth, rate_factor):
    # move the quantization + rate-reduction logic you already wrote into this function and have it return the processed chunk.
    delta = 2 / (2 ** bit_depth)
    quantized_chunk = np.round(chunk / delta) * delta
    quantized_chunk = quantized_chunk[::rate_factor]
    quantized_chunk = np.repeat(quantized_chunk, rate_factor, axis=0)[:len(chunk)]
    return quantized_chunk

audio, sample_rate = sf.read(
    "hammond.wav",
    dtype="float32",
    always_2d=True
)

position = 0

# n factor
rate_factor = 8

# bit depth reduction to each real-time buffer
bit_depth = 8

def callback(outdata, frames, time, status):
    global position

    end = min(position + frames, len(audio))
    chunk = audio[position:end]

    

    # 8-bit quantization to each real-time buffer
    quantized_chunk = bitcrush(chunk, bit_depth, rate_factor)


    outdata.fill(0)
    outdata[:len(quantized_chunk)] = quantized_chunk * 0.1

    

    position = end

    if position >= len(audio):
        raise sd.CallbackStop

    

with sd.OutputStream(
    device=5,
    samplerate=sample_rate,
    channels=2,
    dtype="float32",
    blocksize=1024,
    callback=callback,
    latency="high",
):
    sd.sleep(int((len(audio) / sample_rate + 1) * 1000))

# Call bitcrush() on the full audio array.
quantized_audio = bitcrush(audio, bit_depth, rate_factor)

# Save the result with sf.write(...) at the original sample_rate of 44.1 kHz.
sf.write("quantized_audio.wav", quantized_audio, sample_rate)

# write just one SHORT paragraph in your own words covering: what the bitcrusher project does, the signal chain you actually used with WAV files, what bit_depth changes, and what rate_factor changes
# The bitcrusher project processes audio files by reducing their bit depth and sample rate, creating a distorted, lo-fi sound effect. The signal chain involves reading a WAV file, applying quantization to reduce the bit depth (which affects the dynamic range and introduces quantization noise), and then downsampling the audio by a specified rate factor (which reduces the sample rate and can introduce aliasing). The bit_depth parameter controls how many bits are used to represent each audio sample, while the rate_factor determines how much the audio is downsampled, both of which contribute to the overall degradation of the audio quality.

# 2–3 sentences in your own words explaining the difference between: - a live path: sound → ADC → digital processing → DAC → sound - the WAV-file path you actually used, where the audio was already digital and only the DAC was physically exercised during playback.
# In a live path, the audio signal is first captured by an analog-to-digital converter (ADC), processed digitally, and then converted back to analog by a digital-to-analog converter (DAC) for playback. In contrast, the WAV-file path used in this project starts with audio that is already in digital form, so the ADC step is bypassed, and only the DAC is involved during playback, as the audio is read from a file and sent directly to the output device.


# 2–3 sentences explaining: how \(2^B\) determines the available quantization levels, why lowering bit_depth increases quantization error, what you heard when comparing 8-bit and 4-bit audio.
# The expression \(2^B\) determines the number of available quantization levels, where \(B\) is the bit depth; for example, an 8-bit depth provides 256 levels, while a 4-bit depth provides only 16 levels. Lowering the bit depth increases quantization error because there are fewer levels to represent the audio signal, leading to greater discrepancies between the original and quantized signals. When comparing 8-bit and 4-bit audio, the 4-bit audio sounded significantly more distorted and noisy due to the increased quantization error and loss of detail.

# # Write 2–3 sentences explaining what increasing rate_factor does to the effective time resolution, why crude unfiltered reduction can create aliasing/artifacts, and why proper resampling uses an anti-alias filter first.
# Increasing the rate_factor reduces the effective time resolution of the audio signal by downsampling it, which means fewer samples are used to represent the same duration of sound. Crude unfiltered reduction can create aliasing and artifacts because high-frequency components may fold back into lower frequencies, distorting the signal. Proper resampling uses an anti-alias filter first to remove these high-frequency components before downsampling, preventing aliasing and preserving the integrity of the audio signal.


#  Write 2–3 sentences explaining how the callback processes one chunk at a time and why that processing has to finish quickly enough to avoid audio glitches
# The callback function processes one chunk of audio at a time, reading a segment of the audio array and applying the bitcrushing effect before sending it to the output buffer. This processing must finish quickly enough to avoid audio glitches because if the callback takes too long, the output buffer may underflow, resulting in gaps or pops in the audio playback. Therefore, efficient processing is crucial to maintain smooth and continuous audio output.

# Write 2–3 sentences explaining the bug where we saved the processed audio at the wrong sample-rate metadata, why it played slower and deeper, and how you determined that 44.1 kHz was the correct output rate.
# The bug occurred because the processed audio was saved with incorrect sample-rate metadata, which caused it to play back slower and at a lower pitch than intended. This happened because the playback device interpreted the audio data as having a different sample rate than it was actually recorded at. I determined that 44.1 kHz was the correct output rate by checking the original sample rate of the input WAV file and ensuring that the processed audio was saved with the same sample rate to maintain proper playback speed and pitch.


# Write 3–4 sentences explaining why you chose 8-bit + ×8 as your main preset, how it behaved on saturn.wav versus hammond.wav, and what you learned about the separate roles of bit depth and rate reduction.
# I chose 8-bit + ×8 as my main preset because it provided a noticeable lo-fi effect without completely degrading the audio quality, striking a balance between distortion and clarity. When applied to saturn.wav, the effect produced a gritty, vintage sound that retained some musicality, while on hammond.wav, it created a more pronounced distortion that emphasized the harmonic content of the organ. Through this experimentation, I learned that bit depth primarily affects the dynamic range and introduces quantization noise, while rate reduction influences the temporal resolution and can lead to aliasing artifacts. This distinction helped me understand how to manipulate both parameters to achieve different sonic textures in audio processing.