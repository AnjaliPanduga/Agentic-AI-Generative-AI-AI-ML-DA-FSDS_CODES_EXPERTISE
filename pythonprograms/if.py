n=int(input())
m=int(input())
operator=input()
if operator=="+":
    print(f"perform add operation{n}+{m}")
elif operator=="-":
    print("perform sub operation")
elif operator=="*":
    print("perform mult operation")
elif operator=="/":
    print("perform the div operation")
else:
    print("print INVALID operation")
