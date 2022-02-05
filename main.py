import csv
import xml.etree.ElementTree as ET
from csv import writer
import os

base_path = os.path.abspath('')
local_path = '/Input'
for path, subdirs, files in os.walk(base_path+local_path):
    for name in files:
        if name.split('.')[1]=='xml':
            tree = ET.parse(path +'/'+ name)


root = tree.getroot()
headerList = ['type', 'sourceName', 'sourceVersion', 'device', 'name',
              'manufacturer', 'model', 'hardware', 'software',
              'unit', 'creationDate', 'startDate','endDate','value']
def write_to_csv(data):
	with open(data, 'a') as f_object:
		writer_object = writer(f_object)
		writer_object.writerow(row)  
	return data

def unique(list1):
    '''Adding unique elements to list'''
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list

def remove_last_charater(string):
    '''Removing last character from the string'''
    removed = string.rstrip(string[-1])
    return removed

def create_file(x):
    '''Creating csv files to insert data'''
    with open("Output/{}.csv".format(x), 'w') as file:
        dw = csv.DictWriter(file, delimiter=',', 
                    fieldnames=headerList)
        dw.writeheader()

def get_list_of_type():
    '''Getting all the elements from type and storing it in a list'''
    type_lis = []
    for child in root:
        test_dict = child.attrib
        try:      
            type = test_dict["type"]
            type_lis.append(type)
        except KeyError as error:
            pass
    return type_lis


def add_items(item_name):
    '''Adding the columns with the data inside dictionary'''
    if item_name in test_dict:
        item = test_dict[item_name]
        row.append(item)
    else:
        item = ""
        row.append(item)

def add_device_and_software(item_name, device_dictionary):
    '''Adding device and software column'''
    if item_name in device_dictionary:
            item = device_dictionary[item_name]
            item = remove_last_charater(item)
            row.append(item)
    else:
        item = ""
        row.append(item)
    
def add_other_device_items(item_name, device_dictionary):
    '''Adding columns from device dictionary element'''
    if item_name in device_dictionary:
            item = device_dictionary[item_name]
            row.append(item)
    else:
        item = ""
        row.append(item)

def extract_device_information(device_name):
    '''Extracting columns from device key of the dictionay and adding in another dictionary'''
    if device_name in test_dict:
        device = test_dict[device_name]
        dictionary = dict()
        for subString in device.split(","):
            subString = subString.split(":")
            if len(subString)==2:
                dictionary[subString[0].strip()] = subString[1]
        add_device_and_software("<<HKDevice", dictionary)
        add_other_device_items("name",dictionary)
        add_other_device_items("manufacturer",dictionary)
        add_other_device_items("model",dictionary)
        add_other_device_items("hardware",dictionary)
        add_device_and_software("software", dictionary)
    else:
        HKDevice,name,manufacturer,model,hardware,software = "","","","", "",""
        divice_info = [HKDevice,name,manufacturer,model,hardware, software]
        row.extend(divice_info)
    pass

type_lis = get_list_of_type()
unique_lis = unique(type_lis)
for list in unique_lis:
    create_file(list)

for x in unique_lis:
    for child in root:
        row = []
        test_dict = child.attrib
        try:
            if test_dict["type"] == x:
                add_items("type")
                add_items("sourceName")
                add_items("sourceVersion")       
                extract_device_information("device")
                add_items("unit")
                add_items("creationDate")
                add_items("startDate")
                add_items("endDate")
                add_items("value")
                data= write_to_csv("Output/{}.csv".format(x))
                print("Row getting added!")
        except:
            pass
