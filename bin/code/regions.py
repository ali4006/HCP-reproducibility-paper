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


palette_colors = [ "#000000", "#00FF00", "#0000FF", "#FF0000", "#01FFFE", "#FFA6FE", "#FFDB66", "#006401", "#010067", "#95003A", "#007DB5", "#FF00F6", "#FFEEE8", "#774D00", "#90FB92", "#0076FF", "#D5FF00", "#FF937E", "#6A826C", "#FF029D", "#FE8900", "#7A4782", "#7E2DD2", "#85A900", "#FF0056", "#A42400", "#00AE7E", "#683D3B", "#BDC6FF", "#263400", "#BDD393", "#00B917", "#9E008E", "#001544", "#C28C9F", "#FF74A3", "#01D0FF", "#004754", "#E56FFE", "#788231", "#0E4CA1", "#91D0CB", "#BE9970", "#968AE8", "#BB8800", "#43002C", "#DEFF74", "#00FFC6", "#FFE502",
                   "#620E00", "#008F9C", "#98FF52", "#7544B1", "#B500FF", "#00FF78", "#FF6E41", "#005F39", "#6B6882", "#5FAD4E", "#A75740", "#A5FFD2" ]


# pick a color or left/right region
colors={}
nc = 0
for i, region in enumerate(regions):
    c = region.replace('Left', '').replace('Right', '')
    if colors.get(c) is None:
        colors[c] = palette_colors[nc]
        nc = nc + 1
    colors[region] = colors[c]

prefixes = [ 'left', 'right', 'inf', 'lat', 'lateral', '3rd', '4th', 'non' ]

markers = [ 's', 'h', 'P', 'D', 'd', 'x', '+', 'p', ]
def sort_func(x):
    x = x.lower()
    def prefixed(s):
        for x in prefixes:
            if s.startswith(x):
                return True
        return False
    while(prefixed(x)):
        s = x.split(' ')
        x = ' '.join(s[1:])
    return x

for region in sorted(regions, key=sort_func):
    if region == 'Background':
        continue
    marker = markers[abs(hash(region) % len(markers))]
    if region.lower().startswith('cc'):
        marker = '$\cap$'
    if region == 'Brain Stem':
        marker = 3
    if 'ventricle' in region.lower():
        marker = 'o'
    if region == 'Optic Chiasm':
        marker = '2'
    if region == 'CSF':
        marker = '*'
    if 'hypointensities' in region:
        marker = '.'
    if 'left' in region.lower():
        marker = 4
    if 'right' in region.lower():
        marker = 5
    plt.scatter(sizes[region], dices[region],
                color=colors[region],
                marker=marker,
                label=region)

plt.xscale('log')
plt.ylabel('Dice coefficient')
plt.xlabel('Region size in voxels (log)')
plt.legend(fontsize=10)
plt.savefig('images/dice_regions.pdf')