# a class for cluster runner clients

from requests import put, get

class client:
    def __init__(self, rm_address):
        self.rm_addr = rm_address

    # TODO: if argument bigger than list
    def send_req(self, parameter_servers, workers):
        resources_list = get(self.rm_addr + "/resources", data = {"pss": parameter_servers, "wks": workers}).json()
        
        for i in resources_list:
            put(self.rm_addr + "/resources/node1", data = {"idle": 0})
            # TODO: Just for test. It shoule be /resources/ + i["title"]
        return resources_list

    def release(self, resources_to_release):
        for i in resources_to_release:
            # TODO
            put(self.rm_addr + "/resources/node1", data = {"idle": 1})
