import os
import sys

# Run pygccxml and get the document
os.system("python get_features_crude.py " + str(sys.argv[1]) + " > output.txt")

# Convert to XML file
os.system("python convert_to_xml.py > output.xml")

# Get curate XML file
os.system("python curate_xml.py " + str(sys.argv[1]))

# Cleanup
os.system("rm output.txt output.xml output_rectified.xml")
