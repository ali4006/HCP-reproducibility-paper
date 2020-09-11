#!/usr/bin/env python

import argparse
import logging
import nibabel
import sys
import os
import numpy as np
import numpy.ma as ma
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl


def log_error(message):
    logging.error(message)
    sys.exit(1)


def main():
    input_imgs = 'data/fs-20sbj-output/in_bin_img/'
    output_image_file = 'figures/brain_segmentation_mni.png'
    ref_image_file = 'data/fs-20sbj-output/mni_reference.nii'

    # Load images using nibabel
    img_sum = ''
    for img in os.listdir(input_imgs):
        if os.path.splitext(os.path.basename(img))[1] in ['.nii', '.gz']:
            img1 = nibabel.load(os.path.join(input_imgs, img))
            data1 = img1.get_data()
            if img_sum == '':
                img_sum = data1
                continue
            img_sum = img_sum + data1
    im_ref = nibabel.load(ref_image_file)
    im_data_ref = im_ref.get_data()

    # Check that both images have the same dimensions
    # shape1 = im1.header.get_data_shape()
    # shape2 = im_ref.header.get_data_shape()
    hor_view = img_sum[129,:,:]
    hor_view_ref = im_data_ref[98,:,:]
    ver_view = img_sum[:,155,:]
    ver_view_ref = im_data_ref[:,116,:]
    axi_view = img_sum[:,:,130]
    axi_view_ref = im_data_ref[:,:,94]

    # Heatmap plots
    startcolor = '#990033'
    midcolor = '#ffff00'
    endcolor = '#FFFFFF'
    own_cmap1 = mpl.colors.LinearSegmentedColormap.from_list(
                    'own2', [startcolor, midcolor, endcolor])
    fig = plt.figure(figsize=(25,10), facecolor='white')
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    plt.subplots_adjust(hspace=0.05, wspace=0.005)
    cbar_ax = fig.add_axes([.91, .18, .03, .65])
    cbar_ax.tick_params(labelsize=28, color='black', labelcolor='black')
    cbar_ax.yaxis.label.set_size(32)
    cbar_ax.yaxis.label.set_color('black')

    own_cmap1.set_under("0.5", alpha=0)
    hmax= sns.heatmap(np.rot90(ver_view), cbar_ax=cbar_ax, cmap=own_cmap1, xticklabels='',
                      yticklabels='', cbar_kws={'label': 'Number of subjects'}, ax=ax3, vmin=1, vmax=7)
    hmax.imshow(np.rot90(ver_view_ref), cmap='gray', aspect='equal', extent=hmax.get_xlim() + hmax.get_ylim())

    hmax2 = sns.heatmap(np.rot90(hor_view), cmap=own_cmap1, xticklabels='', yticklabels='', cbar=False, ax=ax2, vmin=1, vmax=8)
    hmax2.imshow(np.rot90(hor_view_ref), cmap='gray', aspect='equal', extent=hmax2.get_xlim() + hmax2.get_ylim())

    hmax3 = sns.heatmap(np.rot90(axi_view), cmap=own_cmap1, xticklabels='', yticklabels='', cbar=False, ax=ax1, vmin=1, vmax=8)
    hmax3.imshow(np.rot90(axi_view_ref), cmap='gray', aspect='equal', extent=hmax3.get_xlim() + hmax3.get_ylim())
    plt.rcParams['axes.facecolor'] = 'black'
    plt.savefig(output_image_file, facecolor=fig.get_facecolor(), bbox_inches='tight')
    # plt.show()

if __name__ == '__main__':
    main()
