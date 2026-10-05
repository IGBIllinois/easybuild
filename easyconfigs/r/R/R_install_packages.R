#!/usr/bin/env Rscript

install.packages("BiocManager")
pkgs <- readLines("packages.txt")
new_pkgs <- pkgs[!(pkgs %in% installed.packages()[,"Package"])]
if(length(new_pkgs)) install.packages(new_pkgs)

