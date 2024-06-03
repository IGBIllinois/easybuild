install.packages("BiocManager")
x <- setdiff(dir(path = "/home/apps/software/R/4.3.2-IGB-gcc-8.2.0/lib64/R/library"), dir(path = "/home/apps/software/R/4.4.0-IGB-gcc-8.2.0/lib64/R/library"))
BiocManager::install(x)

