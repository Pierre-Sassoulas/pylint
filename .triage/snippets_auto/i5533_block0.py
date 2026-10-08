from numpy import radians, degrees #  any ufunc will do
  
a=radians(90.0)
print ( "%6.3f"%( degrees(a),))
print ( "%6.3f"% degrees(a))

# ==>  [E1307(bad-string-format-type)] Argument '.ndarray' does not match format type 'f'

# even though the ufunc returns a float-compat arg in this case

# Note: using f-strings this is accepted:

print ( f"{degrees(a):6.3f}" )
