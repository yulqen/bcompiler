from ..compile import encode_win


def test_cp1252_encode():
    wind_string = "£30"
    assert encode_win(wind_string) == "£30"
