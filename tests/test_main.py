import sys
import os
from unittest.mock import patch
import pytest

# Add the root directory to the python path to allow for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import pass_exsists
from unittest.mock import mock_open

@patch('builtins.open', new_callable=mock_open, read_data='a' * 8)
def test_pass_exsists_true(mock_file):
    """
    Test that pass_exsists returns True when the password file exists and is valid.
    """
    assert pass_exsists() is True

@patch('builtins.open', side_effect=FileNotFoundError)
@patch('os.makedirs')
@patch('main.file_system_helper', return_value=True)
def test_pass_exsists_false_no_file(mock_fs_helper, mock_makedirs, mock_open):
    """
    Test that pass_exsists returns False when the password file does not exist.
    """
    assert pass_exsists() is False
    mock_makedirs.assert_called_once_with("etc")
    mock_fs_helper.assert_called_with("etc/psswrd.txt", "touch")

@patch('builtins.open', new_callable=mock_open, read_data='a' * 7)
def test_pass_exsists_false_short_password(mock_file):
    """
    Test that pass_exsists returns False when the password is too short.
    """
    assert pass_exsists() is False

@patch('builtins.open', new_callable=mock_open, read_data='a' * 73)
def test_pass_exsists_false_long_password(mock_file):
    """
    Test that pass_exsists returns False when the password is too long.
    """
    assert pass_exsists() is False

from main import check_connection

@patch('main.check_url', return_value=True)
@patch('main.fl.error')
@patch('main.console')
def test_check_connection_success(mock_console, mock_fl_error, mock_check_url):
    """
    Test that check_connection handles a successful connection correctly.
    """
    check_connection()
    mock_check_url.assert_called_once_with("https://www.python.org", 3)
    mock_fl_error.assert_not_called()
    mock_console.print.assert_not_called()

@patch('main.check_url', return_value=False)
@patch('main.fl.error')
@patch('main.console')
def test_check_connection_failure(mock_console, mock_fl_error, mock_check_url):
    """
    Test that check_connection handles a failed connection correctly.
    """
    check_connection()
    mock_check_url.assert_called_once_with("https://www.python.org", 3)
    mock_fl_error.assert_called_once_with("No internet connection detected")
    mock_console.print.assert_called_once()

from main import run_onboarding

@patch('main.print')
@patch('main.time.sleep')
@patch('main.console')
@patch('main.printWelcome')
def test_run_onboarding(mock_print_welcome, mock_console, mock_sleep, mock_print):
    """
    Test that run_onboarding prints the correct messages and sleeps for 5 seconds.
    """
    run_onboarding()
    assert mock_print.call_count == 3
    mock_sleep.assert_called_once_with(5)
    mock_console.clear.assert_called_once()
    mock_print_welcome.assert_called_once()

from main import application_hub

@patch('builtins.input', side_effect=['1', 'exit'])
@patch('main.Weather.main')
def test_application_hub_weather(mock_weather_main, mock_input):
    """
    Test that application_hub calls Weather.main when the user enters '1'.
    """
    with pytest.raises(SystemExit):
        application_hub()
    mock_weather_main.assert_called_once()

@patch('builtins.input', side_effect=['2', 'exit'])
@patch('main.ToDo.main')
def test_application_hub_todo(mock_todo_main, mock_input):
    """
    Test that application_hub calls ToDo.main when the user enters '2'.
    """
    with pytest.raises(SystemExit):
        application_hub()
    mock_todo_main.assert_called_once()

@patch('builtins.input', side_effect=['onboarding', 'exit'])
@patch('main.run_onboarding')
def test_application_hub_onboarding(mock_run_onboarding, mock_input):
    """
    Test that application_hub calls run_onboarding when the user enters 'onboarding'.
    """
    with pytest.raises(SystemExit):
        application_hub()
    mock_run_onboarding.assert_called_once()

