import re
from random import random

import nibabel as nib
import os
import numpy as np
from partitioning import part

part = part.Part(part.LBPA40)


def filled(image):
    input_array = np.asarray(image.dataobj)
    mask = np.zeros(input_array.shape, dtype=int)
    scope = np.asarray(image.shape)
    naming = {}
    coordinates = {}
    counter = 1
    queue = [np.asarray((0, 0, 0,))]

    # steps = []
    # for number_1 in [-1, 0, +1]:
    #     for number_2 in [-1, 0, +1]:
    #         for number_3 in [-1, 0, +1]:
    #             if number_1 == number_2 == number_3 == 0:
    #                 continue
    #             steps.append(np.asarray((number_1, number_2, number_3,)))

    steps = [np.asarray((0, 0, -1,)), np.asarray((0, 0, +1,)), np.asarray((0, -1, 0,)), np.asarray((0, +1, 0,)),
             np.asarray((-1, 0, 0,)), np.asarray((+1, 0, 0,))]
    count = 0
    try:

        while len(queue) != 0:
            el = queue.pop()
            mask[el[0], el[1], el[2]] = counter
            name_of_part = part.get_name_of_part((el[0], el[1], el[2]), image)
            # name_of_part = 'Nothing'
            if counter not in naming:
                naming[counter] = {name_of_part}
            for step in steps:
                future_el = el + step
                if (future_el >= 0).all() and (future_el < scope).all() and mask[
                    future_el[0], future_el[1], future_el[2]] == 0:
                    mask[future_el[0], future_el[1], future_el[2]] = -1
                    count += 1
                    if input_array[future_el[0], future_el[1], future_el[2]] < 0.1:
                        queue.append(future_el)

        while True:
            first = True
            while len(queue) != 0:
                el = queue.pop()
                mask[el[0], el[1], el[2]] = counter
                if first or random() < 0.2:
                    if counter in coordinates:
                        coordinates[counter].append(el)
                    else:
                        coordinates[counter] = [el]
                for step in steps:
                    future_el = el + step
                    if (future_el >= 0).all() and (future_el < scope).all() and mask[
                        future_el[0], future_el[1], future_el[2]] == 0:
                        mask[future_el[0], future_el[1], future_el[2]] = -1
                        count += 1
                        if input_array[future_el[0], future_el[1], future_el[2]] >= 0.1:
                            queue.append(future_el)
                if first and len(queue) == 0:
                    counter -= 1
                first = False
            # print(count, counter)

            index = np.where(mask == 0)
            if len(index) == 0 or index[0].size == 0:
                break
            queue.append(np.transpose(index)[0])
            counter += 1

        for counter, value in coordinates.items():
            for el in value:
                name_of_part = part.get_name_of_part((el[0], el[1], el[2]), image)
                if counter not in naming:
                    naming[counter] = {name_of_part}
                else:
                    naming[counter].add(name_of_part)


    except Exception as e:
        print(e)
    return naming, coordinates, mask


def list_images(root_path='./', subpath=r'.*\.nii.gz'):
    subpath = os.path.normpath(subpath)
    list_images_cache = []
    for path_, subdirs, files in os.walk(root_path):
        for name in files:
            rel_name = os.path.relpath(os.path.join(path_, name), root_path)
            if re.match(subpath, rel_name):
                list_images_cache.append(rel_name)

    return list_images_cache


if __name__ == "__main__":
    for name in list_images(root_path="data/out", subpath=r'.*prediction.*1\.nii.gz'):
        print(name)
        image = nib.load(os.path.join("out", name))
        # average, out = average_brightness(image)
        # print(average)
        # slice_viewer.choose_dimension(0)
        # slice_viewer.multi_slice_viewer(out)
        naming, coordinates, mask = filled(image)
        print(naming)
        print(coordinates)
        # slice_viewer.multi_slice_viewer(mask)
        img = nib.Nifti1Image(mask, image.affine)
        nib.save(img, "Map_" + name)
