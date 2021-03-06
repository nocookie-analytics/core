from datetime import datetime
import sentry_sdk
import socket

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_utils.openapi import simplify_operation_ids
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.logger import logger
from app.api.api_v1.api import api_router
from app.api.api_v1.docs import docs_router, description
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=description,
    docs_url=None,
    redoc_url=None,
)


# https://github.com/tiangolo/fastapi/issues/2033#issuecomment-696465251
try:
    proxy_ip = socket.gethostbyname("proxy")
    logger.info("Using proxy middleware with %s", proxy_ip)
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=proxy_ip)
except socket.gaierror:
    logger.info("Not using proxy middleware")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(docs_router)

simplify_operation_ids(app)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        settings.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )


@app.on_event("startup")
@repeat_every(seconds=60 * 15, wait_first=True, logger=logger)
def update_salts() -> None:
    from app import crud
    from app.db.session import SessionLocal

    # this task isn't well-suited for scaling horizontally, but that's a problem for another time
    db = SessionLocal()
    logger.info("Updating salts, current time %s", datetime.now())
    try:
        crud.domain.refresh_domain_salts(db=db)
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db.close()
    logger.info("Finished at %s", datetime.now())


@app.on_event("startup")
@repeat_every(seconds=60 * 60, wait_first=True, logger=logger)
def delete_pending_objects() -> None:
    from app import crud
    from app.db.session import SessionLocal

    db = SessionLocal()

    logger.info("Deleting objects, current time %s", datetime.now())
    try:
        crud.user.delete_pending_users(db=db)
        crud.domain.delete_pending_domains(db=db)
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db.close()
    logger.info("Finished at %s", datetime.now())


@app.middleware("http")
async def add_404_middleware(request: Request, call_next):
    response = await call_next(request)
    path = request["path"]
    if path.startswith(settings.API_V1_STR):
        return response
    if response.status_code == 404:
        return FileResponse("assets/index.html")
    return response


# Static should always be the last mount, otherwise it'll interfere with app routes
app.mount("/", StaticFiles(directory="assets"), name="static")
