"""
Agents module that provides trace functionality
"""
import time
from contextlib import contextmanager


@contextmanager
def trace(operation: str):
    """
    Context manager for tracing operations
    
    Usage:
        with trace("Search_trace"):
            # Your code here
    """
    start_time = time.time()
    
    try:
        print(f"🔍 Starting {operation}...")
        yield
        duration = time.time() - start_time
        print(f"✅ Completed {operation} in {duration:.2f}s")
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Failed {operation} after {duration:.2f}s: {str(e)}")
        raise


def gen_trace_id() -> str:
    """Generate a unique trace ID"""
    import uuid
    return f"trace_{uuid.uuid4().hex[:8]}"
