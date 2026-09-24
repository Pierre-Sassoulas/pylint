print("d" + (f"{s1}" if (s1 := "x") else ""))

print((f"{s2}" if (s2 := "x") else "") + "d")

print(f"{s3}" if (s3 := "x") else "")
