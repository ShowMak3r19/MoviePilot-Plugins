"""SaDiscoverSub 插件的纯逻辑测试。"""

import time

from app.plugins.sadiscoversub import SaDiscoverSub


def test_parse_season_from_chinese_title() -> None:
    """从中文季标题解析季号。"""
    assert SaDiscoverSub._parse_season("庆余年 第二季", {}) == 2


def test_parse_season_from_english_title() -> None:
    """从英文季标题解析季号。"""
    assert SaDiscoverSub._parse_season("某剧 Season 2", {}) == 2
    assert SaDiscoverSub._parse_season("某剧 S03", {}) == 3


def test_parse_season_without_season() -> None:
    """电影标题不应被误判为剧集季号。"""
    assert SaDiscoverSub._parse_season("人生若如初见", {}) is None


def test_parse_season_falls_back_to_item_fields() -> None:
    """标题无法解析时回退到条目季字段。"""
    assert SaDiscoverSub._parse_season("某剧", {"ParentIndexNumber": 4}) == 4


def test_duplicate_window_uses_media_identity() -> None:
    """同一媒体身份在去重窗口内应被识别为重复。"""
    plugin = object.__new__(SaDiscoverSub)
    plugin._dedupe_seconds = 60
    plugin._history = [{"key": "themoviedb:206219:", "ts": time.time()}]

    assert plugin._is_duplicate("themoviedb:206219:")
    assert not plugin._is_duplicate("themoviedb:206220:")


def test_duplicate_window_expires() -> None:
    """超过去重窗口后应允许再次处理。"""
    plugin = object.__new__(SaDiscoverSub)
    plugin._dedupe_seconds = 1
    plugin._history = [{"key": "themoviedb:206219:", "ts": time.time() - 5}]

    assert not plugin._is_duplicate("themoviedb:206219:")
