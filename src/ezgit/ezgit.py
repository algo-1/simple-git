import typer
import subprocess
import logging
from rich.logging import RichHandler
import readline

from . import __version__

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

app = typer.Typer()

@app.command("create")
def create_and_checkout_to_branch(
    name: str,
):
    '''
    Creates a new branch from the argument specified delimited by '-' if it does not exist and checkouts to that branch. 
    '''
    branch = create_branch(name)
    subprocess.run(["git", "checkout", "-b", f"{branch}"])

@app.command("push")
def push(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="allows modification of commit message.", show_default=True 
    ),
    message: str = typer.Option(
        '', "-m", "--message", help="commits all staged files with the specified message and pushes to the remote branch.", show_default=True 
    ),
    files: str = typer.Option(
        '', "--files", help='''specify files to stage before commit and push. Example usage: simple-git push -m "fix typos" --files 'example.py utils.py src/config.toml'.'''
    ),
):
    '''
    Pushes all changes to a remote branch of the current branch (creates one if it does not exist).
    '''
    __opts__ = {"-m", "--message", "-i", "--interactive", "--files"}
    try:
        if files:
            if not message:
                log.error("Message option required when using the files option.")
                raise typer.Exit(code=1)
            git_add(files.split())
        if message:
            while message in __opts__:
                log.error("Options cannot be used as message. Enter a valid commit message.")
                message = input(f"commit message: ")
            if interactive:
                message = rlinput("commit message: ", prefill=message)

            log.info(f"Committing with message '{message}'.")
            subprocess.run(["git", "commit", "-m", message])
            push_to_remote()
        else:
            if interactive:
                log.error("Message option required to use interactive.")
                raise typer.Exit(code=1)
            else:
                push_to_remote()
        
    except subprocess.CalledProcessError as err:
        handle_subprocess_error(err)

@app.command("push-all")
def push_all(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="allows modification of commit message.", show_default=True 
    ),
    message: str = typer.Option(
        ..., "-m", "--message", help="commits all staged files with the specified message and pushes to the remote branch.", show_default=True 
    ),
):
    '''
    Adds, commits and pushes all changes to a remote branch of the current branch (creates one if it does not exist).
    '''
    try:
        git_add(["."])
        push(interactive=interactive, message=message, files='')
    except subprocess.CalledProcessError as err:
        handle_subprocess_error(err)

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()

def find_newline_or_space(string, start_index):
    space_index = string.find(" ", start_index)
    newline_index = string.find('\n')

    if space_index != -1 and newline_index != -1:
        return min(space_index, newline_index)
    else:
        return max(space_index, newline_index)

def create_branch(name: str):
    return "-".join(name.split())

def handle_subprocess_error(error: subprocess.CalledProcessError):
    log.error(f"Command failed")
    log.error(f"{error.output}")
    raise typer.Exit(code=error.returncode)

def git_add(files):
    subprocess.run(["git", "add", *files])

def get_commits_not_pushed():
    return subprocess.run(["git", "log", "--branches", "--not", "--remotes"], capture_output=True, text=True).stdout

def get_remote_branch():
    stdout = subprocess.run(["git", "status", "-sb"], capture_output=True, text=True).stdout
    start_index = stdout.find('origin')
    if start_index != -1:
        end_index = find_newline_or_space(stdout, start_index)
        return stdout[start_index:end_index]
    return ""

def push_to_remote():
    commits_to_push = get_commits_not_pushed()
    if commits_to_push:
        remote_branch = get_remote_branch()
        if remote_branch:
            subprocess.run(["git", "push"])
        else:
            subprocess.run(["git", "push", "-u", "origin", "HEAD"])
            remote_branch = get_remote_branch()
        log.info(f"Pushed all changes to {remote_branch}.")
    else:
        log.info("No commits to push.")

def version_callback(value: bool):
    if value:
        typer.echo(f"Simple Git CLI Version: {__version__}.")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(None, "--version", help="Shows the installed version.", callback=version_callback, is_eager=True)
):
    return

def cli():
    app()
