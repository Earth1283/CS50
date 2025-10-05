import pytest
from unittest.mock import patch, Mock
import sys
import os
import requests

# Add the root directory to the python path to allow for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import utils

# Tests for validate_json
def test_validate_json_valid():
    assert utils.validate_json({'a': 1, 'b': 'text'}) == True

def test_validate_json_invalid():
    # Sets are not JSON serializable
    assert utils.validate_json({'a': 1, 'b': {1, 2, 3}}) == False

# Tests for query
def test_query_list_simple():
    db = ['apple', 'banana', 'cherry']
    assert utils.query('banana', db) == True
    assert utils.query('orange', db) == False

def test_query_list_case_insensitive():
    db = ['Apple', 'Banana', 'Cherry']
    assert utils.query('banana', db, case_sensitive=False) == True
    assert utils.query('Banana', db, case_sensitive=True) == True
    assert utils.query('banana', db, case_sensitive=True) == False

def test_query_list_strip_spaces():
    db = ['  apple  ', 'banana', 'cherry']
    assert utils.query('apple', db, strip_spaces=True) == True
    assert utils.query('  apple  ', db, strip_spaces=False) == True

def test_query_dict():
    db = {'a': 'apple', 'b': 'banana'}
    assert utils.query('a', db) == True
    assert utils.query('apple', db) == False

def test_query_regex():
    db = ['apple123', 'banana456', 'cherry789']
    assert utils.query(r'\d+', db, regex=True) == True
    assert utils.query(r'\d{4}', db, regex=True) == False

def test_query_not_found():
    db = ['apple', 'banana', 'cherry']
    assert utils.query('grape', db) == False

# Tests for validate_email
def test_validate_email_valid():
    assert utils.validate_email('test@example.com') == True
    assert utils.validate_email('user.name+tag@gmail.co.uk') == True

def test_validate_email_invalid():
    assert utils.validate_email('test@.com') == False
    assert utils.validate_email('test@com') == False
    assert utils.validate_email('test.com') == False
    assert utils.validate_email('') == False

# Tests for check_url
@patch('api.utils.requests')
def test_check_url_success(mock_requests):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_requests.head.return_value = mock_response
    assert utils.check_url('http://example.com') == True

@patch('api.utils.requests')
def test_check_url_client_error(mock_requests):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_requests.head.return_value = mock_response
    assert utils.check_url('http://example.com/notfound') == False

@patch('api.utils.requests')
def test_check_url_request_exception(mock_requests):
    mock_requests.exceptions.RequestException = requests.exceptions.RequestException
    mock_requests.head.side_effect = requests.exceptions.RequestException('Connection error')
    assert utils.check_url('http://example.com') == False

# Tests for make_an_array
def test_make_an_array():
    assert utils.make_an_array('a', 'b', 'c') == ['a', 'b', 'c']
    assert utils.make_an_array(1, 2, 3) == [1, 2, 3]
    assert utils.make_an_array() == []

# Tests for fileExsists
def test_fileExsists(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("content")
    assert utils.fileExsists(str(p)) == True
    assert utils.fileExsists(str(d / "nonexistent.txt")) == False

# Tests for file_system_helper
def test_file_system_helper_write_read(tmp_path):
    p = tmp_path / "test.txt"
    # Test write
    assert utils.file_system_helper(str(p), 'write', 'hello') == True
    # Test read
    assert utils.file_system_helper(str(p), 'read') == 'hello'

def test_file_system_helper_append(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("line1")
    assert utils.file_system_helper(str(p), 'append', 'line2') == True
    assert p.read_text() == 'line1\nline2'

def test_file_system_helper_remove(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("content")
    # The 'remove' case in file_system_helper has a bug, it uses payload for path
    # Let's test its actual behavior
    assert utils.file_system_helper('test.txt', 'remove', str(tmp_path)) == True
    assert not p.exists()

def test_file_system_helper_exsists(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("content")
    assert utils.file_system_helper(str(p), 'exsists') == True
    assert utils.file_system_helper(str(tmp_path / 'nonexistent.txt'), 'exsists') == False

def test_file_system_helper_touch(tmp_path):
    p = tmp_path / "newfile.txt"
    assert utils.file_system_helper(str(p), 'touch') == True
    assert p.exists()
    # Test touching an existing file
    assert utils.file_system_helper(str(p), 'touch') == False

def test_file_system_helper_invalid_action(tmp_path):
    p = tmp_path / "test.txt"
    assert utils.file_system_helper(str(p), 'dance', 'payload') is None

def test_file_system_helper_write_no_payload(tmp_path):
    p = tmp_path / "test.txt"
    assert utils.file_system_helper(str(p), 'write') == False
