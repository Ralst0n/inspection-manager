from apps.utils.helpers import *


class TestDate():
    def test_returns_true_if_before(self):
        assert before_cutoff_date('05/05/1968', '11/26/1990') == True

    def test_returns_false_if_after(self):
        assert before_cutoff_date('01/11/1994', '02/19/1993') == False

    def test_after_last_scrape(self):
        assert after_last_scrape(
            '05/05/1968', '11/26/1990') == "05/05/1968 is before 11/26/1990"
        assert after_last_scrape(
            '01/11/1994', '02/19/1993') == "01/11/1994 is before 02/19/1993"
