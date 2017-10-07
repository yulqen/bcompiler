from typing import List

import os
import sys
import shutil
import re
import subprocess

DOCS = os.path.join(os.path.expanduser('~'), 'Documents')
BCOMPILER_WORKING_D = 'bcompiler'
ROOT_PATH = os.path.join(DOCS, BCOMPILER_WORKING_D)
SOURCE_DIR = os.path.join(ROOT_PATH, 'source')
RETURNS_DIR = os.path.join(SOURCE_DIR, 'returns')
OUTPUT_DIR = os.path.join(ROOT_PATH, 'output')
REPO_ZIP = 'https://bitbucket.org/mrlemon/bcompiler/get/master.zip'
REPO_GIT = 'https://github.com/departmentfortransport/bcompiler_datamap_files.git'
CONFIG_FILE = os.path.join(SOURCE_DIR, 'config.ini')

GIT_COMMANDS = {
    'untracked': 'git ls-files --others --exclude-standard',
    'status': 'git status',
}


def _git_command(opts: str) -> str:
    """
    Wraps a string git command with a subprocess.run() call, encoding
    stdout.
    :param opts: git command as a str
    :return: str of stdout of command
    """
    return subprocess.run(opts.split(), encoding='utf-8',
                          stdout=subprocess.PIPE).stdout


def _git_check_untracked(dir: str) -> None:
    """
    Discover untracked files in local git repository.
    :param dir: directory containing repository
    :return:
    """
    print("Checking for untracked files...\n")
    os.chdir(dir)
    g_output = _git_command(GIT_COMMANDS['untracked']).split('\n')
    if g_output:
        print("You have files in your auxiliary folder that have not been added to the repository.\n")
        for f in g_output:
            print("\t{}".format(f))
    _discover_master_file(g_output)


def _discover_master_file(g_output: List[str]) -> None:
    """
    Simple test of a string for something that looks like a master xlsx file. We don't want them in the repo,
     particularly if we're about to raze the directory structure.
    :param g_output:
    :return:
    """
    for f in g_output:
        master_f = re.match(r'^.+(?P<master_file>(master|MASTER|Master).+xlsx)', f)
        if master_f:
            print(
                "It looks as though you have a master document in the directory: \n\n\t{}.\n\nPlease remove the master file.\n\n"
                "Master files should not be committed to the auxiliary files repository and "
                "if you we are going to wipe out the repository and start again, you will lose "
                "the master.\n\nPlease copy to a safe directory somewhere, such as your Desktop before "
                "proceeding.".format(master_f.group('master_file')))


def _git_check_modified_files(dir: str) -> None:
    """
    Discover any modified files in local git repository.
    :param dir: directory containing repository
    :return:
    """
    print("Checking for modified files...\n")
    os.chdir(dir)
    g_output = _git_command(GIT_COMMANDS['status']).split('\n')
    for i in g_output:
        mod = re.match(r'\tmodified:\s+(?P<file>.+$)', i)
        if mod:
            print("You have modified files and your repository is not clean.\n")
            print("File: {}".format(mod.group('file')))
    print("You do not have modified files in the auxiliary directory.\n\n")


def main():
    """
    Purpose of this is to bootstrap the system.
    """
    if os.path.exists(ROOT_PATH):
        response = input(
            "This will REMOVE any existing directories containing bcompiler " "auxiliary files (e.g. MyDocuments/bcompiler/source or ~/Documents/"
            "bcompiler/source, depending on your operating system.\n Do you "
            "wish to continue? (y/n) ")
        if response in ['N', 'No', 'NO', 'n']:
            sys.exit()
        else:
            # print(f"Deleting {SOURCE_DIR} and all files within")
            # shutil.rmtree(ROOT_PATH)
            # print("Old auxiliary directory removed")
            _git_check_modified_files(SOURCE_DIR)
            _git_check_untracked(SOURCE_DIR)
            sys.exit()
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
