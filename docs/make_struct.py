import sys
import os
import re

FINP=open(sys.argv[1])

for line in FINP:
    line = line[:-1]
    if line[len(line)-1] == '/':
        try:
            os.makedirs(line)
        except:
            print "Dir " + line + " already exists"
        open(line+"__init__.py","w")
    else:
        if not os.path.exists(line+".py"):
            pathList = line.split("/")
            dirsCount = len(pathList) - 1
            FMOD = open(line+".py", "w")
            print >> FMOD, "# vim: set fileencoding=utf-8"
            print >> FMOD, "import sys\nimport os\nimport re\nimport subprocess"
            print >> FMOD, "sys.path.append(\"" + "/".join(".." for i in xrange(dirsCount)) + "\")"
            print >> FMOD, "import dialog_server\n"

            print >> FMOD, "class " + pathList[-1] + ":"
            print >> FMOD, "    def __init__(self):"
            print >> FMOD, '        """put fields here"""\n'

            print >> FMOD, "    def __call__(self):"
            print >> FMOD, '        """put default action here"""\n'
        else:
            print "File "+line+".py" + " already exists"

