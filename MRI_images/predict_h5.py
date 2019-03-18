import os

import nibabel as nib
import numpy as np
from unet3d.prediction import predict, patch_wise_prediction, prediction_to_image


def run_validation_case(data_index, output_dir, model, data_file, training_modalities,
                        output_label_map=False, threshold=0.5, labels=None, overlap=16, permute=False):
    """
    Runs a test case and writes predicted images to file.
    :param data_index: Index from of the list of test cases to get an image prediction from.
    :param output_dir: Where to write prediction images.
    :param output_label_map: If True, will write out a single image with one or more labels. Otherwise outputs
    the (sigmoid) prediction values from the model.
    :param threshold: If output_label_map is set to True, this threshold defines the value above which is
    considered a positive result and will be assigned a label.
    :param labels:
    :param training_modalities:
    :param data_file:
    :param model:
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    affine = data_file.root.affine[data_index]
    test_data = np.asarray([data_file.root.data[data_index]])
    for i, modality in enumerate(training_modalities):
        image = nib.Nifti1Image(test_data[0, i], affine)
        image.to_filename(os.path.join(output_dir, f"data_{data_index}_{modality}.nii.gz"))

    patch_shape = tuple([int(dim) for dim in model.input.shape[-3:]])
    if patch_shape == test_data.shape[-3:]:
        prediction = predict(model, test_data, permute=permute)
    else:
        prediction = patch_wise_prediction(model=model, data=test_data, overlap=overlap, permute=permute)[np.newaxis]
    prediction_image = prediction_to_image(prediction, affine, label_map=output_label_map, threshold=threshold,
                                           labels=labels)
    if isinstance(prediction_image, list):
        for i, image in enumerate(prediction_image):
            image.to_filename(os.path.join(output_dir, f"prediction_{data_index}_{i + 1}.nii.gz"))
    else:
        prediction_image.to_filename(os.path.join(output_dir, "prediction.nii.gz"))
    return prediction