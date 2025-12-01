import matplotlib.pyplot as plt

# Bitrates used in Section 3.2
bitrates = [16, 32, 64, 128]   # kbps

# Corresponding MOS values from your updated table
mos_values = [2.2, 2.7, 3.5, 4.0]

plt.figure(figsize=(6,4))
plt.plot(bitrates, mos_values, marker='o', linewidth=2)

plt.title("MP3 Bitrate vs MOS")
plt.xlabel("Bitrate (kbps)")
plt.ylabel("Mean Opinion Score (MOS)")
plt.ylim(1.5, 4.5)
plt.grid(True)

plt.tight_layout()
plt.savefig("mp3_mos_curve.png", dpi=300)
plt.close()
