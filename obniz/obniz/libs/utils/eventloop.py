import asyncio
import warnings


def get_event_loop():
    """Return a usable event loop on all supported Python versions.

    Prefers the running loop. Otherwise returns the loop registered for the
    current thread, creating and registering a new one when none exists —
    Python 3.14 removed the implicit creation from asyncio.get_event_loop(),
    and 3.10-3.13 emit DeprecationWarning for it.
    """
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        pass

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("event loop is closed")
        return loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def ensure_future(coro):
    """Schedule a coroutine on the loop returned by get_event_loop()."""
    return asyncio.ensure_future(coro, loop=get_event_loop())
