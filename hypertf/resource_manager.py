#!flask/bin/python

# resource manager, it's a server connecting to cluster runner clients and resource query clients on physical servers,
# and a client connecting to zookeeper server

from flask import Flask, jsonify, abort, request, make_response, url_for
from kazoo.client import KazooClient
from flask_restful import reqparse, abort, Api, Resource
from requests import put, get
import json

# h_list = '192.168.2.202:12181'

# test on local
# TODO
h_list = '127.0.0.1:2181'

app = Flask(__name__)
api = Api(app)

def abort_if_resource_doesnt_exist(resource_id):
    if resource_id not in resource:
        abort(404, message="Resource {} doesn't exist".format(resource_id))

def get_resources_from_kz(zk):
    resources_from_kz = []
    for i in xrange(4):
        ps_node, stat = zk.get('/resources/node' + str(i))
        resources_from_kz.append(ps_node)

    return resources_from_kz

parser = reqparse.RequestParser()
parser.add_argument("idle")
parser.add_argument("id")
parser.add_argument("pss")
parser.add_argument("wks")
parser.add_argument("ip")

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
        resources_idle = []
        j = 0
        pss = int(args["pss"])
        wks = int(args["wks"])
        res_number = pss + wks
        if res_number > len(resource):
            abort(404, message = "no enough resources")
        while (len(resources_idle) < res_number):
            if type(resource[j]) is str:
                i = eval(resource[j])
            if type(resource[j]) is dict:
                i = resource[j]
            if int(i["idle"]) == 1:
                resources_idle.append(i)
            j = j + 1
        return resources_idle

api.add_resource(ResourceList, '/resources') 
api.add_resource(Single_machine, '/resources/<resource_id>')

if __name__ == '__main__':
    
    zk = KazooClient(hosts=h_list)
    zk.start()
    resource = get_resources_from_kz(zk)
    #print resource
    app.run(debug=True)
