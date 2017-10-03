import os
import sys
import shutil
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
    OUTPUT_DIR = os.path.join(ROOT_PATH, 'output')
    REPO_ZIP = 'https://bitbucket.org/mrlemon/bcompiler/get/master.zip'
    REPO_GIT = 'https://github.com/departmentfortransport/bcompiler_datamap_files.git'
    CONFIG_FILE = os.path.join(SOURCE_DIR, 'config.ini')
    if os.path.exists(ROOT_PATH):
        response = input("This will REMOVE any existing directories containing bcompiler " "auxiliary files (e.g. MyDocuments/bcompiler/source or ~/Documents/"
                         "bcompiler/source, depending on your operating system.\n Do you "
                         "wish to continue? (y/n) \n ")
        if response in ['N', 'No', 'NO', 'n']:
            sys.exit()
        else:
            print(f"Deleting {SOURCE_DIR} and all files within")
            shutil.rmtree(ROOT_PATH)
            print("Old auxiliary directory removed")
        print("There is no directory structure set up.")
        print("Creating it.")
        os.mkdir(ROOT_PATH)
        print(f"Created {SOURCE_DIR}")
    else:
        print("There is no directory structure set up.")
        print("Creating it.")
        os.mkdir(ROOT_PATH)
        print(f"Created {SOURCE_DIR}")
    if os.name == 'nt':
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
        print(f"Using git to install necessary auxiliary files in {SOURCE_DIR}")
        subprocess.run(['git', 'clone', REPO_GIT, SOURCE_DIR], stdout=subprocess.PIPE)
        os.mkdir(RETURNS_DIR)
        os.mkdir(OUTPUT_DIR)
        print(f"Please review {CONFIG_FILE} to set options.")
    else:
        print("Not in Windows.")
        try:
            subprocess.run(["git", "--version"])
        except OSError as e:
            if e.errno == os.ENOENT:
                print("You don't have git installed, or it is not on your path."
                      " Install git from your distribution repository or from "
                      " the git web site if you're using a Mac: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git")
                sys.exit()
        print(f"Using git to install necessary auxiliary files in {SOURCE_DIR}")
        subprocess.run(['git', 'clone', REPO_GIT, SOURCE_DIR], stdout=subprocess.PIPE)
        os.mkdir(RETURNS_DIR)
        os.mkdir(OUTPUT_DIR)
        print(f"Please review {CONFIG_FILE} to set options.")


if __name__ == '__main__':
    main()
