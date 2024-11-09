import pandas as pd

# Read the JSON files
df_followers = pd.read_json('followers_1.json')['string_list_data']
df_followings = pd.read_json('following.json')['relationships_following']
df_follow_requests = pd.read_json('recent_follow_requests.json')['relationships_permanent_follow_requests']

# Extract followers and followings
followers = [f[0]['value'] for f in df_followers]
followings = [f['string_list_data'][0]['value'] for f in df_followings]
follow_requests = [f['string_list_data'][0]['value'] for f in df_follow_requests]

diff_list = [item for item in followings if item not in followers]

# Print the results
print("follow_requests:", len(follow_requests))
print("Followers:", len(followers))
print("Followings:", len(followings))

print('unfollowers: ')
for f in diff_list:
    print(f)
    print('-' * 39)
