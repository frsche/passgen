from passgen import (
    Chain,
    Leet,
    Nothing,
    Permutation,
    capitalize,
    g,
    lowercase,
    unique,
)


def test_single():
    assert list(g("abc")) == ["abc"]
    assert list(g(2011)) == ["2011"]


def test_concat():
    assert list(g("a") + "b") == ["ab"]
    assert list(g("pw") + ["a", "b"]) == ["pwa", "pwb"]


def test_alternative():
    assert list(g("a") | "b") == ["a", "b"]
    assert list(g(["a", "b", "c"])) == ["a", "b", "c"]


def test_optional():
    assert list(g("20").optional() + "11") == ["11", "2011"]


def test_radd_and_ror():
    assert list("pw" + g("x")) == ["pwx"]
    assert list(["a", "b"] | g("c")) == ["a", "b", "c"]


def test_chain_sep_and_map_each():
    assert list(Chain(["a", "b"], sep=["-", "."])) == ["a-b", "a.b"]
    assert list(Chain(["hello", "world"], map_each=[lowercase, capitalize])) == [
        "helloworld",
        "HelloWorld",
    ]


def test_chain_drops_empty_parts():
    assert list(Chain([g("a").optional(), "b"], sep=["-"])) == ["b", "a-b"]


def test_permutation():
    assert set(Permutation(["a", "b"])) == {"ab", "ba"}


def test_empty_iterable_is_nothing():
    assert list(g([])) == []
    assert list(Nothing()) == []


def test_leet_default():
    assert list(Leet("ab")) == ["ab", "a8", "@b", "@8", "4b", "48"]


def test_leet_no_match_is_identity():
    assert list(Leet("xyz")) == ["xyz"]


def test_leet_custom_subs():
    assert list(Leet("ab", subs={"b": ["8"]})) == ["ab", "a8"]


def test_unique():
    assert list(unique(["a", "b", "a", "c", "b"])) == ["a", "b", "c"]