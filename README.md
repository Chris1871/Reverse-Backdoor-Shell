Creates a backdoor reverse shell with compatible listener.  The reverse shell is made to be run on on a windows computer.  The listener should work on any operating system.

These scripts are written to be run with Python27.

Only run on your own computers or computers that you have permission to run it on.
 
Run listener.py on listener computer.  Enter in your listener computers IP Address and whichever port you want at the bottom of the script.

Run reverse_backdoor.py on victims computer.  Enter in the IP Address and Port at the bottom of the script to match what's in the listener.

reverse_backdoor.py can be turned into an executable and run on any computer with a Python intepretor.

The backdoor can run system terminal commands, change directories, and upload/download files.
To upload files, type upload <file name>
To download files, type download <filename>
Enter "exit" to quit the program

