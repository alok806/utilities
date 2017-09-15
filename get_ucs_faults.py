#!/usr/bin/env python
from argparse import ArgumentParser
import operator
from multiprocessing.pool import ThreadPool
from numrange import expand_ip
from imcsdk.imchandle import ImcHandle

def gather_faults(ip, username, password):
    handle = ImcHandle(ip, username, password)
    fault_l = []
    try:
        handle.login()
        object_array = handle.query_classid("FaultInst")
        for fault in object_array:
            fault_l.append(fault.descr)
    except Exception, e:
        print 'Failure in getting info for {} => {}'.format(ip, e)
        pass
    return fault_l



def main():
    parser = ArgumentParser('')
    parser.add_argument('-i', required=True, help='IP address range')
    parser.add_argument('-u', required=True, help='CIMC Username')
    parser.add_argument('-p', required=True, help='CIMC Password')
    args = parser.parse_args()
    ips = expand_ip(args.i)
    pool = ThreadPool(processes=36)
    async_results = {}
    output = {}

    print('Collecting data')

    for ip in ips:
        async_results[ip] = pool.apply_async(gather_faults, (ip, args.u, args.p))

    for ip in ips:
        output[ip] = async_results[ip].get()

    output = sorted(output.items(), key=operator.itemgetter(0))
    for fault in output:
        print "{} -> {}".format(fault[0], fault[1])

if __name__ == '__main__':
    main()
