parameter_servers_idle = ["10.40.2.203:12301", "10.40.2.202:12302", "10.40.2.201:12303", "10.40.2.200:12304"]
workers_idle = ["10.40.2.203:12201", "10.40.2.202:12202", "10.40.2.201:12203", "10.40.2.200:12204"]
parameter_servers_occupied = []
workers_occupied = []

def get_worker(n_worker):
    assert(isinstance(n_worker, int))
    workers = []
    for index in xrange(n_worker):
        workers.append(workers_idle.pop())
    for worker in workers:
        workers_occupied.append(worker)

    return workers

def get_ps(n_ps):
    assert(isinstance(n_ps, int))
    pss = []
    for index in xrange(n_ps):
        pss.append(parameter_servers_idle.pop())
    for ps in pss:
        parameter_servers_occupied.append(ps)

    return pss

def main():
    workers_test = get_worker(2)
    print "workers: "
    for i in workers_test:
        print i
    
    print "workers_occupied: "
    for i in workers_occupied:
        print i

    print "workers_idle: "
    for i in workers_idle:
        print i
    
    print "pss: "
    pss_test = get_ps(2)
    for i in pss_test:
        print i

    print "parameter_servers_occupied: "
    for i in parameter_servers_occupied:
        print i

    print "parameter_servers_idle: "
    for i in parameter_servers_idle:
        print i

if __name__ == "__main__":
    main()
