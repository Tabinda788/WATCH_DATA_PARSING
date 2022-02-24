import configparser
import os
import xml.etree.ElementTree as ET
__author__ = "Tabinda Hilal"


config = configparser.ConfigParser()
config.read('config.cfg')
RAMP_REDUCTION = str(config["constants"]["RAMP_REDUCTION"])
NO_OF_FILES_TO_GENERATE = int(config["constants"]["NO_OF_FILES_TO_GENERATE"])
INPUT_DIRECTORY = str(config["paths"]["INPUT_DIRECTORY"])
INPUT_FILENAME = str(config["paths"]["INPUT_FILENAME"])
OUTPUT_DIRECTORY = str(config["paths"]["OUTPUT_DIRECTORY"])

REDUCTION_FACTORS = {
    "HALF": 2,
    "QUARTER": 4
}


def modify_load_params(input_directory, input_filename, output_directory, mumtiply_num=2, ramp_reduction=None):
    input_file = os.path.join(input_directory, input_filename)
    with open(input_file, encoding='latin-1') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        ramp_reduction_factor = REDUCTION_FACTORS.get(ramp_reduction, 1)

        for elem in root.getiterator():
            attribute = elem.attrib
            try:
                if attribute['name'] == 'ThreadGroup.num_threads':
                    new_user_count = str(int(elem.text)*mumtiply_num)
                    elem.text = elem.text.replace(elem.text, new_user_count)
                elif attribute['name'] == 'ThreadGroup.ramp_time':
                    new_ramp = str(int(elem.text)*mumtiply_num /
                                   ramp_reduction_factor)
                    elem.text = elem.text.replace(elem.text, new_ramp)

            except:
                pass
        output_filename = "_".join([input_filename[:input_filename.rfind(".jmx")], new_user_count+"u",
                                   new_ramp+"r"]) + ".jmx"
        tree.write(os.path.join(output_directory,
                   output_filename), encoding='latin-1')


if __name__ == "__main__":
    multiplication_step = 2
    for file_no in range(NO_OF_FILES_TO_GENERATE):
        modify_load_params(INPUT_DIRECTORY, INPUT_FILENAME, OUTPUT_DIRECTORY,
                           (file_no + 1)*multiplication_step, RAMP_REDUCTION)
