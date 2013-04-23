__import__("pkg_resources").declare_namespace(__name__)

import unittest
from zc.buildout import buildout
from mock import patch

class RecipeTestCase(unittest.TestCase):

    def setUp(self):
        from os import mkdir
        from os.path import exists
        if not exists('dist'):
            mkdir('dist')

    def _verify_downloaded_python(self):
        from os.path import exists, sep
        self.assertTrue(sep.join(['parts','bin','python']))

    @patch('infi.recipe.python.pack._get_version')
    def test_pack_1(self, _get_version):
        _get_version.return_value = 12345
        args = '-c buildout-tests.cfg install test_pack_1'
        try:
            buildout.main(args.split())
        except SystemExit:
            pass
        self._verify_tarfile('python-12345.tar.gz')

    def _verify_tarfile(self, name):
        import tarfile
        from os.path import exists
        self.assertTrue(exists(name), 'not found: %s' % name)

    def test_dry_run(self):
        args = '-c buildout-tests.cfg'
        buildout.main(args.split())

