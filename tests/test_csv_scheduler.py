import asyncio
from datetime import datetime

from app.scheduler.csv_scheduler import CSVImportScheduler


def test_start_does_not_create_multiple_running_tasks():
    async def run_test():
        scheduler = CSVImportScheduler(csv_path="associates.csv", import_time="09:00")

        scheduler.start()
        first_task = scheduler._task
        scheduler.start()

        assert scheduler._task is first_task

        await scheduler.stop()

    asyncio.run(run_test())


def test_seconds_until_next_run_uses_same_day_when_time_is_ahead():
    now = datetime(2026, 7, 18, 8, 30, 0)
    scheduler = CSVImportScheduler(csv_path="associates.csv", import_time="09:00")

    seconds = scheduler._seconds_until_next_run(now=now)

    assert seconds == 30 * 60


def test_seconds_until_next_run_uses_next_day_when_time_has_passed():
    now = datetime(2026, 7, 18, 9, 30, 0)
    scheduler = CSVImportScheduler(csv_path="associates.csv", import_time="09:00")

    seconds = scheduler._seconds_until_next_run(now=now)

    assert seconds == 23 * 60 * 60 + 30 * 60
