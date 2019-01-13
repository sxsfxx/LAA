set py_exe="C:\Tools\Python37\python.exe"
set py_po="C:\Tools\Python37\Tools\i18n\pygettext.py"
set py_mo="C:\Tools\Python37\Tools\i18n\msgfmt.py"

%py_exe% %py_mo% -o locale\en\LC_MESSAGES\lang.mo locale\en\LC_MESSAGES\lang.po
%py_exe% %py_mo% -o locale\cn\LC_MESSAGES\lang.mo locale\cn\LC_MESSAGES\lang.po