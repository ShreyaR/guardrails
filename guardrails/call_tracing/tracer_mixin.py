"""tracer_mixin.py.

This file defines our preferred tracer interface. It has a side effect
of acting as a 'noop' when we want to benchmark performance of a tracer.
"""

import os
from typing import Iterator

from guardrails.call_tracing.trace_entry import GuardTraceEntry
from guardrails.classes.validation.validator_logs import ValidatorLogs


class TracerMixin:
    """The pads out the methods but is otherwise a noop."""

    def __init__(self, log_path: os.PathLike, read_mode: bool):
        self.db = None

    def log(self, *args, **kwargs):
        pass

    def log_entry(self, guard_log_entry: GuardTraceEntry):
        pass

    def log_validator(self, vlog: ValidatorLogs):
        pass

    def tail_logs(
        self,
        start_offset_idx: int = 0,
        follow: bool = False,
    ) -> Iterator[GuardTraceEntry]:
        yield from []
