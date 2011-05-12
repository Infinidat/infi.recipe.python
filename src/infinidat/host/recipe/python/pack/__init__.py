__import__("pkg_resources").declare_namespace(__name__)

from zc.buildout import UserError

def _get_git_version():
    from infinidat.host.recipe.version.git import GitFlow
    return GitFlow().head._describe_match("v*").strip('v')

def _get_os_version():
    import platform
    system = platform.system().lower().replace('-', '').replace('_', '')
    if system == 'linux':
        dist_name = platform.dist()[0].lower()
        if dist_name == 'ubuntu':
            dist_version  = platform.dist()[1].lower()
        else:
            dist_version  = platform.dist()[1].lower().split('.')[0]
        arch = 'x86' if '32bit' in platform.architecture()[0] else 'x64'
        return "-".join([system, dist_name, dist_version , arch])
    if system == 'windows':
        arch = 'x86' if '32bit' in platform.architecture()[0] else 'x64'
        return "-".join([system, arch])
    if system == 'darwin':
        arch = 'x86' if '32bit' in platform.architecture()[0] else 'x64'
        return "-".join(["macosx", arch])
    return ''

def _get_version():
    return "%s-%s" % (_get_git_version(), _get_os_version())

class Recipe(object):
    def __init__(self, buildout, name, options):
        self._buildout = buildout
        self._options = options
        self._section_name = name

    def _test_source_directory(self):
        from os.path import isdir, exists
        from os import access, R_OK
        if not self.source:
            raise UserError("missing source_directory")
        if not access(self.source, R_OK):
            raise UserError("cannot read %s" % self.source)
        if not isdir(self.source):
            raise UserError("%s is not a directory" % self.source)

    def _test_distination_file(self):
        from os.path import isfile, exists
        from os import access, W_OK
        if not self.destination_file:
            raise UserError("missing source_directory")
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
        self._write_archive()
        self._popd()
        self._options.created(self.destination_file)
        return self._options.created()

    def _write_archive(self):
        import tarfile
        archive = tarfile.open(name = self.destination_file, mode = 'w:gz')
        archive.add(self.source, arcname = 'python')

    def update(self):
        pass

