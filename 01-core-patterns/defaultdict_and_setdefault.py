# defaultdict

from collections import defaultdict

# Grouping items into lists
grouped_items = defaultdict(list)
data = ['apple', 'banana', 'apple']
for item in data:
    grouped_items[item].append(1)
print(grouped_items)
# Output: defaultdict(<class 'list'>, {'apple': [1, 1], 'banana': [1]})
dict(grouped_items)

# Counting occurrences
counts = defaultdict(int)
for item in data:
    counts[item] += 1 # Starts at 0 if new
print(counts)
# Output: defaultdict(<class 'int'>, {'apple': 2, 'banana': 1})
dict(counts)



# setdefault

my_config = {'theme': 'dark'}

# Get 'language', default to 'en' if not present
current_lang = my_config.setdefault('language', 'en')
print(f"Current language: {current_lang}")
print(my_config)
# Output: Current language: en
#         {'theme': 'dark', 'language': 'en'}

# If key exists, it just returns the existing value (doesn't change it)
current_theme = my_config.setdefault('theme', 'light')
print(f"Current theme: {current_theme}")
print(my_config)
# Output: Current theme: dark
#         {'theme': 'dark', 'language': 'en'}


