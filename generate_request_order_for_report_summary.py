import os
import configparser
import json
import xml.etree.ElementTree as ET
__author__ = "Tabinda Hilal"

config = configparser.ConfigParser()
config.read('config.cfg')
INPUT_DIRECTORY = str(config["paths"]["INPUT_DIRECTORY"])
INPUT_FILENAME = str(config["paths"]["INPUT_FILENAME"])
OUTPUT_DIRECTORY = str(config["paths"]["OUTPUT_DIRECTORY"])
JSON_FILENAME = str(config["paths"]["JSON_FILENAME"])
PROXY = str(config["tree_path"]["PROXY"])


def generate_request_row_order(input_directory, input_filename, proxy, output_directory, json_filename):
    input_file = os.path.join(input_directory, input_filename)
    tree = ET.parse(input_file)
    hhtp_sampler_proxy = tree.findall(proxy)
    row_order = {}
    list_of_testnames = []
    for proxy in hhtp_sampler_proxy:
        dict = proxy.attrib
        list_of_testnames.append(dict["testname"])
    for names in list_of_testnames:
        row_order[names] = list_of_testnames.index(names)
    index = 0
    for i in row_order:
        row_order[i] = index
        index += 1

    jsonFilePath = os.path.join(output_directory, json_filename)
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(row_order))


if __name__ == "__main__":
    generate_request_row_order(
        INPUT_DIRECTORY, INPUT_FILENAME, PROXY, OUTPUT_DIRECTORY, JSON_FILENAME)
