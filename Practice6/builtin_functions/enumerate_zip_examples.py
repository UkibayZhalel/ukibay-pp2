"""
Built-in Functions - enumerate() and zip()
Demonstrates paired iteration and type checking/conversions.
"""

# ── enumerate() ────────────────────────────────────────────
print("=" * 50)
print("enumerate()  — index + value pairs")
print("=" * 50)

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print("  Default (starts at 0):")
for i, fruit in enumerate(fruits):
    print(f"    [{i}] {fruit}")

print("\n  Custom start (starts at 1):")
for i, fruit in enumerate(fruits, start=1):
    print(f"    {i}. {fruit}")

print("\n  Practical: find index of a value:")
target = "cherry"
for i, fruit in enumerate(fruits):
    if fruit == target:
        print(f"    '{target}' found at index {i}")

# ── zip() ──────────────────────────────────────────────────
print("\n" + "=" * 50)
print("zip()  — pair multiple iterables together")
print("=" * 50)

names   = ["Alice",  "Bob",    "Carol",  "Dave"]
scores  = [92,        85,       78,       95]
grades  = ["A",      "B",      "C",      "A"]

print("  Zipping 3 lists:")
print(f"  {'Name':8} {'Score':>6} {'Grade':>6}")
print(f"  {'-'*8} {'-'*6} {'-'*6}")
for name, score, grade in zip(names, scores, grades):
    print(f"  {name:8} {score:>6} {grade:>6}")

print("\n  zip() stops at shortest list:")
long_list  = [1, 2, 3, 4, 5]
short_list = ["a", "b", "c"]
print(f"  Pairs: {list(zip(long_list, short_list))}")

print("\n  zip() to create a dictionary:")
keys   = ["host", "port", "db",   "user"]
values = ["localhost", 5432, "mydb", "admin"]
config = dict(zip(keys, values))
for k, v in config.items():
    print(f"    {k:6} → {v}")

# ── enumerate + zip combined ───────────────────────────────
print("\n" + "=" * 50)
print("enumerate() + zip()  — indexed pairs")
print("=" * 50)
for i, (name, score, grade) in enumerate(zip(names, scores, grades), start=1):
    bar = "█" * (score // 10)
    print(f"  {i}. {name:6} {grade}  {bar} {score}")

# ── Type checking and conversions ─────────────────────────
print("\n" + "=" * 50)
print("TYPE CHECKING  (type, isinstance)")
print("=" * 50)

mixed = [42, 3.14, "hello", True, None, [1, 2], {"a": 1}]
for val in mixed:
    print(f"  {str(val):12} | type: {type(val).__name__:6} | "
          f"isinstance(int): {isinstance(val, int)}")

print("\n" + "=" * 50)
print("TYPE CONVERSIONS")
print("=" * 50)

conversions = [
    ("int → float",  int,   float,  42),
    ("float → int",  float, int,    3.99),
    ("str → int",    str,   int,    "123"),
    ("int → str",    int,   str,    456),
    ("int → bool",   int,   bool,   0),
    ("str → list",   str,   list,   "hello"),
]
for label, from_t, to_t, val in conversions:
    converted = to_t(val)
    print(f"  {label:15} {str(val):>8} ({from_t.__name__:5})"
          f"  →  {str(converted):>10} ({to_t.__name__})")
