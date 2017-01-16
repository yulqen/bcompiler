import pytest

from bcompiler.process.digest import digest_source_files


def test_digest_source_files():
    base_dir = '/home/lemon/Documents/bcompiler/source/returns'
    digest_source_files(base_dir)
