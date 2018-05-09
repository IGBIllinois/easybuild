from easybuild.easyblocks.generic.cmakemake import CMakeMake
from easybuild.easyblocks.generic.gitcloneconfiguremake import GitCloneConfigureMake

# Work In Progress

class GitCloneCMakeMake(GitCloneConfigureMake, CMakeMake):
    """Builds the Arcade Learning Environment

    Uses cmake, make, then copies the executable to bin
    """
    @staticmethod
    def extra_options(extra_vars=None):
        if extra_vars is None:
            extra_vars = {}
        extra = CMakeMake.extra_options(extra_vars=extra_vars)
        return GitCloneConfigureMake.extra_options(extra_vars=extra)

    def __init__(self, *args, **kwargs):
        GitCloneConfigureMake.__init__(self,*args,**kwargs)

    def fetch_step(self, skip_checksums=True):
        GitCloneConfigureMake.fetch_step(self,True)
    
    def checksum_step(self):
        GitCloneConfigureMake.checksum_step(self)

    def extract_step(self):
        GitCloneConfigureMake.extract_step(self)

    def configure_step(self, srcdir=None, builddir=None):
        CMakeMake.configure_step(self, srcdir=srcdir, builddir=builddir)
    
