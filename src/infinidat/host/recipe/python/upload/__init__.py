__import__("pkg_resources").declare_namespace(__name__)

class Recipe(object):
    def __init__(self, buildout, name, options):
        pass
    
    def install(self):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError