
import sys
import os
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rm_trailing_space import clean_file, main

@pytest.fixture
def fake_fs():
    with Patcher() as patcher:
        yield patcher.fs

def test_clean_file_with_trailing_space(fake_fs):
    file_path = '/test.py'
    fake_fs.create_file(file_path, contents='line1  \nline2\t\n')
    clean_file(file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    assert content == 'line1\nline2\n'

def test_clean_file_no_changes(fake_fs):
    file_path = '/test.py'
    original_content = 'line1\nline2\n'
    fake_fs.create_file(file_path, contents=original_content)
    clean_file(file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    assert content == original_content

def test_clean_empty_file(fake_fs):
    file_path = '/test.py'
    fake_fs.create_file(file_path, contents='')
    clean_file(file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    assert content == ''

def test_main_finds_and_cleans_files(fake_fs, capsys):
    fake_fs.create_file('/test1.py', contents='line1  \n')
    fake_fs.create_dir('/subdir')
    fake_fs.create_file('/subdir/test2.py', contents='line2\t\n')
    fake_fs.create_file('/not_a_python_file.txt', contents='line3  \n')

    main()

    with open('/test1.py', 'r') as f:
        assert f.read() == 'line1\n'
    with open('/subdir/test2.py', 'r') as f:
        assert f.read() == 'line2\n'

    captured = capsys.readouterr()
    assert "Cleaned: test1.py" in captured.out or "Cleaned: /test1.py" in captured.out
    assert "Cleaned: subdir/test2.py" in captured.out or "Cleaned: /subdir/test2.py" in captured.out

def test_main_no_files_found(fake_fs, capsys):
    main()
    captured = capsys.readouterr()
    assert "No Python (.py) files found" in captured.out

def test_clean_file_preserves_final_newline(fake_fs):
    file_path = '/test.py'
    original_content = 'line1  \n'
    fake_fs.create_file(file_path, contents=original_content)
    clean_file(file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    assert content == 'line1\n'
