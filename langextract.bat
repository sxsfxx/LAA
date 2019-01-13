set py_exe="C:\Tools\Python37\python.exe"
set py_po="C:\Tools\Python37\Tools\i18n\pygettext.py"
set py_mo="C:\Tools\Python37\Tools\i18n\msgfmt.py"

%py_exe% %py_po% -o lang.po *.py
copy lang.po locale\en\LC_MESSAGES
copy lang.po locale\cn\LC_MESSAGES