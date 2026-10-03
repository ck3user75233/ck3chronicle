"""Write native research evidence without materializing the whole JSON payload."""
import hashlib
import json


def inspect_bundle(folder):
    """Authenticate retained data only. Never load a parser or learner implementation."""
    from pathlib import Path
    root = Path(folder).resolve()
    manifest = json.loads((root / 'manifest.json').read_bytes())
    for name, expected in manifest['hashes'].items():
        path = (root / name).resolve()
        if path.parent != root:
            raise ValueError('invalid candidate payload path')
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != expected:
            raise ValueError('candidate data hash mismatch: ' + name)
    model = json.loads((root / 'empirical_template_model.json').read_bytes())
    return dict(manifest=manifest, model=model)


def main():
    import argparse
    p=argparse.ArgumentParser(description='Authenticate and inspect candidate data without executing its code.')
    p.add_argument('--bundle',required=True)
    a=p.parse_args();data=inspect_bundle(a.bundle)
    print(json.dumps(dict(manifest=data['manifest'],model_revision=data['model']['revision_id'],
        summary=data['model']['summary']),indent=2))


def write_native_evidence(path, evidence):
    """Preserve every value; bound encoding memory to one contextual record.

    Native occurrence arrays dominate large research bundles. Compact encoding
    per record uses Python's C JSON encoder without allocating another complete
    corpus-sized string and byte buffer. The bundle reader accepts ordinary JSON.
    """
    digest = hashlib.sha256()
    with path.open('wb') as stream:
        def emit(payload):
            stream.write(payload)
            digest.update(payload)

        def encoded(value):
            return json.dumps(value, ensure_ascii=True, sort_keys=True,
                              separators=(',', ':')).encode('ascii')

        emit(b'{')
        for index, key in enumerate(sorted(evidence)):
            if index:
                emit(b',')
            emit(encoded(key)); emit(b':')
            if key == 'records':
                emit(b'[')
                for position, record in enumerate(evidence[key]):
                    if position:
                        emit(b',')
                    emit(encoded(record))
                emit(b']')
            else:
                emit(encoded(evidence[key]))
        emit(b'}\n')
    return digest.hexdigest()


def native_evidence_rows(path, *, retain_occurrences=False):
    """Stream ordinary JSON evidence, retaining one occurrence per row by default.

    Serialization whitespace is not a schema boundary. Decode one contextual
    record at a time, including its occurrence list, rather than the whole corpus.
    Counts include every occurrence. Use retain_occurrences for log provenance;
    the default must not be used to count independent supporting logs.
    """
    with path.open(encoding="utf-8") as stream:
        decoder = json.JSONDecoder()
        buffer, cursor, eof = '', 0, False

        def fill(size=1024 * 1024):
            nonlocal buffer, cursor, eof
            chunk = stream.read(size)
            buffer, cursor = buffer[cursor:] + chunk, 0
            eof = not chunk

        def peek():
            nonlocal cursor
            while True:
                while cursor < len(buffer) and buffer[cursor].isspace():
                    cursor += 1
                if cursor < len(buffer):
                    return buffer[cursor]
                if eof:
                    raise ValueError('truncated native evidence JSON')
                fill()

        def take(expected):
            nonlocal cursor
            if peek() != expected:
                raise ValueError('invalid native evidence JSON boundary')
            cursor += 1

        def value():
            nonlocal cursor
            peek()
            while True:
                try:
                    result, end = decoder.raw_decode(buffer, cursor)
                except json.JSONDecodeError:
                    if eof:
                        raise
                    fill(max(1024 * 1024, len(buffer) - cursor))
                    continue
                if end == len(buffer) and not eof:
                    fill()
                    continue
                cursor = end
                return result

        take('{')
        while peek() != '}':
            key = value()
            take(':')
            if key == 'records':
                take('[')
                while peek() != ']':
                    row = value()
                    occurrences = len(row['native_occurrences'])
                    if not retain_occurrences:
                        row['native_occurrences'] = row['native_occurrences'][:1]
                    yield row, occurrences
                    if peek() != ']':
                        take(',')
                take(']')
                return
            value()
            if peek() != '}':
                take(',')
        raise ValueError('missing native evidence records')



if __name__ == "__main__":
    main()
