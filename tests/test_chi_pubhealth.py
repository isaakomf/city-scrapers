from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.chi_pubhealth import ChiPubHealthSpider

test_response = file_response(
    join(dirname(__file__), "files", "chi_pubhealth.html"),
    url=(
        "https://www.chicago.gov/city/en/depts/cdph/supp_info/boh/2022-board-of-health-meetings.html"  # noqa
    ),
)
spider = ChiPubHealthSpider()

freezer = freeze_time("2022-01-01")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_meeting_count():
    # 1 meeting per month
    assert len(parsed_items) == 3

#
# def test_unique_id_count():
#     assert len(set([item["id"] for item in parsed_items])) == 12
#
#
def test_title():
    assert parsed_items[0]["title"] == "Board of Health"


# def test_description():
#     assert parsed_items[0]["description"] == ""
#
#
# def test_start():
#     assert parsed_items[0]["start"] == datetime(2021, 1, 20, 9)
#
#
# def test_end():
#     assert parsed_items[0]["end"] is None
#
#
# def test_id():
#     assert parsed_items[0]["id"] == "chi_pubhealth/202101200900/x/board_of_health"
#
#
# def test_status():
#     assert parsed_items[0]["status"] == TENTATIVE
#
#
# def test_links():
#     assert parsed_items[0]["links"] == []
#
#
# @pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
#
#
@pytest.mark.parametrize("item", parsed_items)
def test_classification(item):
    assert item["classification"] == BOARD

#
# @pytest.mark.parametrize("item", parsed_items)
# def test_location(item):
#     assert item["location"] == {
#         "name": "2nd Floor Board Room, DePaul Center",
#         "address": "333 S State St, Chicago, IL 60604",
#     }
#
#
# @pytest.mark.parametrize("item", parsed_items)
# def test_source(item):
#     assert item["source"] == test_response.url
