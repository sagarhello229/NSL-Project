import os
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ========== 1. FOLDER-BASED DATASET ==========
def check_folder_label_distribution(dataset_path):
    print("\n=== Folder-Based Dataset Label Counts ===")
    for class_name in os.listdir(dataset_path):
        class_dir = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_dir):
            count = len(os.listdir(class_dir))
            print(f"Class '{class_name}': {count} images")

# ========== 2. LABELS AS PYTHON LIST ==========
def check_list_label_distribution(labels):
    print("\n=== List-Based Labels Count ===")
    counter = Counter(labels)
    for label, count in counter.items():
        print(f"Label '{label}': {count} samples")

    # Optional: Plot
    plt.bar(counter.keys(), counter.values())
    plt.title("Label Distribution (List)")
    plt.xlabel("Class Labels")
    plt.ylabel("Number of Samples")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ========== 3. LABELS FROM CSV USING PANDAS ==========
def check_csv_label_distribution(csv_file, label_column):
    print("\n=== CSV-Based Labels Count ===")
    df = pd.read_csv(csv_file)
    print(df[label_column].value_counts())

    # Optional: Plot
    df[label_column].value_counts().plot(kind='bar')
    plt.title("Label Distribution (CSV)")
    plt.xlabel("Class Labels")
    plt.ylabel("Number of Samples")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ========== 4. ONE-HOT ENCODED LABELS ==========
def check_one_hot_label_distribution(y_onehot):
    print("\n=== One-Hot Encoded Labels Count ===")
    counts = np.sum(y_onehot, axis=0)
    for i, count in enumerate(counts):
        print(f"Class {i}: {int(count)} samples")

    # Optional: Plot
    plt.bar(range(len(counts)), counts)
    plt.title("Label Distribution (One-hot)")
    plt.xlabel("Class Index")
    plt.ylabel("Number of Samples")
    plt.tight_layout()
    plt.show()

# =====================
# ✅ MAIN ENTRY POINT
# =====================
if __name__ == "__main__":
    # === 1. Folder-based dataset ===
    check_folder_label_distribution('/home/sagar/Code/project-3/nsl_dataset/split_dataset/train')

    # === 2. Label list ===
    # labels = ['प', 'श', 'ढ', 'प', 'प', 'श', 'ट', 'ज्ञ', 'झ', 'च']
    # check_list_label_distribution(labels)

    # === 3. CSV based ===
    # check_csv_label_distribution('your_file.csv', 'label')

    # === 4. One-hot encoded ===
    # y_onehot = np.array([[0,1,0], [1,0,0], [0,1,0]])
    # check_one_hot_label_distribution(y_onehot)