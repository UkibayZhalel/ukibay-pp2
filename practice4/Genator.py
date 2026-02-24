def echo_generator():
  while True:
    received = yield
    print("Received:", received)

gen = echo_generator()
next(gen)  # Prime the generator
gen.send("Hello")
gen.send("World")
