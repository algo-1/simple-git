from simple_git import __version__
from simple_git.simple_git import app
from typer.testing import CliRunner
import subprocess

runner = CliRunner()

def test_version():
    assert __version__ == '0.1.0'

def test_create():
    # result = runner.invoke(app, ["create", "some branch"])
    # assert result.exit_code == 0
    # git checkout main
    pass

def test_push_no_option():
    pass

def test_push_with_files():
    # pass + fail 
    pass

def test_push_with_interactive():
    # pass + fail 
    pass

def test_push_all_with_no_message():
    # assert result.exit_code != 0
    pass

def test_push_all():
    # pass + fail
    pass

def init():
    # Make tmp dir and initialise git & relevant files with text for testing
    # Find a way to run this before tests (regardless of failure see pytest &/ typer test best practices)
    pass

def clean():
    # Remove created dirs gracefully
    # Find a way to run this after all tests
    pass
