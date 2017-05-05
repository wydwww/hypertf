# a class for cluster runner clients

from requests import put, get

class client:
    def __init__(self, rm_address):
        self.rm_addr = rm_address

    def send_req(self, parameter_servers, workers, gpus):
        resources_list = get(self.rm_addr + "/resources", data = {"pss": parameter_servers, "wks": workers, "gpus": gpus}).json()
        pss_list = resources_list[0:parameter_servers]
        wks_list = resources_list[parameter_servers:]
        for i in resources_list:
            put(self.rm_addr + "/resources/node" + str(i['id']), data = {"idle": 0, "id": i['id'], "ip": i['ip']})
        return pss_list, wks_list

    def release(self, resources_to_release):
        for i in resources_to_release:
#            print i
            put(self.rm_addr + "/resources/node" + str(i['id']), data = {"idle": 1, "id": i['id'], "ip": i['ip']})
