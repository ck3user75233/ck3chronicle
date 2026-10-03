"""Inference views using the shared declaration matcher."""
from .matching_defaults import RULES
DECLARATIONS = RULES.constructions
recognize = RULES.recognize
field_ranges = RULES.field_ranges
capture_range = RULES.capture_range

def comparison_ranges(source,text):
    found=recognize(source,text)
    return [found['regions'][name]['span'] for name in DECLARATIONS[found['id']]['comparison_regions']] if found else [[0,len(text.encode('utf-8','surrogateescape'))]]


def identity(source,text):
    found=recognize(source,text)
    return found['id'] if found else None
