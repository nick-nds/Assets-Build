import sys
from pathlib import Path
from shutil import copy
from shutil import make_archive
from shutil import rmtree

class Assets:

    project_path = ''

    def __init__(self, version):
        self.version = version

    # init project config
    def project(self):
        config_file = Path("config")
        if config_file.is_file():
            f = open("config", "r")
            self.project_path = f.readline()
            f.close()
            if Path(self.project_path).is_dir():
                return self.project_path
        else:
            self.config()

    # get and verify config details
    def config(self):
        path = input('Enter the absolute path to project folder: ')
        if Path(path).is_dir():
            self.project_path = path

            # write project path in config
            f = open("config", "w")
            f.write(self.project_path)
            f.close()

            self.tree()
        else:
            print('Folder {} does not exist'.format(path))
            self.config()

    # build assets
    def tree(self):
        if Path(self.version).is_dir():
            print('Version {} already exists'.format(self.version))
            sys.exit()

        tree = [
                Path(self.version) / 'admin/css',
                Path(self.version) / 'admin/js',
                Path(self.version) / 'web/css',
                Path(self.version) / 'web/js'
            ]

        print('============================================')
        print('============================================')
        print('Make sure you have run production build.')
        print('Make sure you are in correct branch')
        print("Creating assets from project folder \n {}".format(self.project_path))
        query = input('Do you wish to continue? <Y/n> ')
        query = query.lower()
        if query == "" or query == "yes" or query == "y":
            pass
        else:
            sys.exit()

        for i in tree:
            i.mkdir(parents=True, exist_ok=True)

        mapping = {}
        mapping[tree[0]] = [
                Path(self.project_path) / "public/css/admin/app.css",
                Path(self.project_path) / "public/css/admin/custom.css",
                Path(self.project_path) / "public/css/admin/style.css"
            ]

        mapping[tree[1]] = [
                Path(self.project_path) / "public/js/admin/app.js"
            ]

        mapping[tree[2]] = [
                Path(self.project_path) / "public/css/web/app.css",
                Path(self.project_path) / "public/css/vendors/ladda.min.css"
            ]

        mapping[tree[3]] = [
                Path(self.project_path) / "public/js/web/app.js"
            ]

        for i in mapping:
            for k in mapping[i]:
                copy(k, i)

        make_archive(self.version, 'zip', self.version)
        rmtree(self.version)
        print('Assets ready at {}.zip'.format(self.version))


if __name__ == "__main__":
    print('\nRemove config file to reset project folder\n')
    version = input('Enter version of the assets: ')
    assets = Assets(version)
    assets.project()
    assets.tree()
