#!/usr/bin/env bash

if [ $# != 1 ]
then
    echo "usage: $0 <input_image.nii.gz>"
    exit 1
fi

input_image=$1
bet_output="$(basename ${input_image} .nii.gz)_brain.nii.gz"
bet_output_binarized="$(basename ${input_image} .nii.gz)_brain_bin.nii.gz"

bet ${input_image} ${bet_output}
echo "Voxels / volume in brain mask:"
fslstats ${bet_output} -V
fslmaths ${bet_output} ${bet_output_binarized}
echo "Voxels / volume in binarized brain mask:"
fslstats ${bet_output_binarized} -V
\rm ${bet_output}
