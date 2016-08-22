# nozoki
A module to programmatically read the memory of processes in Windows.

# Usage
```python
from nozoki import ProcessHandle

process = ProcessHandle("<title of window>")
address = 0xDEADBEEF
result = process.readInt(address)
```
