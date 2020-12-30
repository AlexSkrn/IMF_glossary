from main import get_line


def test_get_line():
    text = ['a few']
    result = get_line(text, 4)
    expected = 'a few\t\t\t'

    assert result == expected

    text = ['несколько ', ' немногие']
    result = get_line(text, 4)
    expected = 'несколько\t\tнемногие\t'

    assert result == expected

    text = ['a number of ', ' [IMF]']
    result = get_line(text, 4)
    expected = 'a number of\t[IMF]\t\t'

    assert result == expected

    text = ['a ', ' [b] ', ' c ', ' d ', ' e']

    result = get_line(text, 6)
    expected = 'a\t[b]\tc\t\td\t\te'

    assert result == expected
