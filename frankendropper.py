import urllib2
import argparse
import StringIO
import random

parser = argparse.ArgumentParser(description='Frankendrop some files.')
parser.add_argument('--host', default='www.example.com', metavar='<host>', help='the host field to use (default: "www.example.com")')
parser.add_argument('--url',default='http://www.example.com', help='the url to connect to (default: "http://www.example.com")')
parser.add_argument('--ua', default='Mozilla/4.0', help='the user-agent to use (default: "Mozilla/4.0")')
parser.add_argument('-b', '--begin', default='0', metavar= '<byte index>', help='the byte to begin with (default: 0)')
parser.add_argument('-e', '--end', default='10', metavar= '<byte index>', help='the byte to end with (default: 10)')
parser.add_argument('-c', '--chunks', type=int, default='12', metavar= '<chunk size>', help='the number of bytes per requests (default: 12)')

args = parser.parse_args()

def harvest(url, begin, end, ua, host):
    req = urllib2.Request(url)
    req.headers['Range'] = 'bytes=%s-%s' % (begin, end)
    req.headers['User-Agent'] = ua
    req.headers['Host'] = host
    return urllib2.urlopen(req)

def head_size(url, ua, host):
    req = urllib2.Request(url)
    req.get_method = lambda : 'HEAD'
    req.headers['User-Agent'] = ua
    req.headers['Host'] = host
    return int(urllib2.urlopen(req).info().getheader('Content-Length'))

def chunker(size, chunks):
    list_index = 0
    byte_index = 0
    ranges = {}
    while byte_index+chunks <= size:
        begin = byte_index
        end = begin + chunks
        ranges[list_index] = (begin, end)
        byte_index = end + 1
        list_index = list_index + 1
    if size-byte_index > 0:
        ranges[list_index] = (byte_index, (size-byte_index)+byte_index)
    return ranges

if __name__ == "__main__":
#    b = harvest(args.url, args.begin, args.end, args.ua, args.host)
#    print "the string you requested: ", b.read()
    
#    f = harvest(args.url, 86, 86, args.ua, args.host)
#    ar = harvest(args.url, 326, 327, args.ua, args.host)
#    ts = harvest(args.url, 1065, 1066, args.ua, args.host)
#    print "the string I requested: ", f.read() + ar.read() + ts.read()

    size = head_size(args.url, args.ua, args.host)
    ranges = chunker(size, args.chunks)
    data = {}
    buf = StringIO.StringIO()
    keys = ranges.keys()
    random.shuffle(keys)

    for key in keys:
        (begin, end) = ranges[key]
        f = harvest(args.url, begin, end, args.ua, args.host)
        data[key] = f.read()
    for key in sorted(data):
        buf.write(data[key])
    print buf.getvalue()
