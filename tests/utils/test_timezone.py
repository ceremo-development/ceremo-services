import pytest
from datetime import datetime
from app.utils.timezone import now_ist


def test_now_ist():
    result = now_ist()
    assert isinstance(result, datetime)
    assert result.tzinfo is not None
    assert str(result.tzinfo) == "Asia/Kolkata"
