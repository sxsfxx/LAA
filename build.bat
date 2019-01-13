pyinstaller -w -F LAA.py
xcopy /Y locale\cn\LC_MESSAGES\lang.mo dist\locale\cn\LC_MESSAGES\
xcopy /Y locale\en\LC_MESSAGES\lang.mo dist\locale\en\LC_MESSAGES\