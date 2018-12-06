from apps.utils.helpers import before_cutoff_date, dateField_format, formatted_date, list_blend
from datetime import datetime


class TestDate():
    ''' Tests for util functions that manipulate dates'''

    def test_returns_true_if_before(self):
        assert before_cutoff_date('05/05/1968', '11/26/1990') == True

    def test_returns_false_if_after(self):
        assert before_cutoff_date('01/11/1994', '02/19/1993') == False

    def test_dateField_format(self):
        assert dateField_format('01/01/1968') == '1968-01-01'

    def test_formatted_date(self):
        date_object = datetime(2018, 11, 26)
        assert formatted_date(date_object) == '11/26/2018'


class TestList():
    ''' Tests for util functions that manipulate lists'''

    def test_list_blend(self):
        odds = [1, 3, 5]
        evens = [2, 4, 6, 8]
        assert list_blend(odds, evens) == [1, 2, 3, 4, 5, 6, 8]
