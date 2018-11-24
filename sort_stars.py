#!/usr/bin/env python3

"""Program to get top 3 repos of Github user
   by Stars."""

# Import Statments
import sys
import optparse
import subprocess
import shlex
# End of Import Statements

"""Command Line Args"""

parser = optparse.OptionParser()
parser.add_option("-u", dest="uname",
                  help="The Github username of target account")
parser.add_option("--username", dest="uname",
                  help="The Github username of target account")

(options, arg) = parser.parse_args()
github_username = options.uname

if(github_username is None):
    parser.print_help()
    sys.exit(1)

"""End of Command Line Arg Parsing"""

# Shell Command to be executed
shell_command_1 = """curl -H "Accept: application/vnd.github.mercy-preview+json" \
https://api.github.com/users/{}/repos """.format(github_username)
shell_command_2 = """egrep "stargazers_count|full_name" """

# Running Shell Command and getting output
args1 = shlex.split(shell_command_1)
args2 = shlex.split(shell_command_2)
output0 = subprocess.run(args1, stdout=subprocess.PIPE)
output = subprocess.run(args2, stdout=subprocess.PIPE, input=output0.stdout)
inp = output.stdout.decode('utf-8')

if(inp is None):
    print("[!] No Repos! Exiting...")
    sys.exit(1)

json_dict = dict()
flag = 0  # Flag to check if first repo
curr_name = None
curr_star_count = None
line = ""
for char in inp:
    line += char
    if(char == ','):
        line = line[:-1]
        if("full_name" in line):
            if(flag == 0):
                pass
            else:
                curr_name = str(line.split(":")[-1].split("/")[-1])[:-1]
                json_dict.update({curr_name: curr_star_count})
        elif("stargazers_count" in line):
            if(flag == 0):
                flag = 1
                curr_star_count = int(line.split(":")[-1])
                json_dict.update({curr_name: curr_star_count})
            else:
                curr_star_count = int(line.split(":")[-1])
        line = ""

ctr = 0
output_dict = dict()
for (key, value) in sorted(json_dict.items(),
                           key=lambda x: x[1],
                           reverse=True):
    output_dict[key] = value
    ctr += 1
    if(ctr == 3):
        break
print(output_dict)
