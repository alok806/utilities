#!/usr/bin/env python
# paul@paullesiak.com


def expand_ip_list(ip_list):
    """
    Return an expanded list of any range operators within another IP list
    """
    if isinstance(ip_list, str):
        return expand_ip(ip_list)
    if isinstance(ip_list, list):
        hosts = []
        for host in ip_list:
            hosts.extend(expand_ip(host))
        return hosts


def expand_ip(rangefunc):
    """
    Returns an expanded list of an IP address with any range operators
    """
    hosts = []
    octets = rangefunc.split('.')
    for i, octet in enumerate(octets):
        if '-' in octet or ',' in octet:
            for digit in expand_range(octet):
                ip = '.'.join(octets[:i] + [str(digit)] + octets[i+1:])
                hosts += expand_ip(ip)
            break
    else:
        hosts.append(rangefunc)
    return hosts


def expand_range(s):
    """
    expand a text range that defines a range of integers using commas and dashes into a list
    """
    o = []
    if ',' in s:
        for c in s.split(','):
            o.extend(expand_range(c))
    elif '-' in s:
        r = sorted(map(int, s.split('-')))
        o = range(r[0], r[1] + 1)
    else:
        o = [int(s)]
    return o


def collapse_range(expandedlist):
    """
    collapses a range of integers into a comma or dash separated list
    """
    addrange = lambda l, a, b: l.append(a) if a == b else l.append(sorted([a, b]))
    results = []
    last = None
    startrange = None
    for i in sorted(set(expandedlist)):
        if last and startrange:
            if i - last > 1:
                addrange(results, startrange, last)
                startrange = i
        else:
            startrange = i
        last = i
    addrange(results, startrange, last)
    return results


def main():
    hosts = ['1.1-2.1-2.1-2', '2.2.2.2']
    assert(expand_ip_list(hosts) == ['1.1.1.1', '1.1.1.2', '1.1.2.1', '1.1.2.2', '1.2.1.1', '1.2.1.2', '1.2.2.1', '1.2.2.2', '2.2.2.2'])
    # l = [int(1000*random.random()) for i in xrange(8000)]
    l = [1, 2, 3, 4, 5, 7, 8, 9, 12, 11]
    r = collapse_range(l)
    comma = lambda a: '-'.join(map(str, a)) if isinstance(a, list) else str(a)
    rangeStr = ','.join(map(comma, r))
    e = expand_range(rangeStr)
    assert(sorted(e) == sorted(l))
    print 'Tests passed'


if __name__ == '__main__':
    main()

