import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataset_dir = os.getcwd() + "\dataset1\drone_dataset\sig_1M_dataset"

df = pd.read_csv(dataset_dir + "\dataset.csv")
threshold = 75
ctr = 0
not_exist = 0
relabel = True
new_df_path = dataset_dir + "\_filtered_dataset_" + "threshold_" + str(threshold) + ".csv"
new_df = pd.DataFrame(columns=df.columns)
first_class = 0
second_class = 0
for index, row in df.iterrows():
    i = row['fragment_name']
    j = row['label']
    filename = dataset_dir + "/" + i
    if not (os.path.exists(filename)):
        # file not exist
        print("id: " + str(id))
        print("filename: " + filename)
        print("file does not exist!")
        not_exist += 1
    else:
        with open(dataset_dir + '/'+i, 'rb') as fl:
            sig = np.frombuffer(fl.read(), dtype=np.float32)
        max = np.max(sig)
        if(max < threshold and j == 1):
            print("label is: " + str(j))
            print("max is: " + str(max))
            print("fragment name is: " + i)
            # plt.plot(sig)
            # plt.show()
            ctr += 1
            if relabel:
                row["label"] = 0
                new_df = pd.concat([new_df, row])
        if row["label"] == 0:
            first_class += 1
        elif row["label"] == 1:
            second_class += 1


if relabel:
    new_df.to_csv(new_df_path)
    print("new dataset file: " + new_df_path)
print("amount of first class: " + str(first_class))
print("amount of second class: " + str(second_class))

print("not exist: " + str(not_exist))
print("bad fragments: " + str(ctr))