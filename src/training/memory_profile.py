import logging
from typing import Any, Callable

from kedro.io import AbstractTransformer
from memory_profiler import memory_usage


def _normalise_mem_usage(mem_usage):
    # memory_profiler < 0.56.0 returns list instead of float
    return mem_usage[0] if isinstance(mem_usage, (list, tuple)) else mem_usage


class ProfileMemoryTransformer(AbstractTransformer):
    """A transformer that logs the maximum memory consumption during load and save calls
    """

    @property
    def _logger(self):
        return logging.getLogger(self.__class__.__name__)

    def load(self, data_set_name: str, load: Callable[[], Any]) -> Any:
        mem_usage, data = memory_usage(
            (load, [], {}),
            interval=0.1,
            max_usage=True,
            retval=True,
            include_children=True,
        )
        # memory_profiler < 0.56.0 returns list instead of float
        mem_usage = _normalise_mem_usage(mem_usage)

        self._logger.info(
            "Loading %s consumed %2.2fMiB memory at peak time", data_set_name, mem_usage
        )
        return data

    def save(self, data_set_name: str, save: Callable[[Any], None], data: Any) -> None:
        mem_usage = memory_usage(
            (save, [data], {}),
            interval=0.1,
            max_usage=True,
            retval=False,
            include_children=True,
        )
        mem_usage = _normalise_mem_usage(mem_usage)

        self._logger.info(
            "Saving %s consumed %2.2fMiB memory at peak time", data_set_name, mem_usage
        )
