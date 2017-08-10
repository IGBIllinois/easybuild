from easybuild.easyblocks.generic.cmakemake import CMakeMake
from easybuild.easyblocks.generic.makecp import MakeCp

# Work In Progress

class GitSubmoduleMakeCp(MakeCp):
	"""Builds the Arcade Learning Environment

	Uses cmake, make, then copies the executable to bin
	"""
	@staticmethod
	def extra_options(extra_vars=None):
		extra = {
			'git_commit': ['', "Commit number to check out", MANDATORY],
		}
		if extra_vars is None:
			extra_vars = {}
		extra.update(extra_vars)
		return MakeCp.extra_options(extra_vars=extra_vars)

	def __init__(self, *args, **kwargs):
		CMakeMake.__init__(self,*args,**kwargs)

	def fetch_step(self, sources=None, checksums=None):
		"""
		Runs git clone, then git submodule update to fetch source files
		"""
		if self.cfg['sources']:
			pass
	
	def checksum_step(self):
		pass	
	
	def extract_step(self):
		pass
	
	
