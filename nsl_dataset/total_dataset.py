import os

def count_total_images(data_dir='split_dataset'):
    total_images = 0
    for root, dirs, files in os.walk(data_dir):
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        total_images += len(image_files)
    return total_images

total = count_total_images()
print(f"Total images in dataset (train + val + test): {total}")
