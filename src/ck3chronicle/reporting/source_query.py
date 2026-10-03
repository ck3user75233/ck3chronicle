"""Source selection validation, shared by standalone and composed searches."""
from pathlib import PurePosixPath

from .query import QueryError, _integer, _list, _object, _string, validate_text


SOURCE_FIELDS = {'roots', 'members', 'files', 'referenced_paths', 'directories',
                 'recursive', 'extensions', 'include', 'exclude', 'filename',
                 'relative_path', 'filename_globs', 'path_globs', 'case_sensitive',
                 'content', 'reference_mode'}


def validate_source(value):
    _object(value, SOURCE_FIELDS, 'source')
    if not value:
        raise QueryError('empty source selection')
    for key, selection in value.items():
        if key in {'recursive', 'case_sensitive'}:
            if type(selection) is not bool:
                raise QueryError(f'{key} must be boolean')
        elif key == 'reference_mode':
            if selection not in {'relative', 'basename'}:
                raise QueryError('reference_mode must be relative or basename')
        elif key in {'filename', 'relative_path'}:
            _object(selection, {'exact', 'text'}, key)
            if not selection:
                raise QueryError(f'empty {key} predicate')
            if 'exact' in selection:
                _list(selection['exact'], key)
                for part in selection['exact']:
                    _string(part, key)
            if 'text' in selection:
                validate_text(selection['text'])
        elif key == 'content':
            validate_text(selection)
        else:
            _list(selection, key)
            for part in selection:
                if key == 'members':
                    _object(part, {'load_order', 'name', 'path', 'root_ID', 'stable_id', 'descriptor_path'}, 'member')
                    if not part:
                        raise QueryError('empty member selector')
                    for field, item in part.items():
                        if field == 'load_order':
                            _integer(item, field)
                        elif item is not None:
                            _string(item, field)
                else:
                    _string(part, key)
                    if key == 'directories':
                        path = PurePosixPath(part.replace('\\', '/'))
                        if path.is_absolute() or '..' in path.parts or ':' in part:
                            raise QueryError('directories must stay relative to the selected roots')

