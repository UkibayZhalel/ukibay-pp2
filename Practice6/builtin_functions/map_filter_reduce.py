"""
Built-in Functions - map(), filter(), and reduce()
Demonstrates functional programming tools on lists.
"""

from functools import reduce

numbers  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
words    = ["hello", "WORLD", "Python", "CODE", "open"]
products = [
    {"name": "Laptop",  "price": 999.99, "qty": 3},
    {"name": "Mouse",   "price":  29.99, "qty": 15},
    {"name": "Monitor", "price": 349.99, "qty": 7},
    {"name": "Keyboard","price":  79.99, "qty": 12},
]

# ── map() ──────────────────────────────────────────────────
print("=" * 50)
print("map()  — transform every element")
print("=" * 50)

squared   = list(map(lambda x: x ** 2, numbers))
to_upper  = list(map(str.upper, words))
revenues  = list(map(lambda p: round(p["price"] * p["qty"], 2), products))

print(f"  Original  : {numbers}")
print(f"  Squared   : {squared}")
print(f"  Words upper: {to_upper}")
print(f"  Revenues  : {revenues}")

# ── filter() ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("filter()  — keep elements that match a condition")
print("=" * 50)

evens        = list(filter(lambda x: x % 2 == 0, numbers))
long_words   = list(filter(lambda w: len(w) > 4, words))
high_revenue = list(filter(lambda p: p["price"] * p["qty"] > 500, products))

print(f"  Even numbers  : {evens}")
print(f"  Words > 4 chars: {long_words}")
print(f"  High-revenue products:")
for p in high_revenue:
    print(f"    {p['name']:10} — ${p['price'] * p['qty']:,.2f}")

# ── reduce() ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("reduce()  — aggregate to a single value")
print("=" * 50)

total        = reduce(lambda acc, x: acc + x, numbers)
product_all  = reduce(lambda acc, x: acc * x, numbers)
total_rev    = reduce(lambda acc, p: acc + p["price"] * p["qty"], products, 0)
longest_word = reduce(lambda a, b: a if len(a) >= len(b) else b, words)

print(f"  Sum of numbers    : {total}")
print(f"  Product of numbers: {product_all}")
print(f"  Total revenue     : ${total_rev:,.2f}")
print(f"  Longest word      : '{longest_word}'")

# ── Chaining all three ─────────────────────────────────────
print("\n" + "=" * 50)
print("CHAINED  map → filter → reduce")
print("=" * 50)
# Sum of squares of even numbers
result = reduce(
    lambda acc, x: acc + x,
    filter(lambda x: x % 2 == 0,
           map(lambda x: x ** 2, numbers))
)
print(f"  Sum of squares of even numbers: {result}")
print(f"  (2²+4²+6²+8²+10² = 4+16+36+64+100 = {4+16+36+64+100})")
