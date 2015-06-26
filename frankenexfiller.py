import os
import urllib2
import argparse
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
  dest='filename', required=True, help='the file name to POST')

args = parser.parse_args()

def putter(data, size, url, ua, host, begin, end):
  req = urllib2.Request(url)
  req.headers['Content-Range'] = 'bytes=%s-%s/%s' % (begin, end - 1, size)
  req.headers['User-Agent'] = ua
  req.headers['Host'] = host
  req.headers['Content-Length'] = size 
  req.data = data
  req.get_method = lambda: 'PUT'
  return urllib2.urlopen(req)

def chunker(size, chunks):
  list_index = 0
  byte_index = 0
  ranges = {}
  while byte_index+chunks <= size:
    begin = byte_index
    end = begin + chunks
    ranges[list_index] = (begin, end)
    byte_index = end
    list_index = list_index + 1
  if size-byte_index > 0:
    ranges[list_index] = (byte_index, (size-byte_index)+byte_index)
  return ranges

if __name__ == "__main__":
  if args.begin > 0 and args.end >= args.begin:
    size = args.end - args.begin
    with open(args.filename, 'r') as f:
      f.seek(args.begin)    
      data = f.read(size)
    putter(data, size, args.url, args.ua, args.host, args.begin, args.end)

  else:
    size = os.path.getsize(args.filename)
    ranges = chunker(size, args.chunksize)
    keys = ranges.keys()
    random.shuffle(keys)

    with open(args.filename, 'r') as f:
      for key in keys:
        (begin, end) = ranges[key]
        size = end - begin
        f.seek(begin)
        data = f.read(size)
        try:
          putter(data, size, args.url, args.ua, args.host, begin, end)
        except:
          pass
          # ignore HTTP server reponse code that indicate our PUT has failed
