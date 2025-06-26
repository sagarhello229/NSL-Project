# misclassified image ko classes haru analyze garne
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# ======== Sample Data Placeholder ============
# NOTE: Replace these with your actual data
# Suppose label_encoder is already fitted and gives class names
# Replace below 3 lines with your actual data

# y_test_enc = [...]        # Actual encoded labels
# y_pred = [...]            # Predicted encoded labels
# label_encoder.classes_ = [...]  # Class names (e.g., ['प', 'च', 'श', ...])

# For demo only — replace in your code
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(['प', 'च', 'श'])
y_test_enc = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
y_pred =     np.array([0, 2, 1, 0, 1, 2, 2, 1, 0])
# =============================================

# Generate confusion matrix
cm = confusion_matrix(y_test_enc, y_pred)

# Show heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix")
plt.show()

# Extract misclassified pairs
misclassified = []
for i in range(len(cm)):
    for j in range(len(cm)):
        if i != j and cm[i][j] > 0:
            misclassified.append({
                "Actual": label_encoder.classes_[i],
                "Predicted": label_encoder.classes_[j],
                "Count": cm[i][j]
            })

# Show misclassified table
df = pd.DataFrame(misclassified)
print("\n🔍 Misclassified Pairs:")
print(df if not df.empty else "✅ No misclassifications found!")
