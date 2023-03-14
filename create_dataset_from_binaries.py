import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# split files to dataset

source_dir = os.getcwd() + '/'# + 'drive/MyDrive/NER/'
file_names = os.listdir(source_dir)
dataset_dir = source_dir + "dataset/"
csv_filename = "dataset.csv"
fragment_tag = 'fragment_'
drone_file_name_key = 'drone'
noise_file_name_key = 'noise'
drone_class_value = 1
noise_class_value = 0
fragment_size = 8000000

if (not os.path.exists(dataset_dir)):
    print("Creating dataset dir...")
    os.makedirs(dataset_dir)

print("###############CONFIG###############")
print('dataset dir: ' + dataset_dir)
print('source dir: ' + source_dir)
print('file names: ' + str(file_names))
print('csv_filename: ' + str(csv_filename))
print("fragment_tag: " + str(fragment_tag))
print('drone_file_name_key: ' + str(drone_file_name_key))
print('noise_file_name_key: ' + str(noise_file_name_key))
print('drone_class_value: ' + str(drone_class_value))
print('noise_class_value: ' + str(noise_class_value))
print('fragment_size: ' + str(fragment_size))
print("####################################")

i = 0
fragment_names = []
labels = []
for file_name in file_names:
    try:
        with open(source_dir + file_name, 'rb') as fl:
            data = np.frombuffer(fl.read(), dtype=np.float32)
            print("####################################")
            print("file: " + file_name)
            print("file len(samples): " + str(len(data)))
            print("------------------------------------")
        print(len(data))
        batch_size = len(data) // fragment_size
        for j in range(0, batch_size):
            fragment = data[j * fragment_size:(j + 1) * fragment_size]
            fragment_name = fragment_tag + str(round(time.time() * 1000))
            fragment_names.append(fragment_name)
            with open(dataset_dir + fragment_name, "wb") as fl:
                fl.write(fragment)

            current_key = 0
            if file_name.find(drone_file_name_key) > -1:
                labels.append(drone_class_value)
                current_key = drone_class_value

            if file_name.find(noise_file_name_key) > -1:
                labels.append(noise_class_value)
                current_key = noise_class_value

            print("fragment name: " + fragment_name)
            print("fragment key: " + str(current_key))
        print("####################################")
    except Exception as e:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(str(e))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print(fragment_names)
print(labels)
df = pd.DataFrame(columns=['fragment_name', 'label'])
df['fragment_name'] = fragment_names
df['label'] = labels
df.to_csv(dataset_dir + csv_filename, sep=',', index=False)
