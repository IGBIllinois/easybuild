from easybuild.easyblocks.generic.cmakemake import CMakeMake
from easybuild.easyblocks.generic.pythonpackage import PythonPackage
from easybuild.easyblocks.generic.makecp import MakeCp

class EB_ArcadeLearningEnvironment(PythonPackage,CMakeMake,MakeCp):
	"""Builds the Arcade Learning Environment

	Uses cmake, make, pip install, then copies the executable to bin
	"""
	@staticmethod
	def extra_options(extra_vars=None):
		return MakeCp.extra_options(extra_vars=extra_vars)

	def __init__(self, *args, **kwargs):
		PythonPackage.__init__(self,*args, **kwargs)
		MakeCp.__init__(self,*args,**kwargs)

	def configure_step(self):
		PythonPackage.configure_step(self)
		return CMakeMake.configure_step(self)

	def build_step(self):
		return CMakeMake.build_step(self)

	def install_step(self):
		files_to_copy = self.cfg.get('files_to_copy', [])
		self.log.info("Starting install_step with files_to_copy: %s" % files_to_copy)
		PythonPackage.install_step(self)
		return MakeCp.install_step(self)

	def sanity_check_step(self, *args, **kwargs):
		return MakeCp.sanity_check_step(self, *args, **kwargs)

	def make_module_extra(self):
		return PythonPackage.make_module_extra(self)
