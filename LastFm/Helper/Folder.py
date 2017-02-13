import os

def fcount(path):
    for root, dirs, files in os.walk(path):
        return len(dirs)
