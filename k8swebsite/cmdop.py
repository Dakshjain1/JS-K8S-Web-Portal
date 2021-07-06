#!/usr/bin/python3

import cgi
import subprocess
import os
print("content-type: text/html")
print()

f = cgi.FieldStorage()
cmd = f.getvalue("cmd")
cmd1 = "sudo {0} --kubeconfig=./config".format(cmd)

#a = subprocess.getoutput(cmd1)
#print(a)

runCmd = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
(output, err) = runCmd.communicate()
exitCode = runCmd.wait()
if exitCode == 0:
    print(output.decode())
else:
    print(output.decode())
