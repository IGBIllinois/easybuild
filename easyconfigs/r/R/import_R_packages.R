#Updating R packages on Biocluster ----

# First, load old R version to check packages:

#$ srun -p hpcbio --pty bash
#$ module load R/4.2.2-IGB-gcc-8.2.0
#$ R

#Find main library location

.libPaths()

# a user's personal library may be listed first,
# so make sure to use the main one

oldlib <- "/home/apps/software/R/4.2.2-IGB-gcc-8.2.0/lib64/R/library"

#Get list of packages installed there

oldpkgs <- dir(path = oldlib)
length(oldpkgs)


#Next, find which packages were installed from GitHub:
#From https://stackoverflow.com/questions/49698348/how-to-find-out-which-package-was-installed-from-github-in-my-r-library

isGithub <- function(pkg){
  !is.null(packageDescription(pkg)$GithubRepo)
}


result <- sapply(oldpkgs, isGithub)
sum(result)
#This is the number of github packages

df <- data.frame(package = names(result), github_or_not = result,
                 stringsAsFactors = FALSE)
head(df[df$github_or_not, ])

#Also pull out Github username:

df$username <- "none"

for (i in which(df$github_or_not)){
  df$username[i] <- packageDescription(df$package[i])$GithubUsername
}

#output the entire list to use in new R version session:

write.table(df, file = "~/oldRpackages.txt", sep = "\t")


# Quit this version of R without saving objects

q(save = "no")


#Switch to new R version

#$ module purge
#$ module load R/4.3.2-IGB-gcc-8.2.0
#$ R


#Read in old packages

df <- read.delim("~/oldRpackages.txt")


# Get main library location of new R version

.libPaths()

# a user's personal library may be listed first,
# so make sure to use the main one

newlib <- "/home/apps/software/R/4.3.2-IGB-gcc-8.2.0/lib64/R/library"



# Find the differences in installed packages

newpkgs <- dir(path = newlib)

missingpkgs <- setdiff(df$package, newpkgs)

length(missingpkgs)

# Option 1: install all packages from previous R ----

# The easiest way to install most all of the
# previously installed packages is to try to
# use BiocManager::install() on the entire
# vector of missingpkgs. However, packages that
# are deprecated from Bioconductor or CRAN, or
# packages only available from Github will
# throw warnings. You can safely ignore these
# and not worry about tracking them as we can
# re-check missing packages later. This method
# does have the benefit that if a package
# previously installed from Github but has now
# been submitted to CRAN or Bioconductor, it
# will update the installation


if (!require("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

BiocManager::install(missingpkgs)


# This may take a while. When it is all done,
# re-check for missing packages:

newpkgs <- dir(path = newlib)

missingpkgs <- setdiff(df$package, newpkgs)

length(missingpkgs)

df2 <- df[df$package %in% missingpkgs,]


# check and install any remaining packages from Github:

if (!require("devtools", quietly = TRUE)) {
  install.packages("devtools")
} #This checks and installs the devtools package if needed

for (i in which(df2$github_or_not)){
  devtools::install_github(paste(df2$username[i], df2$package[i], sep = "/"))
}


# Option 2: install only desired packages ----

# Instead installing all old packages, create a list
# of the packages you do want to install, either in R
# or in a tab-delimited file. Here, I will start with
# all the old packages and hand-edit it.

#write.table(df[df$package %in% missingpkgs,], file = "~/checkRpackages.txt")

#Read back in after modifying

pkgList <- read.delim("~/checkRpackages2.txt")
dim(pkgList)

toinstall <- pkgList$package


if (!require("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

BiocManager::install(toinstall)

#You may still get warnings about missing packages
#if any desired package is deprecated or only
#available on Github. As before, these can
#be ignored for now. This also will likely
#install more than the requested packages as
#they have dependencies

#See what did not get installed:

newlib <- "/home/apps/software/R/4.3.2-IGB-gcc-8.2.0/lib64/R/library"
newpkgs <- dir(path = newlib)

missingpkgs <- setdiff(toinstall, newpkgs)

length(missingpkgs)

pkgList2 <- pkgList[pkgList$package %in% missingpkgs,]


# check and install any remaining packages from Github:

if (!require("devtools", quietly = TRUE)) {
  install.packages("devtools")
} #This checks and installs the devtools package if needed

for (i in which(pkgList2$github_or_not)){
  devtools::install_github(paste(pkgList2$username[i], pkgList2$package[i], sep = "/"))
}


# if all looks good, quit this version of R without saving objects

q(save = "no")


