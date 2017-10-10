import pytest

from ..utils import directory_has_returns_check


@pytest.mark.skip("Only using as example")
def test_create_tmp_dir(tmpdir):
    """
    Example from the documentation - the file is removed.
    """
    p = tmpdir.mkdir("returns").join("TEST_RETURN.xlsm")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


def test_empty_returns_dir_throws_exception(tmpdir, capsys):
    d = tmpdir.mkdir("returns")
    directory_has_returns_check(d)
    out, err = capsys.readouterr()
    assert err == "Please copy populated return files to returns directory.\n"

