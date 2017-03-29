
class Allocator:
    def __init__(self):
        self.ps_list_tcp = ["10.40.2.203:12301", "10.40.2.202:12302", "10.40.2.201:12303","10.40.2.200:12304"]
        self.ps_list_rdma = ["10.40.199.203:12301", "10.40.199.202:12302", "10.40.199.201:12303","10.40.199.200:12304"]
        self.wk_list_tcp = []
        self.wk_list_rdma =  ["10.40.199.203:12201", "10.40.199.202:12202", "10.40.199.201:12203","10.40.199.200:12204"]

    def get_ps(ps_num, is_rdma = False):
        if is_rdma:
            return self.ps_list_rdma[0:ps_num]
        else:
            return self.ps_list_tcp[0:ps_num]

    def get_wk(wk_num, is_rdma = True):
        if is_rdma:
            return self.wk_list_rdma[0:wk_num]
        else:
            return self.wk_list_tcp[0:wk_num]


    # currently we assume IP addresses are known
    # so we dont' implement the below two
    # left for future needed
    def resolve_ps_list():
        return

    def resolve_wk_list():
        return
