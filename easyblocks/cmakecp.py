from easybuild.easyblocks.generic.cmakemake import CMakeMake
from easybuild.easyblocks.generic.makecp import MakeCp

class CMakeCp(CMakeMake,MakeCp):
	"""Builds the Arcade Learning Environment

	Uses cmake, make, then copies the executable to bin
	"""
	@staticmethod
	def extra_options(extra_vars=None):
		return MakeCp.extra_options(extra_vars=extra_vars)

	def __init__(self, *args, **kwargs):
		CMakeMake.__init__(self,*args,**kwargs)

	def configure_step(self):
		return CMakeMake.configure_step(self)

	def build_step(self):
		return CMakeMake.build_step(self)

	def install_step(self):
		return MakeCp.install_step(self)

	def sanity_check_step(self, *args, **kwargs):
		return MakeCp.sanity_check_step(self, *args, **kwargs)

