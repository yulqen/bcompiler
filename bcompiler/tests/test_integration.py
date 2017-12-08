import subprocess


def test_bcompiler_help():
    output = subprocess.run(['bcompiler', '-h'], stdout=subprocess.PIPE, encoding='utf-8')
    assert output.stdout.startswith('usage')
