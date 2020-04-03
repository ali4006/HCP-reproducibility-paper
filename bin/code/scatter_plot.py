import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clss
import matplotlib.cm as cm
from sklearn.preprocessing import normalize
import csv
import os
import seaborn as sns
import pandas as pd


def csv_reader(csv_file):
    # open csv file
    with open(csv_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # included_cols = [22, 26]
        freq_ = {}
        subjects = {}
        i = 0
        for row in reader:
            if i == 0:
                i = i+1
                continue
            subjects[int(row[26])] = [float(i) for i in row[1:21]]
            freq_[int(row[26])] = float(row[22])
    return freq_, subjects


def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)


def main():
    parser = argparse.ArgumentParser(description="Scatter plots of Dice \
                                     coefficients and region sizes.")
    parser.add_argument("csv_file",
                        help='Input CSV file')
    parser.add_argument("output",
                        help='Output folder')

    args = parser.parse_args()
    csv_file = args.csv_file
    fig = plt.figure(figsize=(15, 15))
    fig2 = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)
    ax2 = fig2.add_subplot(111)
    # ax3 = fig.add_subplot(223)
    # ax4 = fig.add_subplot(224)

    data2 = pd.read_csv(csv_file)  # load data set
    data2.pop('Background')
    # col, row = data2.shape
    # cmap = get_cmap(12)
    data3 = pd.DataFrame(data2)
    data2 = data3.sort_values(by=5, ascending=False, axis=1)
    markers = ['o', 'v', '*', 'P']
    markers2 = ['s', 'X', '>', '1']
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    # [(a,b) for a,b in zip(markers, colors)]
    groups = [(k, j) for j in markers for k in colors]
    groups2 = [(k, j) for j in markers2 for k in colors]
    i = 1
    j = 1
    # x2 = data2['2.0'][1::2]
    for label_ in data2.columns:
        list_ = data2[label_]
        x, y = list_[1::2], np.round(list_[::2], 5)
        # out = np.polyfit(x, y, 2)
        if int(sum(x)/len(x)) < 10000:
            ax1.scatter(x, y, c=groups[i][0], label=label_,
                        marker=groups[i][1])
            ax1.legend(loc='bottom right', fontsize=14)
            ax1.set_xlabel('Region Size (voxels)', fontsize=22)
            ax1.set_ylabel('Dice Coefficients', fontsize=22)
            ax1.tick_params(labelsize=14)
            i = i + 1
        else:
            ax2.scatter(x, y, c=groups2[j][0], label=label_,
                        marker=groups2[j][1])
            ax2.legend(loc='bottom right', fontsize=14)
            ax2.set_xlabel('Region Size (voxels)', fontsize=22)
            ax2.set_ylabel('Dice Coefficients', fontsize=22)
            ax2.tick_params(labelsize=14)
            j = j + 1

    base, ext = os.path.splitext(args.output)
    fig.savefig("{}_1{}".format(base, ext), bbox_inches='tight')
    fig2.savefig("{}_2{}".format(base, ext), bbox_inches='tight')
    # plt.show()


if __name__ == '__main__':
    main()
