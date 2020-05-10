from datetime import timedelta

from blueprints.hubstaff import add_to_cache, check_and_retrieve_from_cache
from utils_for_tests import get_yesterday_start_time, get_mock_table_data


def test_add_to_cache_successful():
    start_time = get_yesterday_start_time()
    start_time = start_time - timedelta(100)
    table_header, table_rows = get_mock_table_data()
    add_to_cache(start_time.isoformat(), table_header, table_rows)

    returned_table_header, returned_table_rows = check_and_retrieve_from_cache(
        start_time.isoformat()
    )

    assert table_header == returned_table_header
    assert table_rows == returned_table_rows


def test_check_cache_for_non_existing_date():
    start_time = get_yesterday_start_time()
    start_time = start_time - timedelta(200)

    returned_table_header, returned_table_rows = check_and_retrieve_from_cache(
        start_time.isoformat()
    )

    assert not returned_table_header
    assert not returned_table_rows
