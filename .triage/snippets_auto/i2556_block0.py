import cppmod

print("cppmod:", cppmod.func())
print("Outer :", cppmod.Outer.func())
print("Inner :", cppmod.Outer.Inner.func())
