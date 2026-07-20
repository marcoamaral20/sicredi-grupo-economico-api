import asyncio
from contextlib import suppress
from datetime import datetime, timedelta
from time import perf_counter

from app.core.logging import logger
from app.scheduler.csv_importer import CSVImporter


class CSVImportScheduler:
    def __init__(
        self,
        csv_path: str,
        import_time: str,
        importer: CSVImporter | None = None,
    ):
        self.csv_path = csv_path
        self.import_time = import_time
        self.importer = importer or CSVImporter()
        self._task: asyncio.Task | None = None

    def start(self) -> None:
        if self._task and not self._task.done():
            return

        self._task = asyncio.create_task(self._run_forever())

    async def stop(self) -> None:
        if self._task is None:
            return

        logger.info("Stopping CSV scheduler.")
        self._task.cancel()

        with suppress(asyncio.CancelledError):
            await self._task

        logger.info("CSV scheduler stopped.")

    async def _run_forever(self) -> None:
        logger.info(
            "CSV scheduler started. csv_path=%s import_time=%s",
            self.csv_path,
            self.import_time,
        )

        while True:
            now = datetime.now()
            delay = self._seconds_until_next_run(now=now)
            next_execution = now + timedelta(seconds=delay)

            logger.info(
                "Next CSV import scheduled for %s",
                next_execution.isoformat(timespec="seconds"),
            )

            await asyncio.sleep(delay)
            await self._execute_import()

    def _seconds_until_next_run(self, now: datetime) -> float:
        target_time = datetime.strptime(self.import_time, "%H:%M").time()
        next_run = datetime.combine(now.date(), target_time)

        if next_run <= now:
            next_run = next_run + timedelta(days=1)

        return (next_run - now).total_seconds()

    async def _execute_import(self) -> None:
        started_at = perf_counter()
        logger.info("Starting CSV import. csv_path=%s", self.csv_path)

        try:
            await self.importer.import_csv(self.csv_path)
        except Exception:
            duration = perf_counter() - started_at
            logger.exception(
                "CSV import failed. duration_seconds=%.2f",
                duration,
            )
            return

        duration = perf_counter() - started_at
        logger.info(
            "CSV import finished successfully. duration_seconds=%.2f",
            duration,
        )
