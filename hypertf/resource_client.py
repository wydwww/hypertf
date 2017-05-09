# a class for cluster runner clients
import json
from requests import put, get

class client:
    def __init__(self, rm_address):
        self.rm_addr = rm_address

    def send_req(self, parameter_servers, workers):
        resources_list = get(self.rm_addr + "/resources", data = {"pss": parameter_servers, "wks": workers}).json()
        #resource_matrix = get(self.rm_addr + "/matrix").json()
        pss_list = resources_list[0:parameter_servers]
        wks_list = resources_list[parameter_servers:]

        # write the matrix to resource manager
        #put(self.rm_addr + "/matrix", data = {"matrix": json.dumps(resource_matrix)})

#        for i in resources_list:
#            put(self.rm_addr + "/resources/" + str(i['id']), data = {"idle": 0, "id": i['id'], "ip": i['ip']})
        return pss_list, wks_list

    def release(self, resources_to_release):
        put(self.rm_addr + "/matrix", data = {"matrix": json.dumps(resources_to_release)}) 
#            print i
#            put(self.rm_addr + "/resources/node" + str(i['id']), data = {"idle": 1, "id": i['id'], "ip": i['ip']})

