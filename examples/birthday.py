from passgen import Chain, Permutation, capitalize, g, lowercase, write_wordlist

# the password started with "pw", then either "abc" or "123"
prefix = g("pw") + ["abc", "123"]

# the year 2011 was in the password (either "2011" or "11")
year = g("20").optional() + "11"
day = ["01", "1"]
month = ["june", "06", "6"]

# the birthday is either day.month.year, day-month-year or month/day/year
birthday = Chain([day, month, year], sep=["-", "."]) | Chain([month, day, year], sep=["/"])

# a special symbol somewhere in the password (either ? or !)
special_symbol = ["?", "!"]

# the words "hello world", all lowercase or capitalized ("helloworld" or "HelloWorld")
good_morning = Chain(["hello", "world"], map_each=[lowercase, capitalize])

# known prefix, unknown order of birthday, special_symbol and good_morning
password = prefix + Permutation([birthday, special_symbol, good_morning])


if __name__ == "__main__":
    count = write_wordlist(password, "wordlist.txt", dedupe=True)
    print(f"Generated {count} words.")