@patch('builtins.input', side_effect=['invalid', 'exit'])
@patch('main.console')
def test_application_hub_invalid_input(mock_console, mock_input):
    """
    Test that application_hub prints an error message for invalid input.
    """
    with pytest.raises(SystemExit):
        application_hub()
    mock_console.print.assert_called_with("[red]Invalid application[/red]")

@patch('builtins.input', side_effect=['1', 'exit'])
@patch('main.Weather.main', side_effect=Exception("Test Exception"))
@patch('main.application_error')
def test_application_hub_exception(mock_application_error, mock_weather_main, mock_input):
    """
    Test that application_hub handles exceptions in applications.
    """
    with pytest.raises(SystemExit):
        application_hub()
    mock_application_error.assert_called_once()

from main import create_password

@patch('getpass.getpass', return_value='password123')
@patch('bcrypt.hashpw', return_value=b'hashed_password')
@patch('builtins.open')
def test_create_password_success(mock_open, mock_hashpw, mock_getpass):
    """
    Test that create_password successfully creates a password.
    """
    create_password()
    mock_hashpw.assert_called_once()
    mock_open.assert_called_with('etc/psswrd.txt', 'w')

@patch('getpass.getpass', side_effect=['short', 'validpassword'])
@patch('main.print')
@patch('bcrypt.hashpw', return_value=b'hashed_password')
@patch('builtins.open')
def test_create_password_too_short(mock_open, mock_hashpw, mock_print, mock_getpass):
    """
    Test that create_password handles a password that is too short.
    """
    create_password()
    mock_print.assert_called_with("[red]Your password does not meet the required safety guidelines of at least 8 chars. Please choose a stronger password.[/red]")
    mock_hashpw.assert_called_once()

@patch('getpass.getpass', side_effect=['a' * 73, 'validpassword'])
@patch('main.print')
@patch('bcrypt.hashpw', return_value=b'hashed_password')
@patch('builtins.open')
def test_create_password_too_long(mock_open, mock_hashpw, mock_print, mock_getpass):
    """
    Test that create_password handles a password that is too long.
    """
    create_password()
    mock_print.assert_called_with("[red]Your password is too long! Choose a shorter one[/red]")
    mock_hashpw.assert_called_once()

from main import handle_password_authentication

@patch('getpass.getpass', return_value='password123')
@patch('bcrypt.checkpw', return_value=True)
@patch('builtins.open')
def test_handle_password_authentication_success(mock_open, mock_checkpw, mock_getpass):
    """
    Test successful password authentication.
    """
    handle_password_authentication()
    mock_checkpw.assert_called_once()

@patch('getpass.getpass', side_effect=['wrongpassword', 'password123'])
@patch('bcrypt.checkpw', side_effect=[False, True])
@patch('builtins.open')
@patch('main.print')
def test_handle_password_authentication_incorrect_password(mock_print, mock_open, mock_checkpw, mock_getpass):
    """
    Test incorrect password authentication.
    """
    handle_password_authentication()
    assert mock_checkpw.call_count == 2
    mock_print.assert_any_call("[red]Incorrect password, please try again[/red]\n[orange]Please double check for typeos[/orange]")

@patch('getpass.getpass', side_effect=KeyboardInterrupt)
@patch('builtins.open')
@patch('main.print')
def test_handle_password_authentication_keyboard_interrupt(mock_print, mock_open, mock_getpass):
    """
    Test keyboard interrupt during password authentication.
    """
    with pytest.raises(SystemExit):
        handle_password_authentication()
    mock_print.assert_any_call("\n[red on white]Exiting password check...[/red on white]")

from main import run_startup_tasks

@patch('threading.Thread')
def test_run_startup_tasks(mock_thread):
    """
    Test that run_startup_tasks starts and joins threads correctly.
    """
    run_startup_tasks()
    assert mock_thread.call_count == 1
    mock_thread.return_value.start.assert_called_once()
    mock_thread.return_value.join.assert_called_once()