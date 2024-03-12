import unittest
import coverage
from Silantieva_test import *
from Ustinova_test import *
from Shpak_test import *

cov = coverage.Coverage(omit='*_test.py')
cov.start()
try:
    unittest.main()
except:
    pass
cov.stop()
cov.save()
cov.html_report()
print('done')