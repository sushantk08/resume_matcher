"""
Unified test runner for Resume Matcher.
"""

import unittest
import sys
import time


def run_all_tests():
    print("=" * 70)
    print("🧪 Running Full Test Suite for Resume / Job Description Matcher")
    print("=" * 70)

    start_time = time.time()
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    duration = time.time() - start_time
    print("-" * 70)
    print(f"⏱️ Total test duration: {duration:.2f} seconds")
    print(f"📊 Results: {result.testsRun} tests run, {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 70)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()