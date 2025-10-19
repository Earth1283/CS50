
import sys
import os
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.file import (
    getFileStructure,
    is_file,
    is_directory,
    rm
)

@pytest.fixture
def fs_setup():
    with Patcher() as patcher:
        patcher.fs.create_dir('/mock_dir/subdir1')
        patcher.fs.create_file('/mock_dir/file1.txt')
        patcher.fs.create_file('/mock_dir/subdir1/file2.txt')
        patcher.fs.create_dir('/mock_dir/empty_subdir')
        yield patcher.fs

def test_get_file_structure_all(fs_setup):
    structure = getFileStructure('/mock_dir', returnDataMode='all')
    expected = {
        'mock_dir': {
            'file1.txt': None,
            'empty_subdir': {},
            'subdir1': {
                'file2.txt': None
            }
        }
    }
    assert structure == expected

def test_get_file_structure_folders(fs_setup):
    structure = getFileStructure('/mock_dir', returnDataMode='folders')
    expected = {
        'mock_dir': {
            'subdir1': {},
            'empty_subdir': {}
        }
    }
    assert structure == expected

def test_get_file_structure_no_subdirs(fs_setup):
    structure = getFileStructure('/mock_dir', returnDataMode='noSubdirs')
    expected = {
        'mock_dir': {
            'file1.txt': None,
            'subdir1': {},
            'empty_subdir': {}
        }
    }
    assert structure == expected

def test_get_file_structure_files(fs_setup):
    structure = getFileStructure('/mock_dir', returnDataMode='files')
    expected = {
        'mock_dir': {
            'file1.txt': None,
            'subdir1': {
                'file2.txt': None
            }
        }
    }
    assert structure == expected

def test_get_file_structure_surface(fs_setup):
    structure = getFileStructure('/mock_dir', returnDataMode='surface')
    assert sorted(structure) == sorted(['empty_subdir', 'file1.txt', 'subdir1'])

def test_get_file_structure_invalid_dir():
    with pytest.raises(ValueError):
        getFileStructure('/non_existent_dir')

def test_is_file(fs_setup):
    assert is_file('/mock_dir/file1.txt') is True
    assert is_file('/mock_dir/subdir1') is False
    assert is_file('/not/exists') is False

def test_is_directory(fs_setup):
    assert is_directory('/mock_dir/subdir1') is True
    assert is_directory('/mock_dir/file1.txt') is False
    assert is_directory('/not/exists') is False

def test_rm_file(fs_setup):
    path = '/mock_dir/file1.txt'
    assert fs_setup.exists(path)
    rm(path)
    assert not fs_setup.exists(path)

def test_rm_empty_dir(fs_setup):
    path = '/mock_dir/empty_subdir'
    assert fs_setup.exists(path)
    rm(path)
    assert not fs_setup.exists(path)

def test_rm_non_empty_dir_no_recurse(fs_setup):
    path = '/mock_dir/subdir1'
    with pytest.raises(OSError):
        rm(path, recursive=False)

def test_rm_non_empty_dir_with_recurse(fs_setup):
    path = '/mock_dir/subdir1'
    assert fs_setup.exists(path)
    rm(path, recursive=True)
    assert not fs_setup.exists(path)

def test_rm_non_existent(fs_setup):
    with pytest.raises(OSError):
        rm('/not/exists')
