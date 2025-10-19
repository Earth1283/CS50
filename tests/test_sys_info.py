
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sys_info import (
    getOS,
    getPythonVersion,
    getMachine,
    getProcessor,
    getPlatform
)

@patch('sys_info.platform')
@patch('sys_info.fl')
def test_get_os(mock_fl, mock_platform):
    """
    Test that getOS returns the correct OS and logs the call.
    """
    mock_platform.system.return_value = 'Linux'
    assert getOS() == 'Linux'
    mock_fl.logger.assert_called_once()

@patch('sys_info.platform')
@patch('sys_info.fl')
def test_get_python_version(mock_fl, mock_platform):
    """
    Test that getPythonVersion returns the correct Python version and logs the call.
    """
    mock_platform.python_version.return_value = '3.8.10'
    assert getPythonVersion() == '3.8.10'
    mock_fl.logger.assert_called_once()

@patch('sys_info.platform')
@patch('sys_info.fl')
def test_get_machine(mock_fl, mock_platform):
    """
    Test that getMachine returns the correct machine and logs the call.
    """
    mock_platform.machine.return_value = 'x86_64'
    assert getMachine() == 'x86_64'
    mock_fl.logger.assert_called_once()

@patch('sys_info.platform')
@patch('sys_info.fl')
def test_get_processor(mock_fl, mock_platform):
    """
    Test that getProcessor returns the correct processor and logs the call.
    """
    mock_platform.processor.return_value = 'x86_64'
    assert getProcessor() == 'x86_64'
    mock_fl.logger.assert_called_once()

@patch('sys_info.platform')
@patch('sys_info.fl')
def test_get_platform(mock_fl, mock_platform):
    """
    Test that getPlatform returns the correct platform and logs the call.
    """
    mock_platform.platform.return_value = 'Linux-5.4.0-72-generic-x86_64-with-glibc2.29'
    assert getPlatform() == 'Linux-5.4.0-72-generic-x86_64-with-glibc2.29'
    mock_fl.logger.assert_called_once()
