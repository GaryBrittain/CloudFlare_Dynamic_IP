#!/usr/bin/python
#Use Cloudflare as a DDNS service, and keep the IP up to date

import urllib, urllib2, json

#Cloudflare API
url = "https://www.cloudflare.com/api_json.html"
key = ""
email = ""
domain = ""
host = ""

#Pushover API
po_url = "https://api.pushover.net/1/messages.json"
token = ""
user = ""

#Fetch current IP address
current_ip = urllib2.urlopen("http://iptools.bizhat.com/ipv4.php")
if current_ip.getcode() != 200:
  print 'Error obtaining current IP address'
else:
  myip = current_ip.read()

#See if the current IP is different to Cloudflare
parameters = {
    'a': 'rec_load_all',
    'tkn': key,
    'email': email,
    'z': domain
}

req = urllib2.Request(url, data=urllib.urlencode(parameters))
stats = urllib2.urlopen(req)
data = json.load(stats)

if stats.getcode() != 200:
  print 'Error connecting to Cloudflare'
else:
  for i in data['response']['recs']['objs']:
    if i['display_name'] == host:
      cf_ip = i['content']
      dns_id = i['rec_id']

#Update Cloudflare, if required
if cf_ip == myip:
  print 'No update required. Closing...'
else:
  parameters = {
    'a': 'rec_edit',
    'tkn': key,
    'email': email,
    'z': domain,
    'id': dns_id,
    'type': 'A',
    'name': host,
    'ttl': '1',
    'content': myip
  }

  req = urllib2.Request(url, data=urllib.urlencode(parameters))
  stats = urllib2.urlopen(req)
  data = json.load(stats)

  if stats.getcode() != 200:
    print 'Error connecting to Cloudflare'
  else:
#Send a notification via Pushover if successful
    if data['result'] != "success":
      print 'Error updating Cloudflare'
    else:
      parameters = {
        'token': token,
        'user': user,
        'message': 'Cloudflare IP updated: ' + data['response']['rec']['obj']['content'],
        'title': data['response']['rec']['obj']['name']
      }

      req = urllib2.Request(po_url, data=urllib.urlencode(parameters))
      stats = urllib2.urlopen(req)
      data = json.load(stats)

      if data['status'] != 1:
        print 'Error sending message to Pushover'
