# Simple Git

## Installation

`pip install ezgit`

run `ezgit --version` to confirm install

## Usage
run `ezgit --help`to see a list of commands and their usage
run `ezgit <command> --help` to see the available options and the respective usage for the specified command

## Sample Workflow

Imagine you have three files that you want to commit and push at once, you can use 
`ezgit create "feature branch"` to create a branch called `feature-branch` and checkout to that branch then run `ezgit push-all -m "add files to do xyz change"` to add all the files, commit them with the specified message and push them to `origin/feature-branch`

Using -i / --interactive option with the push / push-all commands allows you to modify the commit message specified

Enjoy!
