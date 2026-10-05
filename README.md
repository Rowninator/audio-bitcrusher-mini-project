# Project Overview

The bitcrusher project processes audio files by reducing their bit depth and effective sampling resolution, creating a distorted sound effect. The signal chain involves reading a WAV file, applying quantization to reduce the bit depth, and then reducing the effective sampling resolution by retaining every rate_factor-th sample and holding it across the following samples. The bit_depth parameter controls how many bits are used to represent each audio sample, while the rate_factor controls effective time resolution and creates the bitcrusher texture both of which contribute to the overall degradation of the audio quality.

## Signal Chain

In a live path, the audio signal is first captured by an ADC converter processed digitally and then converted back to analog by a DAC for playback. In contrast, the WAV-file path used in this project starts with audio that is already in digital form, so the ADC step is bypassed, and only the DAC is involved during playback, as the audio is read from a file and sent directly to the output device.

## Quantization and Bit Depth

2^B determines the number of quantization levels, where B is the bit depth, an 8-bit depth provides 256 levels and a 4-bit depth provides 16 levels. Lowering the bit depth increases quantization error because there are fewer levels to represent the audio signal. When comparing 8-bit and 4-bit audio, the 4-bit audio sounded more distorted and noisy because of the increased quantization error


## Rate Reduction and Aliasing
 
Increasing the rate_factor reduces the time resolution of the audio by downsampling it. unfiltered reduction can create aliasing because high frequency components may fold back into lower frequencies and distort the signal. correct resampling uses an anti alias filter first to remove these high frequency components before downsampling which prevents aliasing.

## Real-Time Processing

The callback function processes one chunk of audio at a time and applying the bitcrushing effect before sending it to the output buffer. This processing has to finish fast enough to avoid audio glitches. Therefore, efficient processing is crucial to maintain smooth and continuous audio output.

## Debugging Lesson

The bug occurred because the processed audio was saved with incorrect sample rate metadata, which caused it to play back slower and at a lower pitch than intended. This happened because the playback device interpreted the audio data as having a different sample rate than it was actually recorded at. 44.1 kHz was the correct output rate by checking the original sample rate of the input WAV file

## Final Musical Experiment and What I Learned

I chose 8-bit + ×8 as my main preset because it provided a nice lofi effect without completely obstructing quality. When applied to saturn.wav, the effect produced a gritty, vintage sound while on hammond.wav, it created a more pronounced distortion that emphasized the soound of the organ. I learned that “bit depth primarily affects amplitude resolution and quantization error, while rate reduction influences the time resolution and can lead to aliasing artifacts.