Python script to generate password wordlist based on description of the password.

Example:
```python
# the password started with "pw", then either "abc" or "123"
prefix = g("pw") + ["abc", "123"]

# i remember the year 2011 was in the password (either "2011" or "11")
year = g("20").optional() + "11"
day = ["01", "1"]
month = ["june", "06", "6"]
# the birthday is either day.month.year, day-month-year or month/day/year
birthday = Chain([day ,month, year], sep=["-", "."]) | Chain([month, day, year], sep=["/"])

# there was a special symbol inside the password (either ? or !)
special_symbol = ["?", "!"]

# there were also the two words "hello world" in the password. But either all lowercase, or capitalized. (either "helloworld" or "HelloWorld")
good_morning = Chain(["hello", "world"], map_each=[lowercase, capitalize])

# I know the password started with prefix, but i don't know the order of birthday, special_symbol and good_morning.
password = prefix + Permutation([birthday, special_symbol, good_morning])

count = 0
with open("wordlist.txt", "w") as f:
	for t in password:
		f.write(t + "\n")
		count += 1
print("Generated", count, "words.")
```

Results in the following wordlist (first 10 entries):
```
pwabc01-june-11?helloworld
pwabc01-june-11?HelloWorld
pwabc01-june-11!helloworld
pwabc01-june-11!HelloWorld
pwabc01.june.11?helloworld
pwabc01.june.11?HelloWorld
pwabc01.june.11!helloworld
pwabc01.june.11!HelloWorld
pwabc01-june-2011?helloworld
pwabc01-june-2011?HelloWorld
```