import asyncio

from app.api import main


def test_lifespan_imports_csv_before_starting_scheduler(monkeypatch):
    events = []

    async def fake_init_database():
        events.append("database")

    class FakeCSVImporter:
        async def import_csv(self, csv_path: str):
            events.append(("import", csv_path))

    class FakeCSVImportScheduler:
        def __init__(self, csv_path: str, import_time: str):
            events.append(("scheduler", csv_path, import_time))

        def start(self):
            events.append("start")

        async def stop(self):
            events.append("stop")

    monkeypatch.setattr(main, "init_database", fake_init_database)
    monkeypatch.setattr(main, "CSVImporter", FakeCSVImporter)
    monkeypatch.setattr(main, "CSVImportScheduler", FakeCSVImportScheduler)

    async def run_lifespan():
        async with main.lifespan(main.app):
            events.append("running")

    asyncio.run(run_lifespan())

    assert events == [
        "database",
        ("import", main.settings.csv_import_path),
        ("scheduler", main.settings.csv_import_path, main.settings.csv_import_time),
        "start",
        "running",
        "stop",
    ]
