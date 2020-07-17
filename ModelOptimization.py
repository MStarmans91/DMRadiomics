import WORC
import os
import glob
from classes import switch


def editconfig(config):
    '''
    Function to edit the WORC configuration for the DTF study.
    '''
    config['General']['Segmentix'] = 'True'

    config['PREDICTGeneral']['Joblib_ncores'] = '1'
    config['PREDICTGeneral']['Joblib_backend'] = 'threading'

    config['Normalize']['ROI'] = 'False'  # No Normalization for CT

    config['ImageFeatures']['coliage'] = 'False'
    config['ImageFeatures']['vessel'] = 'True'
    config['ImageFeatures']['phase'] = 'True'
    config['ImageFeatures']['log'] = 'True'
    config['ImageFeatures']['image_type'] = 'MR'
    config['ImageFeatures']['vessel_radius'] = '0'  # tumors can be really small

    config['Featsel']['Variance'] = 'True, False'

    config['SelectFeatGroup']['shape_features'] = 'True, False'
    config['SelectFeatGroup']['histogram_features'] = 'True, False'
    config['SelectFeatGroup']['orientation_features'] = 'True, False'
    config['SelectFeatGroup']['texture_Gabor_features'] = 'True, False'
    config['SelectFeatGroup']['texture_GLCM_features'] = 'True, False'
    config['SelectFeatGroup']['texture_GLCMMS_features'] = 'True, False'
    config['SelectFeatGroup']['texture_GLRLM_features'] = 'True, False'
    config['SelectFeatGroup']['texture_GLSZM_features'] = 'True, False'
    config['SelectFeatGroup']['texture_NGTDM_features'] = 'True, False'
    config['SelectFeatGroup']['texture_LBP_features'] = 'True, False'
    config['SelectFeatGroup']['patient_features'] = 'True, False'
    config['SelectFeatGroup']['semantic_features'] = 'True, False'
    config['SelectFeatGroup']['coliage_features'] = 'False'
    config['SelectFeatGroup']['vessel_features'] = 'True, False'
    config['SelectFeatGroup']['phase_features'] = 'True, False'
    config['SelectFeatGroup']['log_features'] = 'True, False'

    config['CrossValidation']['N_iterations'] = '100'

    config['Genetics']['label_names'] = 'DM'
    config['Genetics']['modus'] = 'singlelabel'

    config['HyperOptimization']['N_iterations'] = '100000'
    config['HyperOptimization']['n_jobspercore'] = '4000'

    config['SampleProcessing']['SMOTE'] = 'True'
    config['SampleProcessing']['Oversampling'] = 'False'

    config['Ensemble']['Use'] = 'False'

    return config


# Inputs
name = 'WORC_DM_DD'
current_path = os.path.dirname(os.path.abspath(__file__))
label_file = os.path.join(current_path, 'ExampleData', 'pinfo_DM.txt')
semantics_file = os.path.join(current_path, 'ExampleData', 'sem_DM.txt')
config = os.path.join(current_path, 'ExampleData', 'config_modeloptimization.ini')

# Altough you can also the features, we will supply the raw image
images = glob.glob(os.path.join(current_path, 'ExampleData', 'ExampleImage*.nii.gz'))
images.sort()

segmentations = glob.glob(os.path.join(current_path, 'ExampleData', 'ExampleSegmentation*.nii.gz'))
segmentations.sort()

metadatas = glob.glob(os.path.join(current_path, 'ExampleData', 'ExampleDCM*.dcm'))
metadatas.sort()

# As we only have a single patient/object, hence we will repeat it to mimick
# having multiple. We do this in a dictionary, in which the keys
# correspond to the "patient" names also used in the label and semantics files
patient_names = ['DMRadiomics-' + str(i).zfill(3) for i in range(0, 10)]
images = {k: v for k, v in zip(patient_names, images)}
segmentations = {k: v for k, v in zip(patient_names, segmentations)}
metadatas = {k: v for k, v in zip(patient_names, metadatas)}

# Create the WORC network
network = WORC.WORC(name)

# Instead of supplying the .ini file to the network, we will create
# the config object for you directly from WORC,
# so you can interact with it if you want.
# Altough it is a configparser object, it works similar as a dictionary
config = network.defaultconfig()

# The default config from the WORC 2.1.3 version we used, was a stripped
# version in order to get a quick result. The actual default used for normal
# experiments is created through the editconfig function.
config = editconfig(config)

# Set the label name you want to PREDICT: we use DM = Desmoid for now
config['Genetics']['label_names'] = 'DM'

