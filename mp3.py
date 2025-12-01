import os
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import spectrogram

# ----------------------------------------------------------
# SETUP
# ----------------------------------------------------------
input_wav = "original.wav"   # Your 10MB file-examples.com WAV
output_folder = "mp3_spectrograms"
os.makedirs(output_folder, exist_ok=True)

bitrates = [128, 64, 32, 16]  # kbps (extremely low)
spectros = {}

# Load WAV
sr, data = wavfile.read(input_wav)

# Convert stereo to mono
if len(data.shape) == 2:
    data_mono = data.mean(axis=1)
else:
    data_mono = data

# Crop a highly active region (20.00 to 20.10 sec)
start = int(sr * 20.00)
end = int(sr * 20.10)
crop_original = data_mono[start:end]
spectros["original"] = crop_original

# ----------------------------------------------------------
# ENCODE & EXTRACT SPECTROGRAMS
# ----------------------------------------------------------
original_audio = AudioSegment.from_wav(input_wav)

for br in bitrates:
    out_path = f"{output_folder}/audio_{br}kbps.mp3"
    original_audio.export(out_path, format="mp3", bitrate=f"{br}k")

    # Load MP3 version
    mp3_audio = AudioSegment.from_mp3(out_path)
    samples = np.array(mp3_audio.get_array_of_samples())

    if mp3_audio.channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)

    crop = samples[start:end]
    spectros[f"{br}kbps"] = crop

# ----------------------------------------------------------
# PLOTTING FUNCTION
# ----------------------------------------------------------
def plot_spectrogram(sig, title, filename):
    f, t, Sxx = spectrogram(sig, fs=sr, nperseg=256, noverlap=128)
    plt.figure(figsize=(6, 4))
    plt.pcolormesh(t, f, 10*np.log10(Sxx + 1e-8), shading="gouraud")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.title(title)
    plt.colorbar(label="Power (dB)")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/{filename}", dpi=300)
    plt.close()

# ----------------------------------------------------------
# GENERATE FIGURES
# ----------------------------------------------------------
plot_spectrogram(spectros["original"], 
                 "Original WAV Spectrogram (20 ms)", 
                 "spec_original.png")

plot_spectrogram(spectros["128kbps"], 
                 "MP3 128 kbps Spectrogram (20 ms)", 
                 "spec_128.png")

plot_spectrogram(spectros["64kbps"], 
                 "MP3 64 kbps Spectrogram (20 ms)", 
                 "spec_64.png")

plot_spectrogram(spectros["32kbps"], 
                 "MP3 32 kbps Spectrogram (20 ms)", 
                 "spec_32.png")

plot_spectrogram(spectros["16kbps"], 
                 "MP3 16 kbps Spectrogram (20 ms)", 
                 "spec_16.png")
