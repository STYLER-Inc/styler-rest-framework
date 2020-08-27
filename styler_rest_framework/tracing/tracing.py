
import logging

from aiohttp import web
from opencensus.common.transports.async_ import AsyncTransport
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
from opencensus.trace import attributes_helper
from opencensus.trace.propagation import google_cloud_format
import opencensus.trace.tracer


HTTP_HOST = attributes_helper.COMMON_ATTRIBUTES['HTTP_HOST']
HTTP_METHOD = attributes_helper.COMMON_ATTRIBUTES['HTTP_METHOD']
HTTP_PATH = attributes_helper.COMMON_ATTRIBUTES['HTTP_PATH']
HTTP_ROUTE = attributes_helper.COMMON_ATTRIBUTES['HTTP_ROUTE']
HTTP_URL = attributes_helper.COMMON_ATTRIBUTES['HTTP_URL']
HTTP_STATUS_CODE = attributes_helper.COMMON_ATTRIBUTES['HTTP_STATUS_CODE']


def initialize_tracer(project_id, context, propagator):
    exporter = stackdriver_exporter.StackdriverExporter(
        project_id=project_id,
        transport=AsyncTransport
    )
    tracer = opencensus.trace.tracer.Tracer(
        span_context=context,
        exporter=exporter,
        propagator=propagator,
        sampler=opencensus.trace.tracer.samplers.AlwaysOnSampler()
    )

    return tracer


def trace_middleware(project_id):
    @web.middleware
    async def middleware(request, handler):
        if handler.__name__ == 'health_check':
            return await handler(request)
        span = None
        tracer = None
        try:
            propagator = google_cloud_format.GoogleCloudFormatPropagator()
            span_context = propagator.from_headers(request.headers)
            tracer = initialize_tracer(project_id, span_context, propagator)
            span = tracer.start_span()
            span.name = handler.__name__
            tracer.add_attribute_to_current_span(
                HTTP_HOST, request.host
            )
            tracer.add_attribute_to_current_span(
                HTTP_METHOD, request.method
            )
            tracer.add_attribute_to_current_span(
                HTTP_PATH, request.path
            )
            tracer.add_attribute_to_current_span(
                HTTP_URL, str(request.url)
            )
            request['trace_header'] = propagator.to_headers(span_context)
        except:  # NOQA
            logging.exception('Could not initialize the tracer')

        try:
            response = await handler(request)
            if tracer:
                tracer.add_attribute_to_current_span(
                    HTTP_STATUS_CODE, response.status
                )
            return response
        finally:
            if tracer:
                tracer.end_span()
    return middleware


def config_tracer(app, project_id):
    app.middlewares.append(trace_middleware(project_id))
