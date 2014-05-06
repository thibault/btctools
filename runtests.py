import os
import sys
import nose


PROJECT_ROOT = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'btctools'))

argv = sys.argv
nose_args = argv + ['--nocapture']
result = nose.main(argv=nose_args)
