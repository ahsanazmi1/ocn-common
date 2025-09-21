"""
Central trace utility for OCN ecosystem.

This module provides trace ID generation and management utilities that can be
used across all OCN services to maintain request correlation and observability.
"""

import uuid
from contextvars import ContextVar
from typing import Any, Dict, Optional

# Context variable for storing trace ID in the current execution context
trace_context: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)

# HTTP header name for trace ID propagation
TRACE_HEADER = "x-ocn-trace-id"


def new_trace_id() -> str:
    """
    Generate a new unique trace ID.
    
    Returns:
        A new UUID4 string formatted as a trace ID.
        
    Examples:
        >>> trace_id = new_trace_id()
        >>> len(trace_id) == 36  # UUID4 format
        True
        >>> trace_id.count('-') == 4  # UUID4 has 4 hyphens
        True
    """
    return str(uuid.uuid4())


def ensure_trace_id(ctx: Optional[Dict[str, Any]]) -> str:
    """
    Ensure a trace ID exists in the given context.
    
    If the context contains a valid trace ID (UUID4 format), return it. 
    Otherwise, generate a new one and store it in the context under the 'trace_id' key.
    
    Args:
        ctx: Optional context dictionary that may contain a trace_id
        
    Returns:
        The existing or newly created trace ID.
        
    Examples:
        >>> ctx = {'user_id': '123'}
        >>> trace_id = ensure_trace_id(ctx)
        >>> 'trace_id' in ctx
        True
        >>> trace_id == ctx['trace_id']
        True
        
        >>> existing_trace = '550e8400-e29b-41d4-a716-446655440000'
        >>> ctx = {'trace_id': existing_trace}
        >>> ensure_trace_id(ctx) == existing_trace
        True
    """
    if ctx is None:
        ctx = {}
    
    # Check if we have a valid trace ID (UUID4 format)
    existing_trace_id = ctx.get('trace_id')
    if not existing_trace_id or not _is_valid_trace_id(existing_trace_id):
        ctx['trace_id'] = new_trace_id()
    
    return ctx['trace_id']


def _is_valid_trace_id(trace_id: str) -> bool:
    """
    Check if a string is a valid UUID4 trace ID.
    
    Args:
        trace_id: String to validate
        
    Returns:
        True if valid UUID4 format, False otherwise
    """
    try:
        parsed_uuid = uuid.UUID(trace_id)
        return parsed_uuid.version == 4
    except (ValueError, TypeError):
        return False


def inject_trace_id_ce(envelope: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
    """
    Inject trace ID into a CloudEvent envelope as the subject.
    
    The CloudEvent subject field is used to carry the trace ID for correlation
    across services in the OCN ecosystem.
    
    Args:
        envelope: CloudEvent envelope dictionary
        trace_id: Trace ID to inject as the subject
        
    Returns:
        Modified CloudEvent envelope with trace_id as subject
        
    Examples:
        >>> envelope = {
        ...     'specversion': '1.0',
        ...     'id': 'event-123',
        ...     'source': 'https://example.com',
        ...     'type': 'ocn.orca.decision.v1'
        ... }
        >>> trace_id = 'trace-456'
        >>> result = inject_trace_id_ce(envelope, trace_id)
        >>> result['subject'] == trace_id
        True
        >>> result['id'] == 'event-123'  # Other fields preserved
        True
    """
    # Create a copy to avoid modifying the original
    modified_envelope = envelope.copy()
    modified_envelope['subject'] = trace_id
    return modified_envelope


def get_current_trace_id() -> Optional[str]:
    """
    Get the current trace ID from the context variable.
    
    Returns:
        Current trace ID if set, None otherwise.
        
    Examples:
        >>> # Initially no trace ID
        >>> get_current_trace_id() is None
        True
        
        >>> # Set trace ID in context
        >>> trace_context.set('test-trace-123')
        >>> get_current_trace_id() == 'test-trace-123'
        True
    """
    return trace_context.get()


def set_current_trace_id(trace_id: str) -> None:
    """
    Set the current trace ID in the context variable.
    
    Args:
        trace_id: Trace ID to set in the current context
        
    Examples:
        >>> set_current_trace_id('new-trace-456')
        >>> get_current_trace_id() == 'new-trace-456'
        True
    """
    trace_context.set(trace_id)


def clear_current_trace_id() -> None:
    """
    Clear the current trace ID from the context variable.
    
    Examples:
        >>> set_current_trace_id('trace-789')
        >>> clear_current_trace_id()
        >>> get_current_trace_id() is None
        True
    """
    trace_context.set(None)


def trace_middleware(app):
    """
    FastAPI middleware helper for automatic trace ID management.
    
    This middleware automatically:
    1. Extracts trace ID from the x-ocn-trace-id header
    2. Sets it in the context variable for the request
    3. Ensures every request has a trace ID (generates one if missing)
    
    Args:
        app: FastAPI application instance
        
    Returns:
        The same FastAPI app instance (for chaining)
        
    Examples:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> app = trace_middleware(app)
        >>> # Now all requests will have automatic trace ID management
        
    Usage:
        Add this middleware to your FastAPI app to get automatic trace ID
        propagation across all endpoints. The trace ID will be available
        via get_current_trace_id() in your route handlers.
    """
    from fastapi import Request
    from starlette.middleware.base import BaseHTTPMiddleware
    
    class TraceMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Extract trace ID from header
            trace_id = request.headers.get(TRACE_HEADER)
            
            # If no trace ID in header, generate a new one
            if not trace_id:
                trace_id = new_trace_id()
            
            # Set trace ID in context
            set_current_trace_id(trace_id)
            
            try:
                # Process the request
                response = await call_next(request)
                
                # Add trace ID to response headers for client correlation
                response.headers[TRACE_HEADER] = trace_id
                
                return response
            finally:
                # Clean up context
                clear_current_trace_id()
    
    # Add the middleware to the app
    app.add_middleware(TraceMiddleware)
    
    return app


def create_trace_context(trace_id: Optional[str] = None) -> Dict[str, str]:
    """
    Create a trace context dictionary for logging and correlation.
    
    Args:
        trace_id: Optional trace ID, generates new one if not provided
        
    Returns:
        Dictionary with trace_id and other context information
        
    Examples:
        >>> ctx = create_trace_context()
        >>> 'trace_id' in ctx
        True
        >>> len(ctx['trace_id']) == 36  # UUID4 format
        True
        
        >>> ctx = create_trace_context('custom-trace')
        >>> ctx['trace_id'] == 'custom-trace'
        True
    """
    if trace_id is None:
        trace_id = new_trace_id()
    
    return {
        'trace_id': trace_id,
        'service': 'ocn-common',
        'version': '1.0.0'
    }


def format_trace_log(trace_id: str, message: str, **kwargs) -> str:
    """
    Format a log message with trace ID for structured logging.
    
    Args:
        trace_id: Trace ID for correlation
        message: Log message
        **kwargs: Additional context to include in the log
        
    Returns:
        Formatted log message string
        
    Examples:
        >>> log = format_trace_log('trace-123', 'Processing request', user_id='456')
        >>> 'trace-123' in log
        True
        >>> 'Processing request' in log
        True
        >>> 'user_id=456' in log
        True
    """
    context_parts = [f"{k}={v}" for k, v in kwargs.items()]
    context_str = " ".join(context_parts) if context_parts else ""
    
    return f"[trace_id={trace_id}] {message}" + (f" {context_str}" if context_str else "")
