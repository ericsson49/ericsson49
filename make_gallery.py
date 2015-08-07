import sys
import json
import pystache

reload(sys)
sys.setdefaultencoding('UTF8')

name = sys.argv[1]
f1 = sys.argv[2]
f2 = f1[0:len(f1)-5] + '.html'

ff1 = open('gallery.mustache','r')
templ = ff1.read()
ff1.close()
res = pystache.render(templ, {'name': name, 'images': json.load(open(f1, 'r')) })
ff2 = open(f2,'w')
ff2.write(res)
ff2.close()

