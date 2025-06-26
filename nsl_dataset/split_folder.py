import os
import shutil
import random

def split_dataset(source_dir, dest_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=None):
    total_ratio = train_ratio + val_ratio + test_ratio
    assert abs(total_ratio - 1.0) < 1e-6, "Ratios must sum to 1"

    if seed is not None:
        random.seed(seed)

    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    for cls in classes:
        class_path = os.path.join(source_dir, cls)

        images = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
        random.shuffle(images)

        n_total = len(images)
        n_train = round(train_ratio * n_total)
        n_val = round(val_ratio * n_total)
        n_test = n_total - n_train - n_val  

        train_images = images[:n_train]
        val_images = images[n_train:n_train + n_val]
        test_images = images[n_train + n_val:]

        for category, image_list in zip(['train', 'val', 'test'], [train_images, val_images, test_images]):
            dest_class_dir = os.path.join(dest_dir, category, cls)
            os.makedirs(dest_class_dir, exist_ok=True)
            for img in image_list:
                src_img_path = os.path.join(class_path, img)
                dst_img_path = os.path.join(dest_class_dir, img)
                shutil.copy(src_img_path, dst_img_path)

split_dataset(
    source_dir='combine_dataset',
    dest_dir='split_dataset',
    train_ratio=0.7,
    val_ratio=0.15,
    test_ratio=0.15,
    seed=42
)
