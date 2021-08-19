"""Unittests for aws2wrap."""
import contextlib
import io
import unittest

import aws2wrap

# pylint: disable=missing-class-docstring,missing-function-docstring


class TestProcessArguments(unittest.TestCase):
    """Test a few cases of the cli parsing to ensure it is functional."""

    def test_no_args(self):
        args = aws2wrap.process_arguments(['aws2-wrap'])
        self.assertFalse(args.export)
        self.assertFalse(args.generate)

    def test_exclusive(self):
        fake = io.StringIO()
        with self.assertRaises(SystemExit) as exc, contextlib.redirect_stderr(fake):
            aws2wrap.process_arguments(['aws2-wrap', '--export', '--generate'])
        self.assertEqual(exc.exception.code, 2)
        self.assertTrue(
            "argument --generate: not allowed with argument --export" in fake.getvalue())


class TestRetrieveAttribute(unittest.TestCase):

    def test_success(self):
        self.assertEqual(42, aws2wrap.retrieve_attribute({'answer': 42}, 'answer'))

    def test_failure(self):
        with self.assertRaises(aws2wrap.Aws2WrapError):
            aws2wrap.retrieve_attribute({'answer': 42}, 'question')
