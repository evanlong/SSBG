There was a weird hang we were seeing in [Float](http://itunes.apple.com/us/app/float-reader/id447992005?ls=1&mt=8). It would occur anytime a text field became the first responder. The issue could be reproduced with our development build as well as the live app store build. The hang had the following frames at the top of the callstack for the main thread:

    0   libsystem_kernel.dylib        	mach_msg_trap (in libsystem_kernel.dylib) + 20
    1   libsystem_kernel.dylib        	mach_msg (in libsystem_kernel.dylib) + 50
    2   libxpc.dylib                  	_xpc_connection_check_in (in libxpc.dylib) + 152
    3   libxpc.dylib                  	_xpc_connection_init (in libxpc.dylib) + 1032
    4   libxpc.dylib                  	_xpc_connection_wakeup2 (in libxpc.dylib) + 774
    5   libxpc.dylib                  	_xpc_connection_wakeup (in libxpc.dylib) + 62
    6   libxpc.dylib                  	_xpc_connection_send_registration (in libxpc.dylib) + 24
     
    #If you are reading this... reboot your iOS device. Your problems will probably go away.


Google didn't return useful results for some the various `_xpc*` function names. Although the libxpc keyword seemed to be associated with "hang." I went and grabbed another 4S. Fortunately, the issue did not repro. From what I could tell libxpc is related to remote debugging. However, it never shutdown properly and was left running to break as it pleased. After a quick reboot of the device we were back to normal.

Seeing as Google was pretty sparse on this issue I hope this will save others some time.

