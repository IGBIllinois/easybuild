from easybuild.easyblocks.generic.configuremake import ConfigureMake

class MakeInstall(ConfigureMake):
	"""Builds the Arcade Learning Environment

	Uses cmake, make, then copies the executable to bin
	"""
	@staticmethod
	def extra_options(extra_vars=None):
		return ConfigureMake.extra_options(extra_vars=extra_vars)

	def __init__(self, *args, **kwargs):
		ConfigureMake.__init__(self,*args,**kwargs)

	def configure_step(self):
		return False

	def build_step(self):
		return ConfigureMake.build_step(self)

	def install_step(self):
		return ConfigureMake.install_step(self)

	def sanity_check_step(self, *args, **kwargs):
		return ConfigureMake.sanity_check_step(self, *args, **kwargs)

