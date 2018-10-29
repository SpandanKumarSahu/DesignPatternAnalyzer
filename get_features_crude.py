from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser
import pygccxml
import sys

# Find the location of the xml generator (castxml or gccxml)
generator_path, generator_name = utils.find_xml_generator()

# Configure the xml generator
xml_generator_config = parser.xml_generator_configuration_t(
    xml_generator_path=generator_path,
    xml_generator=generator_name)

# Parse the c++ file
decls = parser.parse([sys.argv[1]], xml_generator_config)
declarations.print_declarations(decls)