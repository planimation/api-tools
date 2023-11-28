# !/usr/bin/env python3
import sys, os
import argparse
import planimation_api as api
import zipfile
from io import BytesIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line utility for Planimation Python API.")
    subparsers = parser.add_subparsers(dest="fileOption", help="submitPDDL or submitVFG")
    parser_pddl = subparsers.add_parser("submitPDDL", help="Choose PDDL files")
    # [path of domain] [path of problem] [path of animation profile]
    parser_pddl.add_argument("path_of_domain", help="Path of domain")
    parser_pddl.add_argument("path_of_problem", help="Path of problem")
    parser_pddl.add_argument("path_of_animation_profile", help="Path of animation profile")
    parser_pddl.add_argument("output_format", help="Output format.")
    # flags
    parser_pddl.add_argument("--startStep", help="Start step")
    parser_pddl.add_argument("--stopStep", help="Stop step")
    parser_pddl.add_argument("--quality", help="Quality")
    # VFG
    parser_vfg = subparsers.add_parser("submitVFG", help="Choose VFG file")
    parser_vfg.add_argument("path_of_VFG", help="Path of VFG")
    parser_vfg.add_argument("output_format", help="Output format.")
    # flags
    parser_vfg.add_argument("--startStep", help="Start step")
    parser_vfg.add_argument("--stopStep", help="Stop step")
    parser_vfg.add_argument("--quality", help="Quality")

    args = parser.parse_args()

    if args.output_format is None:
        print("Error: output format not specified.")
        exit(1)
    if args.output_format not in ["mp4", "png", "gif", "webm"]:
        print("Error: output format not supported.")
        exit(1)
    if args.startStep is None:
        startStep = 0
    else:
        startStep = args.startStep
    if args.stopStep is None:
        stopStep = 0
    else:
        stopStep = args.stopStep
    if args.quality is None:
        quality = 1
    else:
        quality = args.quality
    if args.fileOption == "submitPDDL":
        result = api.pddl_visualise(args.parth_of_domain, args.path_of_problem, args.path_of_animation_profile,
                           args.output_format, startStep, stopStep, quality)
    else:
        result = api.vfg_visualise(args.path_of_VFG, args.output_format, startStep, stopStep, quality)

    if args.output_format == 'png':
        with zipfile.ZipFile(BytesIO(result), 'r') as zip_ref:
            zip_ref.extractall('animation_png')
    else:
        with open('animation.'+args.output_format, 'wb') as animation:
            animation.write(result)
