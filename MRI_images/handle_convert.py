import os
import convert_to_h5

raw_data_list = []
nii_root_path = "data/original/ozerki/"
for i in range(1, 10):
    raw_data = os.path.join(nii_root_path, f"G{i}.nii.gz")
    black_stub = os.path.join(nii_root_path, "")
    raw_data_list.append((raw_data,))

convert_to_h5.write_data_to_file(raw_data_list, 'data/h5/ozerki.h5', (144, 144, 144))