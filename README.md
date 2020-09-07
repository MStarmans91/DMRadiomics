# DMRadiomics
Script to compute features and fit radiomics models used in the paper "Differential diagnosis and
mutation stratification of desmoid-type fibromatosis on MRI using a radiomics approach."
M. J. M. Timbergen and M. P. A. Starmans et al. 2020.

When using this code, please cite the above mentioned paper and the code itself: [![][DOI]][DOI-lnk]

[DOI]: https://zenodo.org/badge/DOI/10.5281/zenodo.4017190.svg
[DOI-lnk]: https://zenodo.org/badge/latestdoi/214962190

## Installation
For the feature extraction, only the PREDICT package, version 2.1.3,
and the subsequent dependencies are required, which can be installed through pip:

    pip install "PREDICT==2.1.3"

For the model optimization, additionally WORC, version 2.1.3, is required:

    pip install "WORC==2.1.3"

When training or testing model 5 - 7, elastix is required to align the T2 (FS or non-FS)
to the T1. Make sure there elastix is installed on your PC and can be called on
the command line using the "elastix" command. See here for the installation
instructions: http://elastix.isi.uu.nl/

## Usage
The ExtractFeatures.py script can be used to extract all features. We provided
you with the exact same configuration file that was used in the study. The
script can be easily modified to use your own data instead of the
provided example data and requires:

1. An image in ITK Image format, e.g. .nii, .nii.gz, .tiff, .nrrd, .raw
2. A segmentation in ITK Image format.
3. Optionally, metadata in DCM format

Extracting the features from the example data should take less than 10 seconds.
Using a larger image and/or mask may result in a longer computation time.

Documentation for the model optimization is provided in the respective script.

An overview with the names / labels of all features can be found in the
feature_names.xlsx sheet. These features are also included in the example
feature file.

## Known Issues

### Pyradiomics
The PyRadiomics package we use requires numpy in the installation, hence
you may need to install numpy manually beforehand:

    pip install "numpy==1.6.2"

From version 2.2.0 and above, PyRadiomics removed a function and might throw
this error:

'''AttributeError: 'module' object has no attribute "RadiomicsFeaturesExtractor"'''

This can be overcome by downgrading to version 2.1.2:

    pip install "pyradiomics==2.1.2"

### Missingpy
Missingpy version 0.2.0 may throw an ascii error: in that case, manually
remove and reinstall the package:

    pip uninstall missingpy
    pip install "missingpy==0.2.0"


## Computation time
The computation time of an experiment depends mostly on two factors:

1. The size of the dataset in terms of patients and features. A mutation experiment conducted
  on only the DTF subset (61 patients) and only using T1-MRI (411 features)
  will take less time than a DTF vs non-DTF (203 patients) on T1- and T2-MRI (822 features).
2. The amount of workflows executed. By default, this equals
  100.000 randomly sampled workflows x 5x train-validation cross-validation x 100x train-test cross-validation
  = 50 million workflows. Reducing any of the settings and thus the amount of workflows will (almost, due to overhead) linearly decrease the computation time

Compared to the workflow optimization computation time, the feature extraction
computation time is neglectable.

For the largest setup described, we have conducted experiments on two different hardware configurations with the following computation time:

1. A CPU cluster with max. 140 jobs with one core each: 24 hours
2. A single High Performance Computing (HPC) node with 32 cores: 32 hours

While the first option has more cores available, due to the overhead of cluster scheduling, execution on a similar HPC would be faster.
Note that not all CPU power is used 100% of the time
