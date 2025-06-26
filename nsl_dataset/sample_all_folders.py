import os
import random
import shutil

def undersample_dataset(dataset_path):
    class_counts = {}
    
    # Step 1: Count images per class
    for class_name in os.listdir(dataset_path):
        class_dir = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_dir):
            count = len(os.listdir(class_dir))
            class_counts[class_name] = count

    # Step 2: Find minimum count
    min_count = min(class_counts.values())
    print(f"\nMinimum images in any class: {min_count}")

    # Step 3: For each class, if more than min, remove extra images
    for class_name, count in class_counts.items():
        class_dir = os.path.join(dataset_path, class_name)
        images = os.listdir(class_dir)

        if count > min_count:
            extra = count - min_count
            print(f"Class '{class_name}' has {count}, removing {extra} images.")
            random.shuffle(images)
            images_to_remove = images[:extra]

            for img in images_to_remove:
                os.remove(os.path.join(class_dir, img))
        else:
            print(f"Class '{class_name}' already has {count}, no change.")

    print("\n✅ Dataset undersampling complete!")

# 🔽 Example usage:
undersample_dataset('/home/sagar/Code/project-3/nsl_dataset/split_dataset/train')
