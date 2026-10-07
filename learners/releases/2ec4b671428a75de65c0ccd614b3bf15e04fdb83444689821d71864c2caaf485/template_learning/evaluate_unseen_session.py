"""Launch candidate evaluation with an explicit retained learner release."""
import argparse
from pathlib import Path
from template_learning.learner_loader import catalog_root, resolve_release, launch


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--learner-root',type=Path,default=catalog_root())
    p.add_argument('--learner-release',required=True)
    p.add_argument('--bundle',type=Path,required=True)
    p.add_argument('--log',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--receipt')
    a=p.parse_args()
    folder,pin=resolve_release(a.learner_root,a.learner_release)
    launch(folder,pin,'evaluate',['--bundle',str(a.bundle.resolve()),'--log',str(a.log.resolve()),
        '--output',str(a.output.resolve())],receipt=a.receipt)


if __name__=='__main__':
    main()
