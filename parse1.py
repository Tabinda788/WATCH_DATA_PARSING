from traceback import print_tb
import xml.etree.ElementTree as ET
import json
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')   
RAMP_REDUCTION = str(config["constants"]["RAMP_REDUCTION"])
NO_OF_FILES_TO_GENERATE = int(config["constants"]["NO_OF_FILES_TO_GENERATE"])

REDUCTION_FACTORS = {
"HALF": 2,
"QUARTER": 4
}

tree = ET.parse("henrietta_site_user_test.jmx")
root = tree.getroot()
hhtp_sampler_proxy = tree.findall('./hashTree/hashTree/hashTree/HTTPSamplerProxy')
thread_group = tree.findall('./hashTree/hashTree/ThreadGroup')
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
    index+=1


jsonFilePath = "Output/henrietta_site_user_test.json"
with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(row_order))

def replace_text(mumtiply_num=2, ramp_reduction=None):
  with open('henrietta_site_user_test.jmx', encoding='latin-1') as f:
    tree = ET.parse(f)
    root = tree.getroot()
  ramp_reduction_factor = REDUCTION_FACTORS.get(ramp_reduction, 1)
  for elem in root.getiterator():
    attribute = elem.attrib
    try:
      if attribute['name'] == 'ThreadGroup.num_threads':
        elem.text = elem.text.replace(elem.text, str(int(elem.text)*mumtiply_num))        
      elif attribute['name'] == 'ThreadGroup.ramp_time':
        elem.text = elem.text.replace(elem.text, str(int(elem.text)*mumtiply_num/ramp_reduction_factor))

    except:
      pass
  tree.write('Output/henrietta_site_user_test_{}u_{}r.jmx'.format(mumtiply_num*len(thread_group),mumtiply_num*len(thread_group)), encoding='latin-1')

if __name__=="__main__":    
    multiplication_step = 2
    for file_no in range(NO_OF_FILES_TO_GENERATE):
        replace_text((file_no + 1)*multiplication_step, RAMP_REDUCTION)