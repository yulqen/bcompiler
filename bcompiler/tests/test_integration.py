import subprocess

from bcompiler import __version__


def test_bcompiler_help():
    output = subprocess.run(['bcompiler', '-h'], stdout=subprocess.PIPE, encoding='utf-8')
    assert output.stdout.startswith('usage')


def test_bcompiler_version():
    output = subprocess.run(['bcompiler', '-v'], stdout=subprocess.PIPE, encoding='utf-8')
    assert output.stdout.strip() == __version__


def test_bcompiler_count_rows(populated_template):
    output = subprocess.run(['bcompiler', '-r'], stdout=subprocess.PIPE, encoding='utf-8')
    assert output.stdout.startswith('Workbook')
