#!/usr/bin/env python

# On windows the file extension .pyw hides the console window

try:
    import nmcontrol
    nmcontrol.main()
except:
    import traceback
    traceback.print_exc()  # python.exe nmcontrolwin.pyw
    f = open("errorlog_pyw.txt", "w")  # may fail on newer windows versions
    f.write(traceback.format_exc())
    f.close()
