from __future__ import annotations

from app.voice.audio_sink_player import (
    _SINK_DRAIN_RETRY_MAX_MS,
    _SINK_DRAIN_RETRY_MIN_MS,
    _drain_retry_delay_ms,
    _sink_still_buffering,
)


class _FakeSinkState:
    def __init__(self, name: str) -> None:
        self.name = name


class _FakeSink:
    def __init__(self, state_name: str, buffer_size: int, bytes_free: int) -> None:
        self._state_name = state_name
        self._buffer_size = buffer_size
        self._bytes_free = bytes_free

    def state(self) -> _FakeSinkState:
        return _FakeSinkState(self._state_name)

    def bufferSize(self) -> int:
        return self._buffer_size

    def bytesFree(self) -> int:
        return self._bytes_free


def test_drain_retry_delay_waits_for_remaining_audio() -> None:
    assert _drain_retry_delay_ms(100, 4100) == _SINK_DRAIN_RETRY_MAX_MS
    assert _drain_retry_delay_ms(3900, 4100) == 100


def test_drain_retry_delay_finishes_when_audio_elapsed() -> None:
    assert _drain_retry_delay_ms(4000, 4100) is None
    assert _drain_retry_delay_ms(5000, 4100) is None


def test_drain_retry_delay_clamps_to_bounds() -> None:
    assert _drain_retry_delay_ms(0, 120) == _SINK_DRAIN_RETRY_MIN_MS
    assert _drain_retry_delay_ms(0, 10000) == _SINK_DRAIN_RETRY_MAX_MS


def test_drain_retry_delay_handles_unknown_duration() -> None:
    assert _drain_retry_delay_ms(0, 0) is None
    assert _drain_retry_delay_ms(100, -1) is None


def test_sink_still_buffering_false_when_no_sink() -> None:
    assert not _sink_still_buffering(None)


def test_sink_still_buffering_true_for_active_buffer() -> None:
    sink = _FakeSink("ActiveState", buffer_size=4096, bytes_free=0)

    assert _sink_still_buffering(sink)


def test_sink_still_buffering_false_when_idle_or_drained() -> None:
    assert not _sink_still_buffering(_FakeSink("IdleState", 4096, 0))
    assert not _sink_still_buffering(_FakeSink("StoppedState", 4096, 0))
    assert not _sink_still_buffering(_FakeSink("ActiveState", 4096, 4096))


def test_sink_still_buffering_conservative_when_unknown() -> None:
    assert _sink_still_buffering(_FakeSink("SuspendedState", 0, 0))
