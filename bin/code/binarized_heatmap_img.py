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
    parser = argparse.ArgumentParser(description="Computes a \
                                     binarized heatmap of the images.")
    parser.add_argument("input_imgs",
                        help='Input folder of binarized difference images')
    parser.add_argument("output_image_file",
                        help='output folder')
    parser.add_argument("ref_image_file",
                        help='reference image like MNI-152')

    args = parser.parse_args()
    # Load images using nibabel
    img_sum = ''
    for img in os.listdir(args.input_imgs):
        if os.path.splitext(os.path.basename(img))[1] in ['.nii', '.gz']:
            img1 = nibabel.load(os.path.join(args.input_imgs, img))
            data1 = img1.get_data()
            if img_sum == '':
                img_sum = data1
                continue
            img_sum = img_sum + data1
    im_ref = nibabel.load(args.ref_image_file)
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
    fig = plt.figure(figsize=(25,10), facecolor='black')
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    plt.subplots_adjust(hspace=0.05, wspace=0.005)
    cbar_ax = fig.add_axes([.91, .2, .02, .6])
    cbar_ax.tick_params(labelsize=26, color='white', labelcolor='white')

    own_cmap1.set_under("0.5", alpha=0)
    hmax= sns.heatmap(np.rot90(ver_view), cbar_ax=cbar_ax, cmap=own_cmap1, xticklabels='', 
                      yticklabels='', ax=ax3, vmin=1, vmax=7)
    hmax.imshow(np.rot90(ver_view_ref), cmap='gray', aspect='equal', extent=hmax.get_xlim() + hmax.get_ylim())

    hmax2 = sns.heatmap(np.rot90(hor_view), cmap=own_cmap1, xticklabels='', yticklabels='', cbar=False, ax=ax2, vmin=1, vmax=8)
    hmax2.imshow(np.rot90(hor_view_ref), cmap='gray', aspect='equal', extent=hmax2.get_xlim() + hmax2.get_ylim())

    hmax3 = sns.heatmap(np.rot90(axi_view), cmap=own_cmap1, xticklabels='', yticklabels='', cbar=False, ax=ax1, vmin=1, vmax=8)
    hmax3.imshow(np.rot90(axi_view_ref), cmap='gray', aspect='equal', extent=hmax3.get_xlim() + hmax3.get_ylim())
    plt.rcParams['axes.facecolor'] = 'black'
    plt.savefig(args.output_image_file, facecolor=fig.get_facecolor(), bbox_inches='tight')
    #plt.show()

if __name__ == '__main__':
    main()
