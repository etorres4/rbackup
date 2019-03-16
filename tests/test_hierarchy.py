import doctest

# ========== Constants ==========
TESTING_MODULE = "rbackup.hierarchy.hierarchy"


# ========== Functions ==========
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TESTING_MODULE))
    return tests
