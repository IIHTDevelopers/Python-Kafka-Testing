import unittest

def print_test_summary(test_result):
    total_tests = test_result.testsRun
    failed_tests = len(test_result.failures)
    errors = len(test_result.errors)
    skipped_tests = len(test_result.skipped)

    print(f"\nRan {total_tests} tests in {test_result.time:.2f}s")
    if failed_tests:
        print(f"Failed tests: {failed_tests}")
        for failure in test_result.failures:
            print(f"  {failure[0].__class__.__name__}.{failure[0]._testMethodName}: {failure[1]}")
    if errors:
        print(f"Errors: {errors}")
        for error in test_result.errors:
            print(f"  {error[0].__class__.__name__}.{error[0]._testMethodName}: {error[1]}")
    if skipped_tests:
        print(f"Skipped tests: {skipped_tests}")
        for skipped in test_result.skipped:
            print(f"  {skipped[0].__class__.__name__}.{skipped[0]._testMethodName}: {skipped[1]}")

if __name__ == '__main__':
    total_tests = 0
    total_pass = 0
    total_fail = 0

    loader = unittest.TestLoader()
    suite = loader.discover('test', pattern='test_*.py')
    test_result = unittest.TestResult()
    suite.run(test_result)

    for test_file in suite:
        print(f"\nTest File: {test_file._tests[0].__class__.__module__}")
        print_test_summary(test_result)
        total_tests += test_result.testsRun
        total_fail += len(test_result.failures) + len(test_result.errors)
        total_pass += test_result.testsRun - (len(test_result.failures) + len(test_result.errors))
        test_result = unittest.TestResult()

    print(f"\nOverall Summary:")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {total_pass}")
    print(f"Failed: {total_fail}")
