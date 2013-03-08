import sys
import os
import re
import subprocess
sys.path.append("..")
import dialog_server

class TDialogServer:
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

def main():
    server = dialog_server.http_server.THttpServer.THttpServer()


if __name__ == '__main__':
    main()

