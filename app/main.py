from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .api_registry import api_registry
from .config import ConfigClass

app = FastAPI(
    title='Notification Service',
    description='Service for notifications',
    docs_url='/v1/api-doc',
    version=ConfigClass.version,
)
app.add_middleware(DBSessionMiddleware, db_url=ConfigClass.SQLALCHEMY_DATABASE_URI)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# API registry
# v1
api_registry(app)


# Implement opentelemetry tracing
def instrument_app(app) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: ConfigClass.APP_NAME}))
    trace.set_tracer_provider(tracer_provider)

    jaeger_exporter = JaegerExporter(agent_host_name='127.0.0.1', agent_port=6831)

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()


if ConfigClass.OPEN_TELEMETRY_ENABLED:
    print('Opentelemetry activated')
    instrument_app(app)
