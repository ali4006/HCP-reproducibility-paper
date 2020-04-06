from matplotlib import pyplot as plt
import matplotlib._color_data as mcd
import random


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
plt.boxplot(data, showfliers=False,
            labels = range(len(sorted_regions)))
plt.gca().xaxis.grid(True)

for i, region in enumerate(sorted_regions):
    plt.scatter( [i+1 for x in dices[region]], dices[region],
                 s=30,
                 #c=colors[region], 
                 label=f'{i} - {region}',
                 marker='.')

plt.yticks([i/10 for i in range(11)])
# plt.ylim(0,1.1)
plt.ylabel('Dice coefficient')
plt.xlabel('Region')
plt.legend(fontsize=10)
plt.savefig('images/dice_regions.pdf')