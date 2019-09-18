__import__("pkg_resources").declare_namespace(__name__)

from infi.os_info import get_platform_string, get_version_from_git

def _get_version():
    return "%s-%s" % (get_version_from_git(), get_platform_string())

class Recipe(object):
    """ This recipe packs the 'dist' directory to python-<version>-<arch>.tar.gz
    it honor the following options:
    include_list: list of paths to add to the archive
    exclude_list: list of paths that match the include list but should be excluded

    note that each path should start with dist
    """
    def __init__(self, buildout, name, options):
        self._buildout = buildout
        self._options = options
        self._section_name = name

    def _test_source_directory(self):
        from zc.buildout import UserError
        from os.path import isdir, exists
        from os import access, R_OK
        if not self.source:
            raise UserError("missing source_directory")
        if not access(self.source, R_OK):
            raise UserError("cannot read %s" % self.source)
        if not isdir(self.source):
            raise UserError("%s is not a directory" % self.source)

    def _test_distination_file(self):
        from zc.buildout import UserError
        from os.path import isfile, exists
        from os import access, W_OK
        if not self.destination_file:
            raise UserError("missing destination_file")
        if not access(self.source, W_OK):
            raise UserError("cannot write %s" % self.destination_file)

    def _pushd(self):
        from os.path import curdir, abspath, relpath
        from os import chdir
        self._curdir = abspath(curdir)
        self._buildout_path = self._buildout.get('buildout').get('directory')
        chdir(self._buildout_path)

    def _popd(self):
        from os import chdir
        chdir(self._curdir)

    def install(self):
        self._pushd()
        self.source = 'dist'
        self.destination_file = 'python-%s.tar.gz' % _get_version()
        self._test_source_directory()
        self._test_distination_file()
        self._build_include_list()
        self._write_archive()
        self._popd()
        self._options.created(self.destination_file)
        return self._options.created()

    def _write_archive(self):
        import tarfile
        archive = tarfile.open(name=self.destination_file, mode='w:gz')
        archive.add(name=self.source, arcname='python', filter=self._tarfile_filter)

    def _build_include_list(self):
        self._include_list = [path.strip() for path in self._options.get("include_list", '').splitlines()]
        if '' in self._include_list:
            self._include_list.remove('')
        self._exclude_list = [path.strip() for path in self._options.get("exclude_list", '').splitlines()]
        if '' in self._exclude_list:
            self._exclude_list.remove('')

    def _tarfile_filter(self, tarinfo):
        path = tarinfo.path
        if path in self._exclude_list:
            return None
        if path in self._include_list:
            return tarinfo
        for basepath in self._include_list:
            if path in basepath:
                return tarinfo
            if basepath in path:
                return tarinfo
        return None

    def update(self):
        pass
