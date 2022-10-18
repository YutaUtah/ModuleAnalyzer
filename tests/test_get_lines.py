import pytest
from pystats import PyStatsApp

INPUT_DIR = 'tests/inputs/'



class TestGetLines:
    def test_empty_file(self):
        lines = PyStatsApp.get_lines(f'{INPUT_DIR}lines-empty.py')

        assert len(lines) == 0

    def test_file(self):
        EXPECTED_OUTPUT = ['A Line', 'Another Line']

        lines = PyStatsApp.get_lines(f'{INPUT_DIR}lines-file.py')

        assert lines == EXPECTED_OUTPUT

    def test_nonexistent_file(self):
        # Expects the function to raise a particular exception
        with pytest.raises(FileNotFoundError):
            PyStatsApp.get_lines(f'{INPUT_DIR}does-not-exist.py')
