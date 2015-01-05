import sys

def print_progress(progress):
    sys.stdout.write("\rProgress: %d%%   " % (progress))
    sys.stdout.flush()
