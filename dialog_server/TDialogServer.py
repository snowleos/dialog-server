import sys
import os
import re
import subprocess
sys.path.append("..")
import dialog_server
import dialog_server.http_server.THttpServer

PROJECT_BASE_DIR = os.getcwd() + "/.."
print PROJECT_BASE_DIR

class TDialogServer:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

def main():
    server = dialog_server.http_server.THttpServer.THttpServer(\
            confPath=PROJECT_BASE_DIR + \
            "/conf/dialog_server.http_server.conf")

    server.Start()
    


if __name__ == '__main__':
    main()

