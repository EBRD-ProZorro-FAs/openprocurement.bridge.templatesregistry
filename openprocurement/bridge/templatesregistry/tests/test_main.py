# -*- coding: utf-8 -*-
import unittest

from openprocurement.bridge.templatesregistry.tests import test_handlers, test_utils, test_template_downloader


def suite():
    tests = unittest.TestSuite()
    tests.addTest(test_handlers.suite())
    tests.addTest(test_utils.suite())
    tests.addTest(test_template_downloader.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
