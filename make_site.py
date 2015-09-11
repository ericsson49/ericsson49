import sys
import json
import pystache
import os.path

with open('site.json', 'r') as f:
  site = json.load(f)

pages = site['pages']
portfolio = [g for g in pages if g['type'] == 'gallery']
port_names = [g['name'] for g in portfolio]

for p in pages:
  print p
  ctx = site.copy()

  fname = p['link']+'.json'
  if os.path.exists(fname) and os.path.isfile(fname):
    with open(fname,'r') as f:
      ctx.update({'gen': 1, 'images': json.load(f)})

  menu = [{'name': g['name'], 'link': g['link'] + '.html', 'active': g['link'] == p['link']} for g in portfolio]
  ctx.update({'items': [
      {'link': 'main.html', 'name': 'Home', 'active': p['link'] == 'main'},
      {'dropdown': 1, 'items': menu, 'name': 'Portfolio', 'active': p['name'] in port_names},
      {'link': 'clients.html', 'name': 'Clients', 'active': p['link'] == 'clients'},
      {'link': 'contacts.html', 'name': 'Contacts', 'active': p['link'] == 'contacts'}
  ]})

  if p['type'] == 'gallery' or p['type'] == 'main':
    content = pystache.Renderer(file_encoding='UTF8').render('''
      <div class="col-xs-12 col-sm-10 col-md-11">
        <div class="embed-responsive embed-responsive-4by3">
          {{> gallery}}
        </div>
      </div>''', ctx)
  elif p['type'] == 'page' and p['name'] == 'Contacts':
    content = pystache.Renderer(file_encoding='UTF8').render('{{> contacts}}', ctx);
  else:
    content = '<img src="http://bvsd.org/health/PublishingImages/under-construction-icon-small1.gif">'

  ctx.update({'content': content})
  pg = pystache.Renderer(file_encoding='UTF8').render('{{> base}}', ctx)
  print p['link']+'.html'
  with open(p['link']+'.html','w') as f:
    f.write(pg.encode('UTF8'))
