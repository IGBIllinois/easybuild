from easybuild.easyblocks.generic.cmdcp import CmdCp
from easybuild.easyblocks.gitclonemakecp import GitCloneMakeCp

# Work In Progress

class GitCloneMakeCp(GitCloneMakeCp, CmdCp):
    """Builds the Arcade Learning Environment

    Uses cmake, make, then copies the executable to bin
    """
    @staticmethod
    def extra_options(extra_vars=None):
        if extra_vars is None:
            extra_vars = {}
        extra = CmdCp.extra_options(extra_vars=extra_vars)
        return GitCloneMakeCp.extra_options(extra_vars=extra)

    def __init__(self, *args, **kwargs):
        GitCloneMakeCp.__init__(self,*args,**kwargs)

    def fetch_step(self, skip_checksums=True):
        GitCloneMakeCp.fetch_step(self,True)
    
    def checksum_step(self):
        GitCloneMakeCp.checksum_step(self)

    def extract_step(self):
        GitCloneMakeCp.extract_step(self)

    def configure_step(self, cmd_prefix=''):
        CmdCp.configure_step(self, cmd_prefix=cmd_prefix)

    def build_step(self):
        CmdCp.build_step(self)

    def install_step(self):
        CmdCp.install_step(self)
    
