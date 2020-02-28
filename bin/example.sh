#!/usr/bin/env bash

if [ $# != 1 ]
then
    echo "usage: $0 <input_image.nii.gz>"
    exit 1
fi

# Parse argument, set output file names
input_image=$1
base_name=$(basename ${input_image} .nii.gz)
bet_output="${base_name}_brain.nii.gz"
bet_output_binarized="${base_name}_brain_bin.nii.gz"

# Run FSL bet, put result in ${bet_output}
bet ${input_image} ${bet_output}
echo "Voxels / volume in brain mask:"
fslstats ${bet_output} -V

# Create binary mask
fslmaths ${bet_output} -bin ${bet_output_binarized}
echo "Voxels / volume in binarized brain mask:"
fslstats ${bet_output_binarized} -V

# Remove temporary file
\rm ${bet_output}
