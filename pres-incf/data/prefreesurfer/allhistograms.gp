#!/usr/bin/env gnuplot

set key off

# Common properties
set term svg
bin_width = 0.01;
set xlabel "NRMSE" font ",20"
set ylabel "No. of Files" font ",20"
set tics font ", 15"
set yrange [0:200]
set xrange [0:.2]
# Each bar is half the (visual) width of its x-range.
set boxwidth 0.01
set style fill solid 1 border rgb 'grey30'
bin_number(x) = floor(x/bin_width)
rounded(x) = bin_width * ( bin_number(x) + 0.05 )
minx=0

# acpc
set output "acpc.svg"
set title "ACPC" font ", 30"
plot 'acpca.dat' using (rounded($1)):(1) smooth frequency with boxes


# atlas reg
set output "atlasreg.svg"
set title "Atlas Registration" font ", 30"
plot 'atlasreg.dat' using (rounded($1)):(1) smooth frequency with boxes

# biasfield
set output "biasfield.svg"
set title "Bias Field Correction" font ", 30"
plot 'biasfield.dat' using (rounded($1)):(1) smooth frequency with boxes

# brainextract
set output "brainextract.svg"
set title "Brain Extraction" font ", 30"
plot 'brainextract.dat' using (rounded($1)):(1) smooth frequency with boxes

# distortion
set output "distortion.svg"
set title "Distortion Correct and Registration" font ", 30"
plot 'distortion.dat' using (rounded($1)):(1) smooth frequency with boxes

# prefreesurfer
set output "prefreesurfer.svg"
set title "Prefreesurfer" font ", 30"
plot 'prefreesurfer.dat' using (rounded($1)):(1) smooth frequency with boxes
