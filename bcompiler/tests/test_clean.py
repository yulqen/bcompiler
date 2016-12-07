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

    # TODO - unable to detect strings in "2015-02-23" format as yet
#    assert d2.clean().month == 6
#    assert d2.clean().year == 2017
#    assert d2.clean().day == 3
