import pytest

from cyclegraph import parse_dates
from datetime import datetime

def test_parse_dates_raises_ValueError_with_invalid_start_date():
  with pytest.raises(ValueError):
    parse_dates('notADate', '2022-06-08')

def test_parse_dates_raises_ValueError_with_invalid_end_date():
  with pytest.raises(ValueError):
    parse_dates('2022-04-15', 'notADate')

def test_parse_dates_can_parse_iso_format_dates():
  start_date, end_date = parse_dates('2022-04-15', '2022-06-08')
  assert start_date == datetime.fromisoformat('2022-04-15')
  assert end_date == datetime.fromisoformat('2022-06-08')
