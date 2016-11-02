#-*-coding:utf-8-*-
'''
https://api.github.com/repos/django/django 

{
  "id": 4164482,
  "name": "django",
  "full_name": "django/django",
  "owner": {
    "login": "django",
    "id": 27804,
    "avatar_url": "https://avatars.githubusercontent.com/u/27804?v=3",
    "gravatar_id": "",
    "url": "https://api.github.com/users/django",
    "html_url": "https://github.com/django",
    "followers_url": "https://api.github.com/users/django/followers",
    "following_url": "https://api.github.com/users/django/following{/other_user}",
    "gists_url": "https://api.github.com/users/django/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/django/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/django/subscriptions",
    "organizations_url": "https://api.github.com/users/django/orgs",
    "repos_url": "https://api.github.com/users/django/repos",
    "events_url": "https://api.github.com/users/django/events{/privacy}",
    "received_events_url": "https://api.github.com/users/django/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "private": false,
  "html_url": "https://github.com/django/django",
  "description": "The Web framework for perfectionists with deadlines.",
  "fork": false,
'''


import argparse
import requests
import json

SERVER_URL_BASE = 'https://api.github.com/repos'

def search_repository(author, repo, search_for='homepage'):
	url = '%s/%s/%s' % (SERVER_URL_BASE, author, repo)
	print 'Searching Repo URL: %s' % url
	result = requests.get(url)
	if(result.ok):
		# 将返回的json数据反序列化
		repo_info = json.loads(result.text or result.content)
		print 'Github repository info for: %s' % repo
		result = 'No result found'
		keys = []
		for key, value in repo_info.iteritems():
			# 要查找的内容在json的键中
			if search_for in key:
				result = value
		return result

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='github search')
	parser.add_argument('--author', action='store', dest='author', required=True)
	parser.add_argument('--repo', action='store', dest='repo', required=True)
	parser.add_argument('--search_for', action='store', dest='search_for', required=True)
	given_args = parser.parse_args()
	result = search_repository(given_args.author, given_args.repo, given_args.search_for)
	if isinstance(result, dict):
		print 'Got result for %s ...' % given_args.search_for
		for key,value in result.iteritems():
			print '%s => %s' % (key, value)
	else:
		print 'Got result fro %s: %s' % (given_args.search_for, result)

