from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers.economic_group import router as economic_group_router
from app.core.config import settings
from app.core.database import init_database
from app.scheduler.csv_importer import CSVImporter
from app.scheduler.csv_scheduler import CSVImportScheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    csv_importer = CSVImporter()
    await csv_importer.import_csv(settings.csv_import_path)

    csv_scheduler = CSVImportScheduler(
        csv_path=settings.csv_import_path,
        import_time=settings.csv_import_time,
    )
    csv_scheduler.start()

    try:
        yield
    finally:
        await csv_scheduler.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(economic_group_router)
