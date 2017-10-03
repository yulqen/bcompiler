import os
import sys
import subprocess


def main():
    """
    Purpose of this is to bootstrap the system.
    """
    DOCS = os.path.join(os.path.expanduser('~'), 'Documents')
    BCOMPILER_WORKING_D = 'bcompiler'
    ROOT_PATH = os.path.join(DOCS, BCOMPILER_WORKING_D)
    SOURCE_DIR = os.path.join(ROOT_PATH, 'source')
    RETURNS_DIR = os.path.join(SOURCE_DIR, 'returns')
    REPO_ZIP = 'https://bitbucket.org/mrlemon/bcompiler/get/master.zip'
    REPO_GIT = 'https://github.com/departmentfortransport/bcompiler_datamap_files.git'
    if not os.path.exists(ROOT_PATH):
        print("There is no directory structure set up.")
        print("Creating it.")
        os.mkdir(ROOT_PATH)
        print(f"Created {SOURCE_DIR}")
    if os.name == 'posix':
        print("We're in Windows.")
        try:
            subprocess.run(["git", "--version"])
        except OSError as e:
            if e.errno == os.ENOENT:
                print("You don't have git installed, or it is not on your path."
                      "Go to https://git-scm.com/download/win and install it,"
                      " then run bcompiler-init again. Please make sure git"
                      "is in your PATH. This process may differ depending on"
                      "your installation. Please consult https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"
                      " for advice.")
                sys.exit()
        print(f"Using git to install necessary auxiliary files in "
              " {SOURCE_DIR}")
        subprocess.run(['git', 'clone', REPO_GIT, SOURCE_DIR], stdout=subprocess.PIPE)
    else:
        print("Not in Windows.")


if __name__ == '__main__':
    main()
