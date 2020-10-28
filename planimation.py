#!/usr/bin/env python3
import sys,os
import planimation_api as api

USAGE_STRING = """
No command-line options given. Usage:

planimation.py submitVFG 		[absolute path of vfg file] [download option (png/webm/gif/mp4)]
planimation.py submitPDDL 		[absolute path of domain file] [absolute path of problem file] [absolute path of animation file] [download option (vfg/png/webm/gif/mp4)]
"""


if __name__ == "__main__":
	# give the usage of command line
	if len(sys.argv) == 1:
		print(USAGE_STRING)
		exit(0)
	i=1
	while i< len(sys.argv):
		#check submitVFG function
		if sys.argv[i] == "submitVFG":
			i+=1
			if len(sys.argv) == 4:
				vfg = sys.argv[i].strip()

				if vfg.endswith('.vfg'):
					i+=1
					downloadtype = sys.argv[i].strip()

					if downloadtype!='png' and downloadtype!='webm' and downloadtype!='gif' and downloadtype!='mp4':
						print("Error: desired output format is not supported; only png, gif, webm and mp4 are supported")
						exit(1)
					else:
						#print(vfg)
						#print(downloadtype)
						print(api.vfg_visualise(vfg,downloadtype))
						exit(0)
				else:
					print("Error: incorrect input format; input should be in vfg format")
					exit(1)
			else:
				print("Error: incorrect number of arguments entered for submitVFG")
				exit(1)
		# check submitPlan function
		elif sys.argv[i] == "submitPDDL":
			i+=1
			if len(sys.argv) == 6:
				domainFile = sys.argv[i].strip()
				i+=1
				problemFile = sys.argv[i].strip()
				i+=1
				animationFile = sys.argv[i].strip()
				if domainFile.endswith('.pddl') and problemFile.endswith('.pddl') and animationFile.endswith('.pddl'):
					i+=1
					downloadtype = sys.argv[i].strip()
					if downloadtype!='png' and downloadtype!='webm' and downloadtype!='gif' and downloadtype!='mp4' and downloadtype!='vfg':
						print("Error: desired output format is not supported; only vfg, png, gif, webm and mp4 are supported")
						exit(1)
					else:
						print(api.pddl_visualise(domainFile,problemFile,animationFile,downloadtype))
						exit(0)

				else:
					print("Error: incorrect input format; all input files should be in pddl format")
					exit(1)

			else:
				print("Error: incorrect number of arguments numbers entered for submitPDDL")
				exit(1)

		else:
			print("Error: no such command " + "'" + sys.argv[1] + "'")
			exit(1)
