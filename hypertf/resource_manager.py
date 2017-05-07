#!flask/bin/python

# resource manager, it's a server connecting to cluster runner clients 
# , and resource query clients on physical servers
# , and a client connecting to zookeeper server

from flask import Flask, jsonify, abort, request, make_response, url_for
from kazoo.client import KazooClient
from flask_restful import reqparse, abort, Api, Resource
from requests import put, get
import json

h_list = '192.168.2.200:2181'

app = Flask(__name__)
api = Api(app)

def abort_if_resource_doesnt_exist(resource_id):
    if resource_id not in resource:
        abort(404, message="Resource {} doesn't exist".format(resource_id))

def get_resource(zk):
    resource_dict = {}
    resource_list_unicode = zk.get_children("resources/") 
    resource_list = list(map(lambda x: str(x), resource_list_unicode))
    for i in resource_list:
        resource_node, stat = zk.get('/resources/%s' % i)
        resource_dict[i] = resource_node
    return resource_dict

parser = reqparse.RequestParser()
parser.add_argument("idle")
parser.add_argument("id")
parser.add_argument("pss")
parser.add_argument("wks")
parser.add_argument("ip")
parser.add_argument("gpus")

# resource schedule
def schedule(ps_num, wk_num, gpu_num):
    resource_offered = []
    ps_offered = []
    wk_offered = []
    res_number = ps_num + wk_num
    server_num = res_number / gpu_num # Let's assume it can be divided for now.
    
    if gpu_num > 4:
        abort(404, message = "a single server has max 4 GPUs")
    if res_number > len(resource): 
        abort(404, message = "no enough resources") 

    j = 0

    while (len(resource_offered) < server_num): 
        i = resource.values()[j]
        if type(resource[j]) is str: 
            i = eval(resource[j]) 
        if type(resource[j]) is dict: 
            i = resource[j] 
        if len(i["gpu_avail_list"]) > 1: 
            resource_return.append(i) 
        j = j + 1
    
    ps_offered = resource_offered[0:ps_num]
    wk_offered = resource_offered[ps_num:]

    return resource_offered

class Single_machine(Resource):
    def get(self, resource_id):
        abort_if_resource_doesnt_exist(resource_id)
        return resource[resource_id]    
    
    def put(self, resource_id):
        args = parser.parse_args()
        node = {
            "idle": args["idle"],
            "id": args["id"],
            "ip": args["ip"]
            }
        resource[int(resource_id[-1])] = node
        # update resource info in zookeeper
        zk = KazooClient(hosts=h_list)
        zk.start()
        zk.ensure_path("/resources/")
        if zk.exists("/resources/" + resource_id):
            zk.set("/resources/" + resource_id, json.dumps(node))
        else:
            zk.create("/resources/" + resource_id, json.dumps(node))
        return

class ResourceList(Resource):
    def get(self):
        args = parser.parse_args()
        pss = int(args["pss"])
        wks = int(args["wks"])
        gs = int(args["gpus"])
        return schedule(pss, wks, gs)

api.add_resource(ResourceList, '/resources') 
api.add_resource(Single_machine, '/resources/<resource_id>')

if __name__ == '__main__':
    
    zk = KazooClient(hosts=h_list)
    zk.start()
    resource = get_resource(zk)
    for i in resource:
        print resource[i]
    app.run(debug=True)

