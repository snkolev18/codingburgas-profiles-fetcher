import argparse
import subprocess
import re

def get_uname():
    out = subprocess.Popen(['git', 'config', '--list'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = out.communicate()
    config_list = str(stdout[0])
    username_match = re.search(r"(user\.name=)(.*?\\n)", str(config_list))
    username = config_list[username_match.start():username_match.end()-2]
    return username.split("=")[1]

def get_uemail():
    out = subprocess.Popen(['git', 'config', '--list'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = out.communicate()
    config_list = str(stdout[0])
    useremail_match = re.search(r"(user\.email=)(.*?\\n)", str(config_list))
    useremail = config_list[useremail_match.start():useremail_match.end()-2]
    return useremail.split("=")[1]