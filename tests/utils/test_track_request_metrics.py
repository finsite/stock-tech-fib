from app.utils.track_request_metrics import track_request_metrics


def test_track_request_success():
    track_request_metrics("AAPL", 10, 60.0, success=True)


def test_track_request_failure():
    track_request_metrics("AAPL", 10, 60.0, success=False)
