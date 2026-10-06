"""Named investigation definitions; no database, model loading or rendering."""
from .query import InvestigationQuery, QueryError, refinement_clauses

SYNTAX_PACKAGE = '68f1ae5db205ab46afef9c4d'
SYNTAX_MODEL = 'f5cde2616f35d563118d3d32'
ASSIGNMENT_REASON = "Trigger is simple assign, but used a symbol other than '=' in the middle"
SYNTAX_ROWS = (
    ('ca6575c8898718edafb168ca', 'pdx_persistent_reader.cpp', 'Unexpected equals token'),
    ('575c64f8a3b6e211b735c3ba', 'pdx_persistent_reader.cpp', 'Malformed opening-brace token'),
    ('0b2804538785c71278ea37e7', 'jomini_script_system.cpp', 'Wrong simple-assignment operator'),
    ('d3e23fc8aad5883970f02964', 'localization_reader.cpp', 'Unexpected localization s'),
    ('3ee5943a9d6e695efc7f6f1c', 'localization_reader.cpp', 'Unexpected localization comma'),
    ('437a7f59c0736bb3b46b6e2f', 'localization_reader.cpp', 'Missing quoted localization value'),
    ('7657bd29deb139cb27588ed9', 'pdx_data_localize.cpp', 'Unterminated localization substitution'),
    ('14f626fdc756e7881168c8b0', 'pdx_data_localize.cpp', 'Required localization quote escaping missing'),
    ('0d942a44097fd983668bacfd', 'pdx_data_statementparser.cpp', 'Trailing data-statement characters'),
)
PRESETS = {
    'hotspots': ('Script/file hotspots', 'Stored diagnostics with an identifiable script/file reference; rank occurrences and distinct exact records by emitter, referenced path and candidate association separately.'),
    'frequent': ('Frequent diagnostics', 'Exact diagnostic records ranked by selected-Run occurrence count within the effective scope.'),
    'syntax': ('Syntax-related diagnostics', 'OR of the nine verified package/model-scoped syntax selectors; both template and provisional records remain eligible.'),
    'new': ('Newly observed diagnostics', 'Positive exact identities absent from every successfully read included predecessor; newness is relative to this window.'),
    'symbol': ('Symbol/template investigation', 'An explicit template reference, template-text condition or typed binding selects exact diagnostics without merging identities.'),
}


def syntax_selectors():
    result = []
    for template, family, _ in SYNTAX_ROWS:
        branch = {'templates': [{'template_id': template, 'model_revision': SYNTAX_MODEL}],
                  'source_families': [family]}
        if template == '0b2804538785c71278ea37e7':
            branch['bindings'] = [{'region': 'body', 'slot_id': 's1', 'type': 'REASON',
                                   'present': True, 'value': ASSIGNMENT_REASON}]
        result.append(branch)
    return result


def validate_package(preset, package_id):
    """Check stored lineage after package-independent input validation."""
    if preset == 'syntax' and package_id != SYNTAX_PACKAGE:
        raise QueryError(f'syntax preset unavailable for package {package_id}; verified package is {SYNTAX_PACKAGE}, model {SYNTAX_MODEL}')


def build_query(preset, value, *, limit=None, historical_limit=None, no_history=False):
    """Validate and compose inputs before requesting any stored Run metadata."""
    query = InvestigationQuery.from_dict(value or {}).to_dict()
    refinement = query['refinement']
    base = {'hotspots': {'has_source_reference': True},
            'new': {'newly_observed': True},
            'syntax': {'selectors': syntax_selectors()}}.get(preset)
    if base:
        refinement.setdefault('all', []).append(base)
    elif preset == 'symbol':
        fields = {'templates', 'template_text', 'template_exact', 'bindings'}
        if not any(fields & c.keys() or (
                c.get('selectors') and all(fields & b.keys() for b in c['selectors']))
                for c in refinement_clauses(refinement)):
            raise QueryError('symbol requires templates, template_text, template_exact or typed bindings in --query')
    elif preset not in (None, 'frequent'):
        raise QueryError(f'unknown preset: {preset}')
    if no_history:
        if query['analytics'].get('trailing_runs') is not None or any('newly_observed' in c for c in refinement_clauses(refinement)):
            raise QueryError('--no-history contradicts trailing_runs/newly_observed; remove the history-dependent option')
        query['analytics'] = {'history': False, 'include_absent': False}
    query['display']['limit'] = limit if limit is not None else query['display']['limit']
    query['display']['historical_limit'] = historical_limit if historical_limit is not None else query['display']['historical_limit']
    if query['display']['limit'] is None:
        query['display']['limit'] = 50
    if query['display']['historical_limit'] is None:
        query['display']['historical_limit'] = 20
    if not query['purpose']:
        query['purpose'] = PRESETS[preset][1] if preset else 'Custom stored diagnostic investigation'
    return InvestigationQuery.from_dict(query)


def preset_description(preset):
    result = {'name': preset or 'custom', 'title': PRESETS[preset][0] if preset else 'Custom investigation',
              'condition': PRESETS[preset][1] if preset else 'The explicit structured query supplies every condition.'}
    if preset == 'syntax':
        result.update(package_id=SYNTAX_PACKAGE, model_revision=SYNTAX_MODEL,
            selectors=syntax_selectors(),
            evidence=[{'template_id': t, 'source_family': f, 'description': d} for t, f, d in SYNTAX_ROWS],
            exclusions='Excludes generic trigger errors, failed context switches, context-dependent named tokens, missing participants/values and unverified brace-balance claims. No exhaustive syntax taxonomy or causal inference.',
            research='docs/CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff')
    return result
