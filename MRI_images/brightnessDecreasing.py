from multiprocessing import Pool
import os
import numpy as np
import SimpleITK as sitk


def decrease(imageArr, strength):
    print(imageArr.shape)
    (amount, height, width) = imageArr.shape
    print(amount, height, width)
    toDecrease = np.ones((height, width))
    for k in range(1, amount):
        for i in range(1, height):
            for j in range(1, width):
                imageArr[k][i][j] -= strength
                if imageArr[k][i][j] < 0:
                    imageArr[k][i][j] = 0
    return imageArr



def test():
    reader = sitk.ImageFileReader()
    reader.SetImageIO("NiftiImageIO")
    reader.SetFileName("G2.nii.gz") #name of image
    image = reader.Execute();

    imageArr= sitk.GetArrayFromImage(image)
    imageArr = decrease(imageArr)
    result = sitk.GetImageFromArray(imageArr)
    sitk.WriteImage(result, 'resultDecreased.nii.gz', True)#name of result