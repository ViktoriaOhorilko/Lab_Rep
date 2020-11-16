# Lab1

Option_18

* Python version : 3.7.3
* Used interpretaton : virtualenv
______________________________________________________________________________________________

## Cloning the repository

### Install Git to your computer
* do it there: `https://git-scm.com/downloads`

### Clone repository
* go to directory where you want to clone repository
* click right mouse
* then -> GitBash Here
* you`ll get command window
* run command `git clone https://github.com/ViktoriaOhorilko/Lab_Rep`

## Instaling python

### install pyenv
* go to cmd.exe 
* run command `pip install pyenv-win --target %USERPROFILE%\.pyenv`
* go to PowerShell
* run command `[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")`
* then `[System.Environment]::SetEnvironmentVariable('path', $HOME + "\.pyenv\pyenv-win\bin;" + $HOME + "\.pyenv\pyenv-win\shims;" + $env:Path,"User")`

### install python
* go to cmd.exe 
* run command `pyenv install 3.7.3`

### inatall virtualenv
* go to cmd.exe 
* run command `pipx install virtualenv`

### if you don`t have PyCharm - install it
* do it there: `https://www.jetbrains.com/pycharm/download/#section=windows`

## Running the project

* open PyCharm
* choose open project -> choose folder where you clone repository
* choose interpretator
* in terminal run commands:
1. pip install flask
2. pip install gevent
* Run project
* go to url `http://127.0.0.1:5000/api/v1/hello-world-18` in browser

