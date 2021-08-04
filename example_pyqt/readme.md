# introduction

this folder will include all scripts and exercises of pyQt5.

reference link: 
- http://code.py40.com/pyqt5/14.html
- https://zetcode.com/gui/pyqt5/


## how to install pyQt5
run comamnd:
``` sudo pip3 install pyqt5 ```
if failed as: 
```
Using cached https://files.pythonhosted.org/packages/8e/a4/d5e4bf99dd50134c88b95e926d7b81aad2473b47fde5e3e4eac2c69a8942/PyQt5-5.15.4.tar.gz
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/usr/lib/python3.6/tokenize.py", line 452, in open
        buffer = _builtin_open(filename, 'rb')
    FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pip-build-g65ja1kh/pyqt5/setup.py'
    
    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-g65ja1kh/pyqt5/
```

run this command 
``` pip3 install --upgrade pip ``` to upgrade pip, then run ```sudo pip3 install pyqt5 ```
reference: https://discourse.psychopy.org/t/trouble-installing-on-ubuntu-18-04/10568

#### on windows
can run command: ```pip3 install PyQt5``` to install PyQt5.
