import sys
import json
import pystache


with open('site.json', 'r') as f:
  site = json.load(f)

port = site['galleries'][1:]
port_names = [g['name'] for g in port]

for g in site['galleries']:
  print g
  with open(g['link']+'.json','r') as f:
    ctx = site.copy()
    ctx.update({'gen': 1, 'name': g['name'], 'images': json.load(f)})
    menu = [{'name': g1['name'], 'link': g1['link'] + '.html', 'active': g1['link'] == g['link']} for g1 in port]
    ctx.update({'items': [
        {'link': 'main.html', 'name': 'Home', 'active': g['link'] == 'main'},
        {'dropdown': 1, 'items': menu, 'name': 'Portfolio', 'active': g['name'] in port_names},
        {'link': 'clients.html', 'name': 'Clients', 'active': g['link'] == 'clients'},
        {'link': 'contacts.html', 'name': 'Contacts', 'active': g['link'] == 'contatcs'}
    ]})
    pg = pystache.Renderer(file_encoding='UTF8').render('{{> site}}', ctx)
  with open(g['link']+'.html','w') as f:
    f.write(pg.encode('UTF8'))
