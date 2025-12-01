import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

# ---------------------------
# Load original image
# ---------------------------

input_path = "kodim20.png"
img = Image.open(input_path).convert("RGB")
img_np = np.array(img)
orig_size = os.path.getsize(input_path) / 1024

print("Loaded image:", input_path)
print("Resolution:", img.size)
print("Original size:", f"{orig_size:.1f} KB")

# ---------------------------
# Choose a high-frequency crop
# ---------------------------

# Crop region with metal textures and text — adjust if needed
crop_box = (200, 150, 350, 300)   # (left, upper, right, lower)
crop = img.crop(crop_box)

# Save crop reference
crop.save("crop_reference.png")

qualities = [95, 75, 50, 30, 10]
results = []

for q in qualities:
    out_path = f"kodim20_q{q}.jpg"
    img.save(out_path, "JPEG", quality=q)

    comp_img = Image.open(out_path).convert("RGB")
    comp_np = np.array(comp_img)

    # Metrics
    psnr = peak_signal_noise_ratio(img_np, comp_np)
    ssim = structural_similarity(img_np, comp_np, channel_axis=2)

    # File size
    file_size = os.path.getsize(out_path) / 1024
    ratio = orig_size / file_size

    results.append((q, file_size, ratio, psnr, ssim))

    # ---------------------------
    # Create crop comparison figure
    # ---------------------------

    comp_crop = comp_img.crop(crop_box)

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    ax[0].imshow(crop)
    ax[0].set_title("Original (crop)")
    ax[0].axis("off")

    ax[1].imshow(comp_crop)
    ax[1].set_title(f"JPEG Q={q} (crop)")
    ax[1].axis("off")

    fig.suptitle(f"Artifact Zoom Comparison: Q={q}", fontsize=14)
    fig.savefig(f"artifact_zoom_q{q}.png", dpi=300)
    plt.close(fig)

# ---------------------------
# Print results
# ---------------------------

print("\nJPEG Compression Results:")
print("Quality | File Size (KB) | Ratio | PSNR | SSIM")
for r in results:
    print(f"{r[0]:>6} | {r[1]:10.1f} | {r[2]:6.2f}:1 | {r[3]:5.2f} dB | {r[4]:.3f}")

# ---------------------------
# PSNR curve
# ---------------------------

qualities_sorted = [r[0] for r in results]
psnr_values = [r[3] for r in results]

plt.figure(figsize=(7,5))
plt.plot(qualities_sorted, psnr_values, marker='o')
plt.title("JPEG Quality vs PSNR (Kodak Image 20)")
plt.xlabel("JPEG Quality")
plt.ylabel("PSNR (dB)")
plt.grid(True)
plt.savefig("jpeg_psnr_curve.png", dpi=300)
plt.close()

print("\nGenerated files:")
print("- artifact_zoom_q95.png")
print("- artifact_zoom_q75.png")
print("- artifact_zoom_q50.png")
print("- artifact_zoom_q30.png")
print("- artifact_zoom_q10.png")
print("- jpeg_psnr_curve.png")
