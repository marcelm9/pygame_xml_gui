import os
from rich import print
os.system("python pyxg_xml_to_mockup.py files/test_xml.xml files/output.py")
print("[purple]Launching UI")
os.system("python files/output.py")
