#!/usr/bin/python

import pexpect
import getpass
from sys import argv
import sys

script, hostlist, remcmd = argv
user = "set_username"
password = '[Pp]assword'
prompt = '[#$]'
yn = 'yes/no'
sshagent = 'id_rsa'
listing = open(hostlist, "r")
num = 0
psswd = getpass.getpass("Pass: ")

for host in listing:
    host = host.strip()
    num += 1
    cmd1 = "ssh %s@%s" % (user, host)
    print str(num) + ". " + host
    child = pexpect.spawn(cmd1, timeout=600)
    i = child.expect([password, prompt, yn, sshagent,
                     'Connection timed out',
                     'Could not resolve hostname'])
    if i == 0:
        child.sendline(psswd)
        child.expect(prompt)
    if i == 1:
        pass
    if i == 2:
        child.sendline('yes')
        child.expect(password)
        child.sendline(psswd)
        child.expect(prompt)
    if i == 3:
        print 'please do a ssh-add'
        break
    if i == 4:
        print host + " down."
        continue
    if i == 5:
        print host + " hostname not found."
        continue
    child.sendline('sudo su -')
    t = child.expect([password, prompt])
    if t == 0:
        child.sendline(psswd)
        child.expect(prompt)
    if t == 1:
        pass
    child.sendline(remcmd)
    child.expect(']#')
    print child.before
    child.sendline('~.')
    child.expect(pexpect.EOF)

listing.close()
