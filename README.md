# HCP-reproducibility-paper
A repository for the HCP reproducibility paper

## How to generate the figures

### Fig 1

To generate Figure 1, run:

```
python ./bin/code/provenance_graph.py
```

### Fig. 2

To generate Figure 2, run:

```
python ./bin/code/heatmap_plot.py
```

### Fig. 4

* [Source file](./figures/t2w_alignment.png)

### Fig. 5

To generate Figure 5, run:

```
python bin/code/binarized_heatmap_img.py
```
We already created the folder of [binarized images](data/fs-20sbj-output/in_bin_img/) between segmentation results in CetOS6 vs. CentOS7 for all subjects. You can create the binarized image for each subject using the following commands:

```
fslmaths subj1_os6.nii.gz -sub subj1_os7.nii.gz subj1_diff.nii.gz
fslmaths subj1_diff.nii.gz -bin subj1_diff_bin.nii.gz
```

### Fig. 6

To generate Figure 6, run:

```
python bin/code/regions.py
```

We already created a CSV [file](./data/fs_seg_dice_accumulated_20sbj.csv) containing all the Dice values between segmented regions for all subjects in CetOS6 vs. CentOS7. You can compute Dice values for each subject using the following command:

```
python ./bin/code/Dice_region_csv.py subj1_os6.nii.gz subj1_os7.nii.gz fs_seg_dice_accumulated_20sbj.csv
``` 

## How to generate the pdf

(You may edit ```paper.tex``` without generating the pdf if you don't manage to).

0. Install ```pdflatex``` and ```bibtex```
1. Compile the document: ```pdflatex -shell-escape paper ; pdflatex -shell-escape paper``` (yes, twice).
2. Generate the bibliography: ```bibtex paper ; pdflatex -shell-escape paper``` (yes, once again).

## License

[MIT](LICENSE) © /bin Lab
