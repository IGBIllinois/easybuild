"""
EasyBuild support for IGB gcc compiler toolchain (includes GCC, OpenMPI, OpenBLAS, LAPACK, ScaLAPACK and FFTW).

:author: Kenneth Hoste (Ghent University)
"""

from easybuild.toolchains.gompi import Gompi
from easybuild.toolchains.fft.fftw import Fftw
from easybuild.toolchains.linalg.openblas import OpenBLAS
from easybuild.toolchains.linalg.scalapack import ScaLAPACK

class Foss(Gompi, OpenBLAS, ScaLAPACK, Fftw):
    """Compiler toolchain with GCC, OpenMPI, OpenBLAS, ScaLAPACK and FFTW."""
    NAME = 'IGB-gcc'
    SUBTOOLCHAIN = Gompi.NAME
