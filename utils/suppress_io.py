import contextlib
from contextlib import contextmanager
import sys, os
import io
from contextlib import redirect_stdout


def capture_stdout(function_call):
    f = io.StringIO()
    with redirect_stdout(f):
        function_call()
    out = f.getvalue()
    return out


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

@contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stderr = old_stderr