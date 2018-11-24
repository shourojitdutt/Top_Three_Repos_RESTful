#!/usr/bin/env python3

# Import Statements
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import subprocess
import shlex
import json
# End of Import Statements

app = Flask(__name__)
api = Api(app)


class TopThreeStars(Resource):

    def fetch_top_three(github_username):
        # Shell Command to be executed
        shell_command_1 = """curl -H "Accept: application/vnd.github.mercy-preview+json" \
        https://api.github.com/users/{}/repos """.format(github_username)
        shell_command_2 = """egrep "stargazers_count|full_name" """

        # Running Shell Command and getting output
        args1 = shlex.split(shell_command_1)
        args2 = shlex.split(shell_command_2)
        output0 = subprocess.run(args1, stdout=subprocess.PIPE)
        output = subprocess.run(
            args2, stdout=subprocess.PIPE, input=output0.stdout)
        inp = output.stdout.decode('utf-8')
        if(inp is None):
            print("[!] No Repos!")
            return([])

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
                        curr_name = str(line.split(
                            ":")[-1].split("/")[-1])[:-1]
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
        return(output_dict)

    def post(self):
        data = request.get_json()
        output = TopThreeStars.fetch_top_three(data['org'])
        json_list = list()
        for val in output.keys():
            newdict = dict()
            newdict.update({"{!s}".format("name"): val})
            newdict.update({"{!s}".format("stars"): output[val]})
            json_list.append(json.dumps(newdict, ensure_ascii=False))
        return jsonify({"result": json_list})


api.add_resource(TopThreeStars, "/repos")

if __name__ == '__main__':
    app.run(debug=True)
