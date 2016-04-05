# qiyan.zm@alibaba-inc.com
import proxylet, sys, re
from proxylet import relocate
from proxylet.relocate import Relocator, UrlInfo
from paste import httpheaders as hdr

'''
[(local url, remote url), (local url2, remote url2), default url]
'''
routes = [
    ('http://localhost:7070/query-player', 'http://localhost:7070'),
    'http://localhost:5000'
]

def to_relocator(route):
    if type(route) == str: return None
    (local, remote) = route
    return Relocator(local, remote)

relocators = filter(lambda r: r, map(to_relocator, routes))

def mapper(req):
    ref_str = hdr.REFERER(req.headers)
    referer = UrlInfo(ref_str) if ref_str else None
    for r in relocators: 
        if r.matchesLocal(req.reqURI):
            return r.mapping
        if referer and r.matchesLocal(referer.path):
            return r.mapping
    url = UrlInfo(routes[-1])
    return (url.host, url.port, None)

def main(port):
    try:
        proxylet.serve('', port, mapper)
    except (SystemExit, KeyboardInterrupt):
        print('bye')
        
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7110
    main(port)

