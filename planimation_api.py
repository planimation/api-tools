import requests
from datetime import datetime
import re
import json

# To be changed once deployed on actual server
# Uncomment when testing locally (and comment below)
pddl_url = "http://127.0.0.1:8000/upload/(?P<filename>[^/]+)$"
vfg_url = "http://127.0.0.1:8000/downloadVisualisation"
# Uncomment when deployed on actual server (and comment above)
#pddl_url = "https://planimation.planning.domains/upload/(?P<filename>[^/]+)$"
#vfg_url = "https://planimation.planning.domains/downloadVisualisation"

# check if the input file is in the correct format using regex
def check_input(filename, format):
    x = re.search("^.+\."+format+"$", filename)
    return bool(x)


# helper function to read file
def read_file(filename):
    file = open(filename, "rb")
    content = file.read()
    file.close()
    return content


# send 3 PDDL files and get back either vfg, png, gif, webm or mp4 file
def pddl_visualise(domain_file, problem_file, animation_profile, output_format, startStep=0, stopStep=1, quality=1):
    if check_input(domain_file, "pddl") is False or check_input(problem_file, "pddl") is False \
            or check_input(animation_profile, "pddl") is False:
        print("Error: incorrect input format; all input files should be in PDDL format")
        return None
    if output_format != "png" and output_format != "webm" and output_format != "gif" and output_format != "mp4" \
            and output_format != "vfg":
        print("Error: desired output format is not supported; only vfg, png, gif, webm and mp4 are supported")
        return None
    if startStep >= stopStep:
        print("Error: startStep must be prior to stopStep")
    domain = read_file(domain_file)
    problem = read_file(problem_file)
    animation = read_file(animation_profile)
    files = ("domain", (None, domain)), ("problem", (None, problem)), ("animation", (None, animation))
    print("Waiting for response...")
    # receiving vfg file
    vfgFileResponse = requests.post(pddl_url, files=files)
    vfgFile = vfgFileResponse.content
    return vfg_visualise(vfgFile, output_format, startStep, stopStep, quality, check_needed=0)

# send a vfg file and get back either png, gif, webm or mp4 file
def vfg_visualise(vfg_file, output_format, startStep=0, stopStep=1, quality=1, check_needed=1):
    if check_needed:
        if check_input(vfg_file, "vfg") is False:
            print("Error: incorrect input format; input should be in vfg format")
            return None
    if output_format != "png" and output_format != "webm" and output_format != "gif" and output_format != "mp4":
        print("Error: desired output format is not supported; only png, gif, webm and mp4 are supported")
        return None
    # check if params follows the protocol
    if startStep >= stopStep:
        print("Error: startStep must be prior to stopStep")
    if check_needed:
        vfg = read_file(vfg_file)
    else:
        vfg = vfg_file
    files = ('vfg', (None, vfg)), ('fileType', (None, output_format))
    if check_needed:
        print("Waiting for response...")
    parameters = ('startStep', (None, startStep)), ("stopStep", (None, stopStep))
    bodyContent = {
        'fileType': output_format,
        'startStep': startStep,
        'stopStep': stopStep,
        'quality': quality
    }
    data_str = vfg.decode('utf-8')
    data_dict = json.loads(data_str)
    vfgText = json.dumps(data_dict)
    if (output_format == 'gif') or (output_format == 'mp4'):
        data_payload = {
            'vfg': vfgText,
            'fileType': output_format,
            'params': bodyContent
        }
        r = requests.post(vfg_url, json.dumps(data_payload))
    else:
        data_str = vfg.decode('utf-8')
        data_dict = json.loads(data_str)
        vfgText = json.dumps(data_dict)
        data_payload = {
            'vfg': vfgText,
            'fileType': output_format
        }
        r = requests.post(vfg_url, json.dumps(data_payload))

    if r.status_code == 200:
        # return the file in the response
        return r.content
    else:
        print(r)
        print("Error: failed to fetch the response.")
