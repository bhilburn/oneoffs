import os
import subprocess
import re
import glob
import requests
import argparse

tr_open = '<tr>\n'
tr_close = '</tr>\n'

td_open = '<td class="post-td">'
td_close = '</td>\n'


def create_tr(name, url, desc):
    if url[0:6] == 'git://':
        url = 'https://' + url[6:]

    ret_str = '\t' + tr_open
    ret_str += '\t' + td_open + '<a href="' + url + '">' + name + '</a>' + td_close
    ret_str += '\t' + td_open + desc + td_close
    ret_str += '\t' + tr_close
    return ret_str


target_dir = ""
starting_dir = os.getcwd()

parser = argparse.ArgumentParser(description="")
parser.add_argument('--dir', dest='target_dir', action="store")
parser.add_argument('--user', dest='user', action="store")
parser.add_argument('--password', dest='password', action="store")
parser.add_argument('--file', dest='ofile', action="store")
args = parser.parse_args()

dir_list = glob.glob("./" + args.target_dir + "/*")

submodules = []

for path in dir_list:
    """
    Head into each subdirectory in the target directory and if it is a git
    repository, grab the repository description through the Github API.
    Obviously this only works if the upstream Fetch URL is, actually, Github.
    """

    # Relying on submodule directories to end in '.git'
    if path[-4:] != ".git":
        continue

    os.chdir(path)
    git_remote = subprocess.check_output("git remote show origin", shell=True)

    # Parse the git Fetch URL from the git remote info
    fetch_url = ""
    git_info = re.split('\n', git_remote)
    for entry in git_info:
        entry = entry.strip()
        if entry.startswith("Fetch URL:"):
            fetch_url = entry
            break

    github_user_repo_dict = fetch_url.split("github.com")
    github_user_repo = github_user_repo_dict[1]

    if github_user_repo[-4:] == ".git":
        github_user_repo = github_user_repo[0:-4]

    api_req = requests.get("https://api.github.com/repos" + github_user_repo,
                           auth=(args.user, args.password))
    json_data = api_req.json()

    try:
        description = json_data["description"]
    except KeyError, e:
        description = "Error: Could not locate repo description on Github"

    submodules.append([github_user_repo, fetch_url, description])

    os.chdir(starting_dir)

print submodules

"""
Create the HTML table
"""

output = open(args.ofile, 'w+')

table_open = '<table class="post-table" border="1" style="width:100%">\n'
table_close = '</table>\n'

th_open = '<td class="post-th" align="center">'
th_close = '</td>\n'


output.write(table_open)

# Header Row
output.write('\t' + tr_open)
output.write('\t' + th_open + 'Plugin' + th_close)
output.write('\t' + th_open + 'Description' + th_close)
output.write('\t' + tr_close)

# Fill out the table contents
for entry in submodules:
    output.write(create_tr(entry[0], entry[1][11:], entry[2]))

output.write(table_close)

output.close()
