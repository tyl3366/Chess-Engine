@echo off

rem set PYTHON_CMD="C:\Python\python.exe"
set PYTHON_CMD="python.exe"

set BASEDIR=%~dp0
cd %BASEDIR%
%PYTHON_CMD% uci.py