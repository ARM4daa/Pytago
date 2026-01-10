from pythonforandroid.recipe import CompiledComponentsPythonRecipe

class PytagoLibRecipe(CompiledComponentsPythonRecipe):

	site_packages_name = 'pytago_lib'
	depends = ['setuptools']
	call_hostpython_via_targetpython = False

	def should_build(self, arch):
		return True

recipe = PytagoLibRecipe()
