import PREDICT
import os

# Configure location of input
image = os.path.join('ExampleData', 'ExampleImage.nii.gz')
segmentation = os.path.join('ExampleData', 'ExampleSegmentation.nii.gz')
metadata = os.path.join('ExampleData', 'ExampleDCM.dcm')
config = 'config_features.ini'

# Configure location of output
output = os.path.join('ExampleData', 'ExampleFeatures.hdf5')


PREDICT.CalcFeatures.CalcFeatures(image=image, segmentation=segmentation,
                                  parameters=config, metadata_file=metadata,
                                  output=output)
