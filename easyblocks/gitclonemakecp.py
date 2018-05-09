from easybuild.easyblocks.generic.makecp import MakeCp
from easybuild.easyblocks.generic.gitcloneconfiguremake import GitCloneConfigureMake

# Work In Progress

class GitCloneMakeCp(GitCloneConfigureMake, MakeCp):
    """Builds the Arcade Learning Environment

    Uses cmake, make, then copies the executable to bin
    """
    @staticmethod
    def extra_options(extra_vars=None):
        if extra_vars is None:
            extra_vars = {}
        extra = MakeCp.extra_options(extra_vars=extra_vars)
        return GitCloneConfigureMake.extra_options(extra_vars=extra)

    def __init__(self, *args, **kwargs):
        GitCloneConfigureMake.__init__(self,*args,**kwargs)

    def fetch_step(self, skip_checksums=True):
        GitCloneConfigureMake.fetch_step(self,True)
    
    def checksum_step(self):
        GitCloneConfigureMake.checksum_step(self)

    def extract_step(self):
        GitCloneConfigureMake.extract_step(self)

    def configure_step(self, cmd_prefix=''):
        MakeCp.configure_step(self, cmd_prefix=cmd_prefix)

    def install_step(self):
        MakeCp.install_step(self)