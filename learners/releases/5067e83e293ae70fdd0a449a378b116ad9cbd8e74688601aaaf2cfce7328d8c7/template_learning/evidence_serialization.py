"""Write native research evidence without materializing the whole JSON payload."""
import hashlib
import json


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