# NOTE: Since we now only use 10 "patients" in this example, we change one setting
# Do not do this for the full experiment.
config['SampleProcessing']['SMOTE_neighbors'] = '1, 1'

# Specific additions for each model discussed in the paper
option = 'model_3_imaging'
for case in switch(option):
    if case('model_1_volume'):
        # NOTE: You will need to manual strip the feature files to only keep
        # the feature named sf_volume_2D and supply these to the network
        # instead of the images
        feature_files = glob.glob(os.path.join(current_path, 'ExampleData', 'DMRadiomics*_volume.hdf5'))
        feature_files.sort()

        # Append the sources to be used
        network.features_train.append(feature_files)
        network.labels_train.append(label_file)
        network.configs.append(config)

        break
    if case('model_2_agesex'):
        # Use only the semantic featues = age and gender
        config['SelectFeatGroup']['shape_features'] = 'False'
        config['SelectFeatGroup']['histogram_features'] = 'False'
        config['SelectFeatGroup']['orientation_features'] = 'False'
        config['SelectFeatGroup']['texture_Gabor_features'] = 'False'
        config['SelectFeatGroup']['texture_GLCM_features'] = 'False'
        config['SelectFeatGroup']['texture_GLCMMS_features'] = 'False'
        config['SelectFeatGroup']['texture_GLRLM_features'] = 'False'
        config['SelectFeatGroup']['texture_GLSZM_features'] = 'False'
        config['SelectFeatGroup']['texture_NGTDM_features'] = 'False'
        config['SelectFeatGroup']['texture_LBP_features'] = 'False'
        config['SelectFeatGroup']['patient_features'] = 'False'
        config['SelectFeatGroup']['semantic_features'] = 'True'
        config['SelectFeatGroup']['coliage_features'] = 'False'
        config['SelectFeatGroup']['vessel_features'] = 'False'
        config['SelectFeatGroup']['phase_features'] = 'False'
        config['SelectFeatGroup']['log_features'] = 'False'

        # Append the sources to be used
        network.images_train.append(images)
        network.segmentations_train.append(segmentations)
        network.metadata.train.append(metadatas)
        network.semantics_train.append(semantics_file)

        break
    if case('model_3_imaging'):
        # Set the non-imaging feature groups to False so they are not used
        config['SelectFeatGroup']['semantic_features'] = 'False'
        config['SelectFeatGroup']['patient_features'] = 'False'

        # Append the sources to be used
        network.images_train.append(images)
        network.segmentations_train.append(segmentations)
        network.metadata.train.append(metadatas)
        network.semantics_train.append(semantics_file)

        break
    if case('model_4_imagingagesex'):
        # Append the sources to be used
        network.images_train.append(images)
        network.segmentations_train.append(segmentations)
        network.metadata.train.append(metadatas)
        network.semantics_train.append(semantics_file)

        break
    if case('model_567_T2'):
        # For these models, an additional image/segmentation/metadata
        # combination per patient has to be supplied to the model, i.e.
        # the T2w non-FS, the T2w FS and T2w FS or non-FS for models 5, 6, and
        # 7, respectively. You can just do this by creating
        # a second object for both the images/segmentations/metadatas and
        # append this to the network. Here, we will just repeat the first

        # NOTE: When a sequence is missing, please supply a dummy object
        # for the image/segmentation/metadata. Make sure the image is called
        # "Dummy.nii.gz": WORC will treat this object appropriately.

        # The "T1"
        network.images_train.append(images)
        network.segmentations_train.append(segmentations)
        network.metadata.train.append(metadatas)
        network.semantics_train.append(semantics_file)

        # The "T2"
        network.images_train.append(images)
        network.segmentations_train.append(segmentations)
        network.metadata.train.append(metadatas)

        # Set the non-imaging feature groups to False so they are not used
        config['SelectFeatGroup']['semantic_features'] = 'False'
        config['SelectFeatGroup']['patient_features'] = 'False'

        # When sequences are missing, we will need to use imputation
        config['Imputation']['use'] = 'True'
        config['Imputation']['strategy'] = 'mean, median, most_frequent, constant, knn'
        config['Imputation']['n_neighbors'] = '5, 5'

        # We need to align the T2 to the T1 using registration through Elastix.
        # Here, we supply the parameter file for Elastix.
        elastix_parameters = os.path.join(current_path, 'ExampleData', 'ParametersRigidDM')
        network.Elastix_Para = [[elastix_parameters]]

        break


# Build, set, and execture the network
network.build()
network.set()
network.execute()
