import os
import sys

# Run pygccxml and get the document
os.system("python get_features_crude.py " + str(sys.argv[1]) + " > output.txt")

# Get the condensed XML file
os.system("python convert_to_xml.py > output.xml")

# Cleanup
os.system("rm output.txt output.xml")
