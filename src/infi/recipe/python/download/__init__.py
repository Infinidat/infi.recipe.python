__import__("pkg_resources").declare_namespace(__name__)

DOWNLOAD_BASE  = 'ftp://python.infinidat.com/python'

class Recipe(object):
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.options = options
        self.buildout = buildout
        self._set_extract_path()
        self._set_url()

    def _set_extract_path(self):
        from os.path import sep
        self.buildout_directory = self.buildout.get('buildout').get('directory')
        DEFAULT_EXTRACT_PATH = sep.join([self.buildout_directory, 'parts'])
        self.extact_path = self.options.get('extract_path', DEFAULT_EXTRACT_PATH)

    def _set_url(self):
        from zc.buildout import UserError
        self.version = self.options.get('version', None)
        if not self.version:
            raise UserError("version option is missing")
        self.download_base = self.options.get('download-base', DOWNLOAD_BASE)
        if not self.download_base:
            raise UserError("download-base option is missing")
        from ..pack import _get_os_version
        filename = "python-%s-%s.tar.gz" % (self.version, _get_os_version())
        self.url = "/".join([self.download_base, filename])

    def install(self):
        self._download()
        self._extract()
        self._notify_on_files_extracted()
        return self.options.created()

    def _download(self):
        from zc.buildout.download import Download
        download = Download(self.buildout.get('buildout'))
        self.download_path = download(self.url)[0]

    def _extract(self):
        import tarfile
        archive = tarfile.open(self.download_path, 'r:gz')
        archive.extractall(self.extact_path)
        archive.close()

    def _get_filenames_from_archive(self):
        import tarfile
        archive = tarfile.open(self.download_path, 'r:gz')
        files = archive.getnames()
        archive.close()
        return files

    def _notify_on_files_extracted(self):
        from os.path import sep
        files = self._get_filenames_from_archive()
        for path in [sep.join([self.extact_path, file]) for file in files]:
            self.options.created(path)

    def update(self):
        pass
