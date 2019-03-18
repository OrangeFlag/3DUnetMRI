import tables
import predict_h5
from unet3d.training import load_old_model

model = load_old_model('tumor_segmentation_model.h5')
data_file = tables.open_file('data/h5/ozerki.h5', "r")

predict_h5.run_validation_case(0, 'data/out', model, data_file, ["t1", "t1ce", "flair", "t2"])
