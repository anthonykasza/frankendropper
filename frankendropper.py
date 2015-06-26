import urllib2
import argparse
import StringIO
import random

parser = argparse.ArgumentParser(description='Frankendrop some files.')

parser.add_argument('--host-header', type=str, default='www.example.com', metavar='<host>', 
  dest='host', help='the host field to use (default: "www.example.com")')
parser.add_argument('--url', type=str, default='http://www.example.com', metavar='<url>', 
  dest='url', help='the url to connect to (default: "http://www.example.com")')
parser.add_argument('--user-agent', type=str, default='Mozilla/4.0', metavar='<user agent>', 
  dest='ua', help='the user-agent to use (default: "Mozilla/4.0")')
parser.add_argument('-b', '--begin', type=int, default=-1, metavar='<begin byte index>',
  dest='begin', help='the byte to begin with')
parser.add_argument('-e', '--end', type=int, default=-1, metavar='<end byte index>', 
  dest='end', help='the byte to end with')
parser.add_argument('-c', '--chunk-size', type=int, default='12', metavar='<chunk size>', 
  dest='chunksize', help='the number of bytes per requests (default: 12)')
parser.add_argument('-f', '--filename', type=str, default='', metavar='<file name>',
  dest='filename', help='the file name to write the requested resource to')

args = parser.parse_args()

def harvest(url, ua, host, begin, end):
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
  if args.begin >= 0 and args.end >= args.begin:
    buf = StringIO.StringIO()
    f = harvest(args.url, args.ua, args.host, args.begin, args.end)
    print f.read()


  else:
    size = head_size(args.url, args.ua, args.host)
    ranges = chunker(size, args.chunksize)
    data = {}
    if args.filename:
      buf = open(args.filename, 'w')
    else:
      buf = StringIO.StringIO()
    keys = ranges.keys()
    random.shuffle(keys)

    for key in keys:
      (begin, end) = ranges[key]
      f = harvest(args.url, args.ua, args.host, begin, end)
      data[key] = f.read()
    for key in sorted(data):
      buf.write(data[key])
    if args.filename:
      buf.close()
    else:
      print buf.getvalue()
