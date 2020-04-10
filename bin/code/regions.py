from matplotlib import pyplot as plt
import matplotlib._color_data as mcd
import random

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(15,15))

with open('./data/fs_seg_dice_accumulated_20sbj.csv') as f:
    lines = f.readlines()


dices = {}
sizes = {}
for i, line in enumerate(lines):
    if i == 0:
        regions = line.split(',')
        regions = [ x.replace('-', ' ').replace('_', ' ').replace('\n', '') for x in regions]
        continue
    if i % 2 == 0:
        pointer = sizes 
    else:
        pointer = dices
    vals = [float(x) for x in line.split(',')]
    for j, val in enumerate(vals):
        region = regions[j]
        if pointer.get(region) is None:
            pointer[region] = []
        pointer[region] += [ val ]

# Sort regions by median dice
from statistics import mean, median
sorted_regions = sorted(regions, key=lambda x: median(dices[x]))

data = [ dices[region] for region in sorted_regions ]
mean_sizes = [ [ mean(sizes[region]) for x in sizes[region]] for region in sorted_regions ]

from math import log
bplot = plt.boxplot(data, showfliers=False, patch_artist=True,
            labels = range(len(sorted_regions)))

#print(bplot)
# fill with colors
for i, patch in enumerate(bplot['boxes']):
    region = sorted_regions[i]
    rs = mean(sizes[region])
    bs = mean(sizes['Background'])
    a = log(rs)/log(bs)
    patch.set_facecolor((0, 0, 0, a))

for i, region in enumerate(sorted_regions):
    plt.scatter( [i+1 for x in dices[region]], dices[region],
                 s=35,
                 color='black',
                 label=f'{i} - {region}',
                 marker='.')

plt.yticks([i/10 for i in range(11)])
# plt.ylim(0,1.1)
plt.ylabel('Dice coefficient')
plt.xlabel('Region')
plt.legend(handlelength=0, handletextpad=0, 
           fontsize=14,
           bbox_to_anchor=(0.98, 0),
           loc="lower right",
           bbox_transform=plt.gcf().transFigure,
           ncol=4)
plt.subplots_adjust(bottom=0.25)
leg = plt.gca().get_legend()
for i in range(len(sorted_regions)):
    leg.legendHandles[i].set_visible(False)
plt.gca().xaxis.tick_top()
plt.gca().xaxis.set_ticks_position('top')
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.grid(True, alpha=0.3)

import matplotlib.ticker as plticker
#locs, labels = plt.xticks()
import numpy as np
plt.xticks(np.arange(1, 45, step=4), labels=np.arange(1, 45, step=4)-1)
yticks = [0.1, 0.3, 0.5, 0.7, 0.9]
plt.yticks(yticks, labels=yticks)


plt.savefig('figures/dice_regions.pdf')