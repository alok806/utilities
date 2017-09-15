#!/usr/bin/env python
from argparse import ArgumentParser
import operator
from multiprocessing.pool import ThreadPool
from numrange import expand_ip
from imcsdk.imchandle import ImcHandle

def gather_vics(ip, username, password):
    handle = ImcHandle(ip, username, password)
    vic_l = []
    try:
        handle.login()
        object_array = handle.query_classid("AdaptorHostEthIf")
        for vic in object_array:
            vic_l.append(vic)
        handle.logout()
    except Exception, e:
        print 'Failure in getting info for {} => {}'.format(ip, e)
        pass
    return vic_l



def main():
    '''
    Quick script to detect if VICs are installed
    '''
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
        async_results[ip] = pool.apply_async(gather_vics, (ip, args.u, args.p))

    for ip in ips:
        output[ip] = async_results[ip].get()

    output = sorted(output.items(), key=operator.itemgetter(0))
    for prop in output:
        print "{} ->".format(prop[0])
        for vic in prop[1]:
            print '{:>20}'.format(vic.cdn)

if __name__ == '__main__':
    main()
