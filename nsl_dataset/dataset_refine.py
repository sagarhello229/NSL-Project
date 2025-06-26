
# import os
# import hashlib
# import cv2

# def dhash(image, hashSize=8):
#     # Simple image hashing function for duplicate detection
#     import cv2
#     resized = cv2.resize(image, (hashSize + 1, hashSize))
#     diff = resized[:, 1:] > resized[:, :-1]
#     return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

# image_hashes = {}
# duplicates = []

# for root, dirs, files in os.walk('/home/sagar/Code/project-3/nsl_dataset/combined_dataset/ह'):
#     for file in files:
#         path = os.path.join(root, file)
#         img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             continue
#         h = dhash(img)
#         if h in image_hashes:
#             duplicates.append(path)
#         else:
#             image_hashes[h] = path

# print(f"Found duplicates: {duplicates}")
# print(f"Total duplicate images found: {len(duplicates)}")

# for file_path in duplicates:
#     try:
#         os.remove(file_path)
#         print(f"Deleted duplicate: {file_path}")
#     except Exception as e:
#         print(f"Error deleting {file_path}: {e}")




# from PIL import Image

# corrupted_files = []

# for filename in os.listdir('/home/sagar/Code/project-3/nsl_dataset/combined_dataset/क्ष'):
#     path = os.path.join('/home/sagar/Code/project-3/nsl_dataset/combined_dataset/क्ष', filename)
#     try:
#         img = Image.open(path)
#         img.verify()  # verify does not load full image but checks integrity
#     except (IOError, SyntaxError) as e:
#         corrupted_files.append(path)

# print("Corrupted files:", corrupted_files)
# # Remove or fix these files



# def is_blurry(image_path, threshold=100):
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         print(f"Could not read image: {image_path}")
#         return True  # Treat unreadable images as blurry
#     laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
#     return laplacian_var < threshold

# blurry_images = []

# imagePath = '/home/sagar/Code/project-3/nsl_dataset/combined_dataset/क'

# for file in os.listdir(imagePath):  
#     path = os.path.join(imagePath, file) 
#     if is_blurry(path):
#         blurry_images.append(path)

# print("Blurry images:", blurry_images)
# print(f"Total blurry images found: {len(blurry_images)}")

