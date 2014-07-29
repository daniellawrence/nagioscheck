#!/usr/bin/env python
"""
Generate all the nagios configuration files based on puppetdb information.
"""
import subprocess as sp
import sys
import urllib2
import json
import socket
import csv
import StringIO

PUPPETDB_URL = 'https://puppetdb:8081/v3/resources'

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
DARK_YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

MESSAGE_LIMIT = 150


def _red(msg):
    " Return the passed message in RED"
    return "%s%s%s" % (RED, msg, ENDC)


def _green(msg):
    " Return the passed message in Green"
    return "%s%s%s" % (GREEN, msg, ENDC)


def _yellow(msg):
    " Return the passed message in Yellow"
    return "%s%s%s" % (YELLOW, msg, ENDC)


def _darkyellow(msg):
    " Return the passed message in Dark Yellow"
    return "%s%s%s" % (DARK_YELLOW, msg, ENDC)


def _blue(msg):
    " Return the passed message in Blue"
    return "%s%s%s" % (BLUE, msg, ENDC)


def execute_check(name, command):
    " Execute the command, caputre the return code and output string. "
    command_list = csv.reader(StringIO.StringIO(command), delimiter=' ')
    command_list = list(command_list)[0]
    child = sp.Popen(command_list, stdout=sp.PIPE)
    streamdata = ''.join(child.communicate()[0].strip().split('|')[0][0:150])
    rc = child.returncode
    if rc == 0:
        name = _green(name)
    elif rc == 1:
        name = _yellow(name)
    elif rc == 2:
        name = _red(name)
    elif rc == 3:
        name = _darkyellow(name)
    return name, streamdata, rc


def main():
    """ Run all the checks on the local system report back the finds to stdout
    Connect to puppetdb,
    Find all the checks,
    Execute all the checks,
    Report back on the results.
    """
    hostname = socket.getfqdn()
    only_check_name = None
    if len(sys.argv) == 2:
        only_check_name = sys.argv[1]

    Q = '["and",' + \
        '["=","certname","%s"],' + \
        '["=","type","Nagios-new::Nrpe::Service"]]' % hostname
    puppetdb_uri = "{0}?query={1}".format(PUPPETDB_URL, Q)
    response = urllib2.urlopen(puppetdb_uri)
    r = json.load(response)
    checks = {}
    results = {}
    for c in r:
        if only_check_name and only_check_name not in c['title']:
            continue
        checks[c['title']] = c['parameters']['check_command']

    for check_name, check_command in checks.items():
        sys.stdout.write(_blue(check_name))
        sys.stdout.flush()
        formatted_name, output, rc = execute_check(check_name, check_command)
        results['name'] = (rc, output)
        sys.stdout.write('\r%-32s %s\n' % (formatted_name, output))


if __name__ == '__main__':
    main()
