import os
import shutil

# Source folders
base_dir = 'dataset'
sources = ['plain_background_data', 'random_background_data']
#combine folders
combined_dir = 'combined_dataset'

# Get class names from one of the source folders (plain_background)
class_dir = os.path.join(base_dir, sources[0])
classes = [d for d in os.listdir(class_dir) if os.path.isdir(os.path.join(class_dir, d))]

# Create combined folders
os.makedirs(combined_dir, exist_ok=True)
for cls in classes:
    target_cls_path = os.path.join(combined_dir, cls)
    os.makedirs(target_cls_path, exist_ok=True)

    for src in sources:
        source_path = os.path.join(base_dir, src, cls)
        if os.path.exists(source_path):
            for filename in os.listdir(source_path):
                src_file = os.path.join(source_path, filename)
                dst_file = os.path.join(target_cls_path, f"{src}_{filename}")
                shutil.copy(src_file, dst_file)
            print(f" Copied from {source_path}")
        else:
            print(f" Not found: {source_path}")
