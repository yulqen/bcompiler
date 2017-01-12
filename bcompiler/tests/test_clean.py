"""
After data from the BICC forms is migrated into a compiled_master.xlsx file,
we need to avoid having to re-save this file as csv and then manually removing
all in-cell commas, so that we can create a transposed_master elsewhere in the
application, because that's a major pain in the backside. So what we're going
here is performing clean-up functions on the resulting compiled_master.xlsx
file that is created straight after the BICC forms compilation. That will then
absolve us from all hassle.
"""
from datetime import date

from bcompiler.process import Cleanser

from bcompiler.utils import simple_round, bc_is_close, quick_typechecker


def test_cleanser_class():
    # comma strings
    commas_str = ("There is tonnes of stuff to think about, we need to clean."
                  " There are multiple commas in here, see? Big commas, big!")
    commas_str2 = ("Millions, upon, millions, of commas! We love ,commas"
                   " even,  if they are malplaced, okay?? , ")

    # apostrophe strings
    apos_str = "'Bobbins ' ' ' ''"
    apos_str2 = "Bobbins ' ' ' ''"

    # mix apos and comma strings
    mix_apos_commas = "'There are mixes, here! Aren't there, yes!"

    # newline strings
    newline_str1 = "There are many ways to write newlines\nand this is one."
    newline_str2 = "Bobbins\nbobbins\nbobbins\nbobbins\nbobbins"

    # date strings
    # dd/mm/yyyy format
    d_d_str = "03/06/2017"

    # with 0:00:00 time format
    d_time_str = "2015-04-01 0:00:00"
    d_time_str2 = "2015-12-31 0:00:00"
    d_time_bad_date = "2015-12-32 0:00:00"

    # integer strings
    i_str = "1234"

    # float strings
    f_str = "12.34"

    # clean percentage sign
    percent_str = "100%"
    percent_str2 = "85%"

    # pound sign
    pound_str = "£12.24"
    pound_str2 = "£12.2499"  # not having that
    pound_str3 = "£20"  # we want to return this as a float too
    pound_str_neg = "-£20"
    pound_str_context = ("£200 - There is a load of test surrounding £20 "
                         "which we do not wish to match!")

    # create Cleanser objects for them all
    c = Cleanser(commas_str)
    c2 = Cleanser(commas_str2)
    a = Cleanser(apos_str)
    a2 = Cleanser(apos_str2)
    mix = Cleanser(mix_apos_commas)
    nl = Cleanser(newline_str1)
    nl2 = Cleanser(newline_str2)
    d = Cleanser(d_d_str)
    dt = Cleanser(d_time_str)
    dt2 = Cleanser(d_time_str2)
    d_bad_date = Cleanser(d_time_bad_date)
    i = Cleanser(i_str)
    f = Cleanser(f_str)
    p = Cleanser(percent_str)
    p2 = Cleanser(percent_str2)
    pnd = Cleanser(pound_str)
    pnd2 = Cleanser(pound_str2)
    pnd3 = Cleanser(pound_str3)
    pnd_neg = Cleanser(pound_str_neg)
    pnd_context = Cleanser(pound_str_context)

    # testing private interface to ensure counting of targets is done
    assert c._checks[c._access_checks('commas')]['count'] == 3
    assert c2._checks[c._access_checks('commas')]['count'] == 7
    assert a._checks[c._access_checks('leading_apostrophe')]['count'] == 1
    assert a2._checks[c._access_checks('leading_apostrophe')]['count'] == 0
    assert mix._checks[c._access_checks('commas')]['count'] == 2
    assert mix._checks[c._access_checks('leading_apostrophe')]['count'] == 1

    # regex checks
    assert nl2.clean() == "Bobbins | bobbins | bobbins | bobbins | bobbins"
    assert nl.clean() == ("There are many ways to write newlines | and this "
                          "is one.")
    assert mix.clean() == "There are mixes here! Aren't there yes!"
    assert c.clean() == ("There is tonnes of stuff to think about we need "
                         "to clean. There are multiple commas in here see? "
                         "Big commas big!")
    assert c2.clean() == ("Millions upon millions of commas! We love "
                          "commas even if they are malplaced okay?? ")
    assert dt.clean() == date(2015, 4, 1)
    assert dt2.clean() == date(2015, 12, 31)
    assert d_bad_date.clean() == d_time_bad_date  # return it and log error
    assert d.clean().month == 6
    assert d.clean().year == 2017
    assert d.clean().day == 3
    assert i.clean() == 1234
    assert f.clean() == 12.34
    assert p.clean() == 1.0
    assert p2.clean() == 0.85
    assert pnd.clean() == 12.24
    assert pnd2.clean() == 12.24
    assert pnd3.clean() == 20.0
    assert pnd_neg.clean() == -20.0
    assert pnd_context.clean() == ("£200 - There is a load of test "
                                   "surrounding £20 which we do not wish "
                                   "to match!")

    # TODO - unable to detect strings in "2015-02-23" format as yet
#    assert d2.clean().month == 6
#    assert d2.clean().year == 2017
#    assert d2.clean().day == 3


def test_simple_round():
    x = 2.99000000002
    x2 = 2.9323
    x = simple_round(x, 2)
    x2 = simple_round(x2, 2)
    assert x == 2.99
    assert x2 == 2.93


def test_is_close():
    x = 2.9900000002
    y = 2.99

    x1 = 2.98
    y1 = 2.99

    x2 = 2
    y2 = 3

    x3 = 2.995
    y3 = 2.99

    assert bc_is_close(x, y) is True
    assert bc_is_close(x1, y1) is False
    assert bc_is_close(x2, y2) is False
    assert bc_is_close(x3, y3) is False


def test_quick_typechecker():

    class Tester:
        pass
    tester = Tester()

    s = 'Shuttlecock'
    i = 1
    f = 1.65

    s1 = 'Shuttlecock sneffles bobbins chorley'
    i1 = 2339930
    f1 = 1.23232114411144

    d = date(2017, 1, 23)
    n = None

    assert quick_typechecker(s, i, f) is False
    assert quick_typechecker(s, s, s) is False
    assert quick_typechecker(i, i, i) is True
    assert quick_typechecker(i) is True
    assert quick_typechecker(f) is True
    assert quick_typechecker(s1) is False
    assert quick_typechecker(i1) is True
    assert quick_typechecker(f1) is True
    assert quick_typechecker(d) is False
    assert quick_typechecker(n) is False
    assert quick_typechecker(tester) is False
