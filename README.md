# passgen

Build a password wordlist from what you remember about a password.

## Install

```sh
pip install -e .
```

## Use it as a library

```python
from passgen import Chain, Permutation, capitalize, g, lowercase, write_wordlist

# the password started with "pw", then either "abc" or "123"
prefix = g("pw") + ["abc", "123"]

# the year 2011 was in it ("2011" or "11")
year = g("20").optional() + "11"
day = ["01", "1"]
month = ["june", "06", "6"]

# birthday as day.month.year, day-month-year or month/day/year
birthday = Chain([day, month, year], sep=["-", "."]) | Chain([month, day, year], sep=["/"])

# a special symbol somewhere ("?" or "!")
special_symbol = ["?", "!"]

# "hello world", all lowercase or capitalized ("helloworld" or "HelloWorld")
good_morning = Chain(["hello", "world"], map_each=[lowercase, capitalize])

# known prefix, unknown order of the three parts after it
password = prefix + Permutation([birthday, special_symbol, good_morning])

for candidate in password:
    print(candidate)

write_wordlist(password, "wordlist.txt", dedupe=True)
```

First few candidates:

```
pwabc01-june-11?helloworld
pwabc01-june-11?HelloWorld
pwabc01-june-11!helloworld
pwabc01-june-11!HelloWorld
pwabc01.june.11?helloworld
```