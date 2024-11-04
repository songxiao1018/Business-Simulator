import cx_Freeze
import sys
# sys.setrecursionlimit(5000)  # 尝试设置一个更大的限制，比如5000，根据需要调整

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="MyApp",
    options={
        "build_exe": {
            "packages": ["flask", "sqlite3", "contextlib", "time", "tkinter", "requests", "threading", "os"],  # 调整以匹配server.py实际使用的包
            "include_files": ["db"],  # 确保docs目录或其内容是server.py需要的
            # 注释掉exclude，因为我们现在明确列出了所需包，应该避免排除必要的包
            # "excludes": []
        }
    },
    executables=executables
)


# import os
# from flask import Flask, request, jsonify
# import sqlite3
# import time
# from contextlib import closing
# import tkinter as tk
# import requests
# import threading
# from tkinter import Tk, Label, font