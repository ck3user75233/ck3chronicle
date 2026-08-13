"""Literal foundation evidence and independently frozen expected hashes.

Oracle provenance
-----------------
The byte strings below were written for the reboot contract, not copied from
the implementation or inherited fixtures. SHA-256 and bundle constants were
calculated independently with Windows cryptography APIs before these tests were
written. Production hashing, manifest, and parser functions were not used to
generate the expected values.
"""
from __future__ import annotations

from pathlib import Path


SIX_LOG_BYTES: dict[str, bytes] = {
    "error.log": b"[01:02:03][E][source.cpp:7]: Error one\r\ncontinued\n",
    "debug.log": b"debug\x00evidence\n",
    "game.log": b"game\r\n",
    "database_conflicts.log": b"db-conflicts\n",
    "setup.log": b"setup\n",
    "text.log": b"text\n",
}

SIX_LOG_SHA256 = {
    "error.log": "e499d59d44286784e340fdfd52aced633876ddd96735e925c2791d4b8c4d8848",
    "debug.log": "d3f7ea74bd08336aeaee0cf3306b0796822d959b4526bb4d157e3ba0a354c3f9",
    "game.log": "3cc29a7afa1d4edc37a1d828216eee1a6ba9d9d556f2a7838e79b83152deaabe",
    "database_conflicts.log": "dd89b74b0f624b9cbe4ed02b77044970eb45d279d331d851a931c1ea80b3bb55",
    "setup.log": "9752eb62a6845a78a9e2eaeb4a6eb2d93a1b654ee8665f71d516cfaca3e7cf57",
    "text.log": "b9e68e1bea3e5b19ca6b2f98b73a54b73daafaa250484902e09982e07a12e733",
}

SIX_LOG_BUNDLE_SHA256 = (
    "9aa4819f147e9db5a15a33dadfcb79a87efc4ac284b3e1de545bedc80399e217"
)

LEXICAL_ERROR_BYTES = (
    b"startup preamble\r\n"
    b"[12:00:00][E][first.cpp:10]: First semantic 'alpha'\r\n"
    b"detail A\n"
    b"[12:00:01][W][second.cpp:20]: Second semantic"
)

LEXICAL_BLOCK_ORACLE = (
    {
        "name": "preamble",
        "start_line": 1,
        "end_line": 1,
        "bytes": 18,
        "raw_sha256": "847aad5f607aa7ac97cc98ed0d8151dfa33df2b92c6ebf738069fdc05181f979",
        "source_block_id": "16601119f94b471b79646f2f387e0a0ad993234ed3a871a96c8e8a8b3a3383f2",
        "timestamp": None,
        "level": None,
        "source_family": "<preamble>",
    },
    {
        "name": "first",
        "start_line": 2,
        "end_line": 3,
        "bytes": 62,
        "raw_sha256": "6c46a433bde88137376c0b2291eec7b422de8ed77077a9b99dd82cf8356b0190",
        "source_block_id": "c08d17bc8c5d30601ab676403902b33428122b03424a77129dd2e9ab0902f5e3",
        "timestamp": "12:00:00",
        "level": "E",
        "source_family": "first.cpp",
    },
    {
        "name": "second",
        "start_line": 4,
        "end_line": 4,
        "bytes": 45,
        "raw_sha256": "515b9ddc73eb01194e2ecc489c76dfe6a9922ca0716d5d9fe78b2fb85c8f257a",
        "source_block_id": "ccacbae02a4aad3a1e13f21088989c260447b1700a46f3bfb4cd90e6e1d7495c",
        "timestamp": "12:00:01",
        "level": "W",
        "source_family": "second.cpp",
    },
)


def write_logs(root: Path, files: dict[str, bytes] | None = None) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for name, data in (files or SIX_LOG_BYTES).items():
        (root / name).write_bytes(data)
