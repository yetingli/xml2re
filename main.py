#codding:utf-8
from xml.etree.ElementTree import XMLParser
from maxdepth import MaxDepth

target = MaxDepth()
parser = XMLParser(target=target)
exampleXml = """
<framework>
  <processers>
    <processer name="AProcesser" file="lib64/A.so" path="/tmp"/>
    <processer name="BProcesser" file="lib64/B.so" value="fordelete"/>
    <processer name="BProcesser" file="lib64/B.so2222222"/>
    <services>
      <service name="search" prefix="/bin/search?" output_formatter="OutPutFormatter:service_inc">
        <chain sequency="chain1"/>
        <chain sequency="chain2"/>
      </service>
      <service name="update" prefix="/bin/update?">
        <chain sequency="chain3" value="fordelete"/>
      </service>
    </services>
  </processers>
</framework>
"""
parser.feed(exampleXml)
print parser.close()