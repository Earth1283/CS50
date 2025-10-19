
import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_storage import (
    setAppInfo,
    getAppInfo,
    deleteAppInfo,
    listAppKeys,
    listAppInfo,
    AppStorageError,
    init_db
)

@pytest.fixture(autouse=True)
def setup_teardown():
    """
    This fixture is automatically used for each test.
    It sets up the database before a test and tears it down after.
    """
    # Each test will have a fresh database
    if os.path.exists('etc/appData.db'):
        os.remove('etc/appData.db')
    init_db()
    yield

def test_set_and_get_app_info():
    """
    Test that we can set and get a value for a key.
    """
    setAppInfo('test_app', 'test_key', 'test_value')
    assert getAppInfo('test_app', 'test_key') == 'test_value'

def test_get_app_info_not_found():
    """
    Test that getAppInfo raises an error when the key is not found.
    """
    with pytest.raises(AppStorageError):
        getAppInfo('test_app', 'test_key')

def test_delete_app_info():
    """
    Test that we can delete a value for a key.
    """
    setAppInfo('test_app', 'test_key', 'test_value')
    assert deleteAppInfo('test_app', 'test_key') is True
    with pytest.raises(AppStorageError):
        getAppInfo('test_app', 'test_key')

def test_delete_app_info_not_found():
    """
    Test that deleteAppInfo raises an error when the key is not found.
    """
    with pytest.raises(AppStorageError):
        deleteAppInfo('test_app', 'test_key')

def test_list_app_keys():
    """
    Test that we can list all keys for a given app.
    """
    setAppInfo('test_app', 'test_key_1', 'test_value_1')
    setAppInfo('test_app', 'test_key_2', 'test_value_2')
    assert set(listAppKeys('test_app')) == {'test_key_1', 'test_key_2'}

def test_list_app_info():
    """
    Test that we can list all key-value pairs for a given app.
    """
    setAppInfo('test_app', 'test_key_1', 'test_value_1')
    setAppInfo('test_app', 'test_key_2', 'test_value_2')
    assert listAppInfo('test_app') == {
        'test_key_1': 'test_value_1',
        'test_key_2': 'test_value_2'
    }

def test_invalid_app_name():
    """
    Test that an invalid app name raises an error.
    """
    with pytest.raises(AppStorageError):
        setAppInfo('invalid-app-name', 'test_key', 'test_value')

def test_invalid_key():
    """
    Test that an invalid key raises an error.
    """
    with pytest.raises(AppStorageError):
        setAppInfo('test_app', None, 'test_value')

def test_none_value():
    """
    Test that a None value raises an error.
    """
    with pytest.raises(AppStorageError):
        setAppInfo('test_app', 'test_key', None)
