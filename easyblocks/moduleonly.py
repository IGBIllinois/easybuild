from easybuild.easyblocks.generic.configuremake import ConfigureMake

class ModuleOnly(ConfigureMake):
	"""Creates only the module and does sanity checks only

	"""
	@staticmethod
	def extra_options(extra_vars=None):
		return ConfigureMake.extra_options(extra_vars=extra_vars)

	def __init__(self, *args, **kwargs):
		ConfigureMake.__init__(self,*args,**kwargs)

	def configure_step(self):
		pass

	def build_step(self):
		pass

	def install_step(self):
		pass

	def sanity_check_step(self, *args, **kwargs):
		return ConfigureMake.sanity_check_step(self, *args, **kwargs)

