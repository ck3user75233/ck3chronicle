"""Receive completed watcher JSON without extracting or resolving membership."""
from copy import deepcopy
import re

from .capture_access import capture_time


class PlaysetError(ValueError):
    """Present completed playset is malformed or disagrees with its capture."""


FIELDS = ('schema_version', 'error_log_sha256', 'debug_log_sha256', 'log_pair_id', 'captured_at')
MEMBER_FIELDS = {'load_order', 'name', 'path', 'root_ID', 'stable_id', 'descriptor_path'}


def stored_playset(value, *, error_log_sha256):
    if value is None:
        return dict(playset_captured=False, **dict.fromkeys(FIELDS), members=[])
    try:
        if not isinstance(value, dict) or set(value) != set(FIELDS) | {'members'}:
            raise ValueError('unexpected playset fields')
        if type(value['schema_version']) is not int or value['schema_version'] != 1:
            raise ValueError('unsupported playset format')
        for field in ('error_log_sha256', 'debug_log_sha256'):
            if not isinstance(value[field], str) or not re.fullmatch('[0-9a-f]{64}', value[field]):
                raise ValueError('invalid ' + field)
        if value['error_log_sha256'] != error_log_sha256:
            raise ValueError('playset error-log hash mismatch')
        if value['log_pair_id'] != 'sha256:' + value['error_log_sha256'] + ':' + value['debug_log_sha256']:
            raise ValueError('playset pair identity mismatch')
        capture_time(value['captured_at'])
        if not isinstance(value['members'], list) or not value['members']:
            raise ValueError('ordered playset requires its base member')
        for index, member in enumerate(value['members']):
            if not isinstance(member, dict) or set(member) != MEMBER_FIELDS:
                raise ValueError('unexpected member fields')
            if type(member['load_order']) is not int or member['load_order'] != index:
                raise ValueError('member order must be consecutive from zero')
            if any(not isinstance(member[k], str) for k in ('name', 'path')):
                raise ValueError('member name/path must be strings')
            if any(member[k] is not None and not isinstance(member[k], str)
                   for k in ('root_ID', 'stable_id', 'descriptor_path')):
                raise ValueError('invalid nullable member field')
            if member['root_ID'] not in (None, 'ROOT_GAME', 'ROOT_STEAM', 'ROOT_LOCAL_MODS'):
                raise ValueError('invalid root_ID')
        return dict(deepcopy(value), playset_captured=True)
    except (TypeError, ValueError, KeyError) as exc:
        raise PlaysetError(str(exc)) from exc
