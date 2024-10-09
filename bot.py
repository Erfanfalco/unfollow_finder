import pandas as pd

# Read the JSON files
df_followers = pd.read_json('followers_1.json')['string_list_data']
df_followings = pd.read_json('following.json')['relationships_following']


# Extract followers and followings
followers = [f[0]['value'] for f in df_followers]
followings = [f['string_list_data'][0]['value'] for f in df_followings]

# Print the results
print("Followers:", len(followers))
print("Followings:", len(followings))

diff_list = [item for item in followings if item not in followers]

print('diff: ', diff_list)
