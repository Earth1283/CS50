
import sys
import os
import pytest
from unittest.mock import patch
from pyfakefs.fake_filesystem_unittest import Patcher
import load_applications
import yaml
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def clear_applications_list():
    load_applications.applications.clear()
    yield
    load_applications.applications.clear()

@pytest.fixture
def fake_fs():
    with Patcher() as patcher:
        base_dir = os.path.dirname(load_applications.__file__)
        apps_path = os.path.join(base_dir, "applications")
        patcher.fs.create_dir(apps_path)
        yield patcher.fs, apps_path

@patch('load_applications.fl')
def test_load_applications_success(mock_fl, fake_fs):
    fs, apps_path = fake_fs
    app_dir = os.path.join(apps_path, 'app1')
    fs.create_dir(app_dir)
    yml_path = os.path.join(app_dir, "application.yml")

    app_config = {
        'app_name': 'Test App', 'version': '1.0', 'description': 'A test app',
        'author': 'tester', 'ready': [], 'ready_max_runtime': 1,
        'paralell_ready_process': False, 'main': ['main.py']
    }
    fs.create_file(yml_path, contents=yaml.dump(app_config))

    load_applications.load_applications()

    assert len(load_applications.applications) == 1
    assert load_applications.applications[0]['name'] == 'Test App'
    mock_fl.log.assert_called_with("Loaded application: Test App v1.0")

@patch('load_applications.fl')
def test_load_no_yml(mock_fl, fake_fs):
    fs, apps_path = fake_fs
    fs.create_dir(os.path.join(apps_path, 'app_no_yml'))

    load_applications.load_applications()

    assert len(load_applications.applications) == 0
    mock_fl.logger.assert_called_with(load_applications.LogLevel.INFO, "Skipping app_no_yml: No application.yml found")

@patch('load_applications.fl')
def test_load_missing_fields(mock_fl, fake_fs):
    fs, apps_path = fake_fs
    app_dir = os.path.join(apps_path, 'app_missing_fields')
    fs.create_dir(app_dir)
    yml_path = os.path.join(app_dir, "application.yml")
    fs.create_file(yml_path, contents="app_name: Incomplete App")

    load_applications.load_applications()

    assert len(load_applications.applications) == 0
    mock_fl.warn.assert_called_with("Skipping app_missing_fields: Missing required fields in application.yml")

@patch('load_applications.fl')
def test_load_invalid_main_field(mock_fl, fake_fs):
    fs, apps_path = fake_fs
    app_dir = os.path.join(apps_path, 'app_invalid_main')
    fs.create_dir(app_dir)
    yml_path = os.path.join(app_dir, "application.yml")

    app_config = {
        'app_name': 'Test App', 'version': '1.0', 'description': 'A test app',
        'author': 'tester', 'ready': [], 'ready_max_runtime': 1,
        'paralell_ready_process': False, 'main': 'not_a_list'
    }
    fs.create_file(yml_path, contents=yaml.dump(app_config))

    load_applications.load_applications()

    assert len(load_applications.applications) == 0
    mock_fl.warn.assert_called_with("Skipping app_invalid_main: 'main' must contain exactly one file")

@patch('load_applications.fl')
def test_load_applications_directory_not_found(mock_fl, fake_fs):
    fs, apps_path = fake_fs

    # Ensure the applications directory does not exist for this test
    shutil.rmtree(apps_path)

    load_applications.load_applications()

    assert len(load_applications.applications) == 0
    mock_fl.warn.assert_called_with(f"Applications directory not found at {apps_path}")

@patch('load_applications.fl')
def test_yaml_load_error(mock_fl, fake_fs):
    fs, apps_path = fake_fs
    app_dir = os.path.join(apps_path, 'app_bad_yml')
    fs.create_dir(app_dir)
    yml_path = os.path.join(app_dir, "application.yml")
    fs.create_file(yml_path, contents="app_name: Bad YML: unclosed_quote: '")

    load_applications.load_applications()

    assert len(load_applications.applications) == 0
    mock_fl.error.assert_called()
    assert "Error loading" in mock_fl.error.call_args[0][0]
