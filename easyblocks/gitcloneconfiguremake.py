import os
import re
import shutil
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.framework.easyconfig import MANDATORY
from easybuild.framework.easyconfig.easyconfig import letter_dir_for
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import mkdir, rmtree2
from easybuild.tools.run import run_cmd
from easybuild.tools.config import source_paths

# Work In Progress

class GitCloneConfigureMake(ConfigureMake):
    """Builds the Arcade Learning Environment

    Uses cmake, make, then copies the executable to bin
    """
    @staticmethod
    def extra_options(extra_vars=None):
        extra = {
            'git_commit': ['', "Commit number to check out", MANDATORY],
        }
        if extra_vars is None:
            extra_vars = {}
        extra.update(extra_vars)
        return ConfigureMake.extra_options(extra_vars=extra)

    def __init__(self, *args, **kwargs):
        ConfigureMake.__init__(self,*args,**kwargs)

    def fetch_step(self, skip_checksums=True):
        ConfigureMake.fetch_step(self,True)

    def fetch_sources(self, sources=None, checksums=None):
        """
        Add a list of source files (git repositories)

        :param sources: list of sources to fetch (if None, use 'sources' easyconfig parameter)
        :param checksums: list of checksums for sources
        """
        if sources is None:
            sources = self.cfg['sources']
        if checksums is None:
            checksums = self.cfg['checksums']

        for index, source in enumerate(sources):
            extract_cmd = 'cp -r %(filename)s %(target)s'

            if isinstance(source, basestring):
                filename = source
            else:
                raise EasyBuildError("Unexpected source spec, not a string: %s", source)

            # check if the repo can be located
            path = self.obtain_repo(filename)
            if path:
                self.log.debug('File %s found for source %s' % (path, filename))
                self.src.append({
                    'name': filename,
                    'path': path, 
                    'cmd': extract_cmd,
                    'checksum': None,
                    'finalpath': self.builddir,
                })
            else:
                raise EasyBuildError('No repo found for source %s', filename)

        self.log.info("Added sources: %s", self.src)
            
    def obtain_repo(self, url, force_download=False):
        """
        Downloads the repo from the given url, then updates submodules
        :param url: url of git repository
        """
        srcpaths = source_paths()
        if re.match(r"^(https?)://", url):
            # URL detected, try and download it
            reponame = url.split('/')[-1].split('.')[0]

            # Try and find the repo in the sources directory first
            foundfile = None
            failedpaths = []
            for path in srcpaths:
                # create list of candidate filepaths
                namepath = os.path.join(path, self.name)
                letterpath = os.path.join(path, letter_dir_for(self.name), self.name)
                candidate_filepaths = [
                    letterpath, namepath, path
                ]
                # look for repo in those locations
                for cfp in candidate_filepaths:
                    fullpath = os.path.join(cfp, reponame)
                    if os.path.isdir(fullpath):
                        self.log.info("Found repo %s at %s", reponame, fullpath)
                        foundfile = os.path.abspath(fullpath)
                        if force_download:
                            print_warning("Found file %s at %s, but re-downloading it anyway..." % (reponame, foundfile))
                            foundfile = None
                        break
                    else: 
                        failedpaths.append(fullpath)
            if foundfile:
                if self.dry_run:
                    self.dry_run_msg("  * %s found at %s", filename, foundfile)
                return foundfile
            else:
                # Figure out where to clone the repo to
                repopath = os.path.join(srcpaths[0], letter_dir_for(self.name), self.name)
                self.log.info("Creating path %s to clone repo to" % repopath)
                mkdir(repopath, parents=True)

                # Remove repo, if it has previously been downloaded (we must be forcing download)
                fullpath = os.path.join(repopath, reponame)
                if os.path.exists(fullpath):
                    rmtree2(fullpath);

                try:
                    if self.download_repo(reponame, url, repopath):
                        return fullpath
                except IOError, err:
                    raise EasyBuildError("Downloading file %s from url %s to %s failed: %s", filename, url, fullpath, err)
        else:
            raise EasyBuildError("Source must be a url to a git repository: %s", url)

    def download_repo(self, reponame, url, path):
        """Clone a repo from the given URL to the specified path"""
        self.log.debug("Trying to download %s from %s to %s", reponame, url, path)

        cmd = "git clone %(url)s %(path)s/%(reponame)s && cd %(path)s/%(reponame)s && git checkout %(git_commit)s && git submodule update --init --recursive && cd -" % {
            'url': url,
            'path': path,
            'reponame': reponame,
            'git_commit': self.cfg['git_commit'],
        }

        downloaded = run_cmd(cmd, log_all=True, simple=True)

        if downloaded:
            self.log.info("Successful clone of repo %s from url %s to path %s" % (reponame, url, path))
            return path
        else:
            self.log.warning("Clone of repo %s to %s failed" % (url, path))
            return None
    
    def checksum_step(self):
        self.log.info("Skipping checksums")
        pass

    def extract_step(self):
        """ Copy all source files to the build directory """
        for source in self.src:
            self.log.info("Unpacking source %s" % source['name'])
            src = source['path']
            dst = os.path.join(self.builddir, source['path'].split('/')[-1])
            try:
                shutil.copytree(src, dst)
            except (OSError, IOError), err:
                raise EasyBuildError("Couldn't copy %s to %s: %s", src, dst, err)
    
