from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
 
 
disable_warnings(InsecureRequestWarning)
 
username = 'issemapp'
password = 'Cu4tr0n3t*'
# If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
host = '172.24.5.22' 
wsdl = '/home/david/Descargas/cucm-phonegrabber-master/RISService70.wsdl'
location = 'https://172.24.5.22:8443/realtimeservice2/services/RISService70?wsdl'.format(host=host)
binding = "{http://schemas.cisco.com/ast/soap}RisBinding"
 
# Create a custom session to disable Certificate verification.
# In production you shouldn't do this, 
# but for testing it saves having to have the certificate in the trusted store.
session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)
 
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)


 
def show_history():
    print(type(history))
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))

SelectBy = 'Name'
SelectItems = {}
StateInfo = ''
CmSelectionCriteria = {
        'MaxReturnedDevices': 1000,
        'DeviceClass': 'Any',
        'Model': '255',
        'Status': 'Any',
        'SelectBy': 'DirNumber',
        'SelectItems': SelectItems
    }

try:
    resp = service.selectCmDevice(CmSelectionCriteria=CmSelectionCriteria, StateInfo=StateInfo)
    #print(resp)
    print(resp['SelectCmDeviceResult']['CmNodes']['item'])
except Fault:
    show_history()