#!/usr/bin/env python3

# Import python modules
import sys

# Append local lib path
sys.path.append("core/lib")

# Import core modules
from core.worker import Worker

def main():
	# Initialize worker
	worker = Worker()
	# Run worker
	worker.run()

if __name__ == "__main__":
	main()
