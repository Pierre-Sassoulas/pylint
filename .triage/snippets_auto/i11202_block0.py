"doc"
from pathlib import Path

Path('/tmp').read_text()				# unspecified-encoding
Path('/tmp').parents[0].read_text()		# unspecified-encoding

(Path('/') / 'tmp').read_text()			# No diagnostic
p: Path = Path('/') / 'tmp'				# Try with type annotation
p.read_text()							# No diagnostic
