import urllib.request, json, re
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


    print("#EXTM3U")
    print("#PLAYLIST:OpenFM")
    for item in sorted(out, key=lambda x: (x['group'] not in preffered_groups, x['group'], x['name'])):
        display_name = re.sub(m3u_special_char_regex, '', item['group']) + " * " + re.sub(m3u_special_char_regex, '', item['name'])
        print("#EXTINF:0 logo=" + item['logo_url'] + ",," + display_name)
        print(item['url'])