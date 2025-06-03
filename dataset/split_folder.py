import os
import shutil
import random

def split_dataset(source_dir, target_dir, train_ratio=0.7):
    classes = os.listdir(source_dir)

    for class_name in classes:
        class_path = os.path.join(source_dir, class_name)
        if not os.path.isdir(class_path):
            continue

        images = os.listdir(class_path)
        random.shuffle(images)

        train_count = int(len(images) * train_ratio)

        train_class_dir = os.path.join(target_dir, 'train', class_name)
        test_class_dir = os.path.join(target_dir, 'test', class_name)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)

        for i, img in enumerate(images):
            src_path = os.path.join(class_path, img)
            if i < train_count:
                dst_path = os.path.join(train_class_dir, img)
            else:
                dst_path = os.path.join(test_class_dir, img)

            shutil.copyfile(src_path, dst_path)

split_dataset("combined_dataset", "split_dataset", train_ratio=0.7)
