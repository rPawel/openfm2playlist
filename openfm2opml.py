# -*- coding: UTF-8 -*-
import urllib.request, json, re, html


with urllib.request.urlopen("https://open.fm/radio/api/v2/ofm/stations_slug.json") as url:
    preffered_groups = ['Na Cały Dzień']
    m3u_special_char_regex = '[,\\-]'
    data = json.loads(url.read().decode())

    groups = {}
    for group in data['groups']:
        groups[group['id']] = group['name']

    out = []
    for channel in data['channels']:
    	out.append( {
    		'name': channel['name'],
    		'group': groups[channel['group_id']],
    		'url': "https://stream.open.fm/" + channel['id'],
    		'logo_url': channel['logo']['url']
    	})


    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<opml version=\"1.0\">")
    print("  <head title=\"Favorites\">")
    print("    <expansionState></expansionState>")
    print("  </head>")
    print("  <body>")
    print("    <outline icon=\"html/images/favorites.png\" text=\"Open.fm\">")

    for item in sorted(out, key=lambda x: (x['group'] not in preffered_groups, x['group'], x['name'])):
        display_name = re.sub(m3u_special_char_regex, '', item['group']) + " * " + re.sub(m3u_special_char_regex, '', item['name'])
        display_name_escaped = html.escape(display_name)
        print("      <outline URL=\"" + item['url'] + "\" icon=\"" + item['logo_url'] + "\" text=\"" + display_name_escaped + "\" type=\"audio\" />")

    print("    </outline>")
    print("  </body>")
    print("</opml>")
