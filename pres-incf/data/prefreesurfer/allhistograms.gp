#!/usr/bin/env gnuplot

set key off

# Common properties
set term png
bin_width = 0.01;
set xlabel "NRMSE"
set ylabel "No. of Files"
set yrange [0:200]
set xrange [0:.2]
# Each bar is half the (visual) width of its x-range.
set boxwidth 0.01
set style fill solid 1 border rgb 'grey30'
bin_number(x) = floor(x/bin_width)
rounded(x) = bin_width * ( bin_number(x) + 0.05 )
minx=0

# acpc
set output "acpc.png"
set title "ACPC"
plot 'acpca.dat' using (rounded($1)):(1) smooth frequency with boxes


# atlas reg
set output "atlasreg.png"
set title "Atlas Registration"
plot 'atlasreg.dat' using (rounded($1)):(1) smooth frequency with boxes

# biasfield
set output "biasfield.png"
set title "Bias Field Correction"
plot 'biasfield.dat' using (rounded($1)):(1) smooth frequency with boxes

# brainextract
set output "brainextract.png"
set title "Brain Extraction"
plot 'brainextract.dat' using (rounded($1)):(1) smooth frequency with boxes

# distortion
set output "distortion.png"
set title "Distortion Correct and Registration"
plot 'distortion.dat' using (rounded($1)):(1) smooth frequency with boxes

# prefreesurfer
set output "prefreesurfer.png"
set title "Prefreesurfer"
plot 'prefreesurfer.dat' using (rounded($1)):(1) smooth frequency with boxes
