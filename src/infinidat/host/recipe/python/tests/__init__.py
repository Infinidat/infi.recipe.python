__import__("pkg_resources").declare_namespace(__name__)

import unittest2
from zc.buildout import buildout
from mock import patch

class RecipeTestCase(unittest2.TestCase):
    
    def setUpAll(self):
        from os import mkdir
        from os.path import exists
        if not exists('dist'):
            mkdir('dist')
            
    @patch('infinidat.host.recipe.python.download._get_url')       
    def test_download_1(self, get_url):
        get_url.return_value = 'http://ci/job/python/label=linux-redhat-6-x86/lastBuild/artifact/python-2.7.1-1-g824ee1a-linux-linux-redhat-6-x86.tar.gz'
        args = '-c buildout-tests.cfg install test_download_1'
        buildout.main(args.split())
        self._verify_downloaded_python()
        
    def _verify_downloaded_python(self):
        from os.path import exists, sep
        self.assertTrue(sep.join(['parts','bin','python']))
        
    @patch('infinidat.host.recipe.python.pack._get_version')
    def test_pack_1(self, _get_version):
        _get_version.return_value = 12345
        args = '-c buildout-tests.cfg install test_pack_1'
        buildout.main(args.split())
        self._verify_tarfile('python-12345.tar.gz')
        
    def _verify_tarfile(self, name):
        import tarfile
        from os.path import exists
        self.assertTrue(exists(name))
            
    def test_dry_run(self):
        args = '-c buildout-tests.cfg'
        buildout.main(args.split())
        