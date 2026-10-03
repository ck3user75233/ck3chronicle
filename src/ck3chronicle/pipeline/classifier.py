"""One shared complete assignment, followed by one binding of its selected regions."""
from copy import deepcopy
from functools import lru_cache
import json

from .bindings import bind_captures
from .domain import (ByteSpan, NativeClassification, NativeReview, ResultIntegrityError,
                     SelectedAssignment, SelectedRegion)
from .raw_input import iter_diagnostics, matching_content, native_regions

CLASSIFIER_REVISION = 'ck3-native-message-classifier-v8'


class Classifier:
    def __init__(self, package, *, cache_size: int = 4096):
        self.package = package
        # Instance scope pins package/parser. Cached results contain no occurrence
        # provenance or absolute bindings. Zero disables this cache for verification.
        self._match_content = lru_cache(maxsize=cache_size)(
            lambda content: package.match(json.loads(content)))

    def read_log(self, path):
        return self.package.parse_file(path)

    def classify_raw(self, raw):
        for diagnostic in iter_diagnostics(self.package, raw):
            yield diagnostic if isinstance(diagnostic, NativeReview) else self.classify(diagnostic)

    def classify(self, diagnostic):
        unit = diagnostic.unit
        try:
            result = self._match_content(json.dumps(matching_content(unit), sort_keys=True,
                                                    ensure_ascii=True, separators=(',', ':')))
        except self.package.api.NativeInputError as exc:
            return NativeReview(diagnostic.original, unit, str(exc), exc)
        # Integrity/compatibility/declaration/programming failures propagate.
        try:
            if (result['api_version'] != self.package.manifest['matcher_api_version'] or
                    result['source_family'] != diagnostic.source_family or
                    result['source_tag'] != diagnostic.source_tag):
                raise ResultIntegrityError('matcher result/input correspondence failed')
            assignment = result['assignment']
            selected = None
            reason = None
            if result['status'] == 'no_match' and assignment is None:
                reason = unit['provenance'].get('recovery_limitation') or 'no complete assignment'
            elif result['status'] == 'matched' and assignment is not None:
                if assignment['match_status'] not in {'template', 'provisional'}:
                    raise ResultIntegrityError('unsupported selected match status')
                regions = list(native_regions(unit))
                if [name for name, _ in regions] != [r['name'] for r in assignment['regions']]:
                    raise ResultIntegrityError('selected regions differ from complete input')
                bound = []
                for (name, native), selected_region in zip(regions, assignment['regions']):
                    layout = selected_region['layout']
                    index = selected_region.get('component_index')
                    if (layout['template_id'] != assignment['template_id'] or
                            layout['region'] != ('continuation' if index is not None else name) or
                            (index is not None and name != 'continuation:' + str(index))):
                        raise ResultIntegrityError('selected layout/component correspondence failed')
                    bound.append(SelectedRegion(name, deepcopy(layout),
                        bind_captures(diagnostic.original, native, selected_region['captures']),
                        ByteSpan(*native['provenance']['span']), index))
                selected = SelectedAssignment(assignment['template_id'], assignment['template_status'],
                    assignment['match_status'], tuple(bound), deepcopy(assignment['selection']))
            else:
                raise ResultIntegrityError('inconsistent matcher outcome/assignment')
            return NativeClassification(diagnostic, self.package.manifest['model_revision_id'],
                                        CLASSIFIER_REVISION, selected, reason)
        except (KeyError, TypeError, IndexError) as exc:
            raise ResultIntegrityError('incomplete selected result: ' + str(exc)) from exc
