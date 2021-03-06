# This script will show you all the shared connections (shared friends) between two Twitter accounts

import urllib
import simplejson as json

source_TwitterAccount = 'ebloch' #Set's the srouce Twitter account to compare friends with /hardcoded


# This returns all the friends of a particular Twitter user as a list
def findfriends(TwitterAccount):
  SEARCH_FOLLOWING = 'http://api.twitter.com/1/friends/ids.json?screen_name='
  SEARCH_FOLLOWERS = 'http://api.twitter.com/1/followers/ids.json?screen_name='
  following_url = SEARCH_FOLLOWING + TwitterAccount
  followers_url = SEARCH_FOLLOWERS + TwitterAccount
  following_results = json.load(urllib.urlopen(following_url))
  followers_results = json.load(urllib.urlopen(followers_url))
  if 'error' in following_results:
    return None
  elif 'error' in followers_results:
    return None
  else:
    
    friends = set(following_results['ids']) & set(followers_results['ids'])
    return friends
  
# This returns all friend overlap between two sets of friends
def compare(friends_one,friends_two):
  matches = set(friends_one) & set(friends_two)
  if not matches:
    return None
  else:
    return matches
  
# This turns plain Twitter Id's into fun Twitter usernames
def make_usernames(ids):
  USER_ID_SHOW = 'http://api.twitter.com/1/users/show.json?user_id='
  usernames = []
  for id in ids:  
    url = USER_ID_SHOW + str(id)
    results = json.load(urllib.urlopen(url))
#    print id
#    print results['screen_name']
    usernames.append(results['screen_name'])
  return usernames  

lookup_TwitterAccount = raw_input('Twitter account: ') #Ask for the lookup account to compare against source account
print ''
print 'Using ' + source_TwitterAccount + ' as account source...'
source_friends = findfriends(source_TwitterAccount) #Run friend finder on source account
lookup_friends = findfriends(lookup_TwitterAccount.replace('/', '').replace('@', '')) #Run friend finders on lookup account and strip @ and /
if lookup_friends == None: #If lookup account doesn't have any friends or there's an error notify
  print 'Sorry this is an invalid Twitter account'
else:
  print 'Discover all mututal friends between ' + source_TwitterAccount + ' and ' + lookup_TwitterAccount + '...'
  friends_in_common = compare(source_friends, lookup_friends) # See if source and lookup account have any friends in common
  if friends_in_common == None:
    print 'Sorry but you have no friends in common :('
  else:
    print 'Converting numbers into names...'
    friends_with_names = make_usernames(friends_in_common) #Convert friends in common Twitter IDs to actual Twitter usernames
    print friends_with_names
print ''

  