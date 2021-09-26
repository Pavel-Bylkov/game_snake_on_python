a = 20
expr = "start"
while expr != "":
    expr = input("> ")
    if expr != "":
        print("= ", eval(expr))
