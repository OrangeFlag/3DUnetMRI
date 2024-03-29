import os
import nibabel as nib
from nibabel.affines import apply_affine
import numpy as np


class Template:
    def __init__(self, template_file_name: str = None, get_name_by_color=None, meta=None):
        self.template_file_name = template_file_name
        self.get_name_by_color = get_name_by_color
        self.meta = meta


class Part:
    def __init__(self, template: Template):
        self.template = nib.load(os.path.abspath(template.template_file_name))
        self.get_name_by_color = template.get_name_by_color

    def get_name_of_part(self, voxel_coord: (int, int, int), image):
        template = self.template
        affine_image_coord = apply_affine(image.affine, voxel_coord)
        voxel_template_coord = apply_affine(np.linalg.inv(template.affine), affine_image_coord)
        if (voxel_template_coord < np.asarray((0, 0, 0,))).any() or (
                voxel_template_coord > np.asarray(template.shape)).any():
            return "You have reached the edge of the world. Next live dragons."
        return self.get_name_by_color(
            template.dataobj[int(voxel_template_coord[0]), int(voxel_template_coord[1]), int(voxel_template_coord[2])])


LBPA40_mas = ["You have reached the edge of the world. Next live dragons.",
              "L_insular_cortex",
              "R_insular_cortex",
              "L_cingulate_gyrus",
              "R_cingulate_gyrus",
              "L_caudate",
              "R_caudate",
              "L_putamen",
              "R_putamen",
              "L_hippocampus",
              "R_hippocampus",
              "cerebellum",
              "brainstem",
              "L_superior_frontal_gyrus"
              "R_superior_frontal_gyrus",
              "L_middle_frontal_gyrus",
              "R_middle_frontal_gyrus",
              "L_inferior_frontal_gyrus",
              "R_inferior_frontal_gyrus",
              "L_precentral_gyrus",
              "R_precentral_gyrus",
              "L_middle_orbitofrontal_gyrus"
              "R_middle_orbitofrontal_gyrus",
              "L_lateral_orbitofrontal_gyrus",
              "R_lateral_orbitofrontal_gyrus",
              "L_gyrus_rectus",
              "R_gyrus_rectus"
              "L_postcentral_gyrus",
              "R_postcentral_gyrus"
              "L_superior_parietal_gyrus",
              "R_superior_parietal_gyrus",
              "L_supramarginal_gyrus",
              "R_supramarginal_gyrus",
              "L_angular_gyrus",
              "R_angular_gyrus",
              "L_precuneus",
              "R_precuneus",
              "L_superior_occipital_gyrus",
              "R_superior_occipital_gyrus",
              "L_middle_occipital_gyrus",
              "R_middle_occipital_gyrus",
              "L_inferior_occipital_gyrus",
              "R_inferior_occipital_gyrus",
              "L_cuneus",
              "R_cuneus",
              "L_superior_temporal_gyrus",
              "R_superior_temporal_gyrus",
              "L_middle_temporal_gyrus",
              "R_middle_temporal_gyrus",
              "L_inferior_temporal_gyrus",
              "R_inferior_temporal_gyrus",
              "L_parahippocampal_gyrus",
              "R_parahippocampal_gyrus",
              "L_lingual_gyrus",
              "R_lingual_gyrus",
              "L_fusiform_gyrus",
              "R_fusiform_gyrus"
              ]


def LBPA40_get_name_by_color(color):
    color = int(color)
    assert 0 <= color < 58
    return LBPA40_mas[color]


LBPA40 = Template("LBPA40.nii.gz", LBPA40_get_name_by_color,
                  {"url": "https://scalablebrainatlas.incf.org/main/coronal3d.php?template=LPBA40_on_SRI24"})
