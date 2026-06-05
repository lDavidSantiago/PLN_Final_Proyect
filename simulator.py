class Simulator:
	"""
	Generates the OS command string from the semantic representation.

	Accepts a dict (simple command) or a list of dicts (compound command).
	Returns str or list of str respectively.
	"""

	# Action mapping:
	#   mkdir  ->  mkdir <name>
	#   rm     ->  rm [-r] <target>
	#   mv     ->  mv <source> <destination>   (move or rename)
	#   cp     ->  cp <source> <destination>
	#   ls     ->  ls [pattern]

	def generate(self, semantic):
		"""
		Generates the OS command string.

		Returns:
			str       if semantic is a dict
			list[str] if semantic is a list of dicts
		"""
		if isinstance(semantic, list):
			return [self._cmd(item) for item in semantic]
		return self._cmd(semantic)

	def show(self, semantic):
		"""Prints the simulator result with a header."""
		result = self.generate(semantic)
		print("── Simulated command ──")
		if isinstance(result, list):
			for i, cmd in enumerate(result, 1):
				print(f"  [{i}] {cmd}")
		else:
			print(f"  {result}")
		print()

	# Dispatch by action
	def _cmd(self, semantic):
		action = semantic.get('action')
		verb = semantic.get('verb')
		object_type = semantic.get('object_type')
		name = semantic.get('name')
		extension = semantic.get('extension')
		destination = semantic.get('destination')

		if action == 'mkdir':
			return self._mkdir(name)
		elif action == 'rm':
			return self._rm(object_type, name, extension, destination)
		elif action == 'mv':
			if verb == 'rename':
				return self._rename(name, extension, destination)
			else:
				return self._move(name, extension, destination)
		elif action == 'cp':
			return self._copy(name, extension, destination)
		elif action == 'ls':
			return self._list(object_type, extension)
		return f"# unrecognized action: {action}"

	# Generators 
	def _mkdir(self, name):
		directory_name = name or 'new_folder'
		return f"mkdir {directory_name}"

	def _rm(self, object_type, name, extension, destination):
		# Case: specific file with extension (e.g. report.pdf)
		if name and extension:
			return f"rm {name}.{extension}"
		# Case: name without extension (folder or file without ext)
		if name:
			if object_type == 'folder':
				return f"rm -r {name}"
			return f"rm {name}"
		# Case: destination resolved as location - all files in folder
		if destination:
			return f"rm {destination}/*"
		# Case: extension only - all files with that extension
		if extension:
			return f"rm *.{extension}"
		return "rm *"

	def _move(self, name, extension, destination):
		source = self._source(name, extension)
		target = f"{destination}/" if destination else "."
		return f"mv {source} {target}"

	def _rename(self, name, extension, destination):
		source = name + (f".{extension}" if extension else "")
		target = destination or "new name"
		return f"mv {source} {target}"

	def _copy(self, name, extension, destination):
		source = self._source(name, extension)
		target = f"{destination}/" if destination else "."
		return f"cp {source} {target}"

	def _list(self, object_type, extension):
		if extension:
			return f"ls *.{extension}"
		if object_type == 'folder':
			return "ls -d */"
		return "ls"

	def _source(self, name, extension):
		"""Builds the source pattern for mv and cp."""
		if name and extension:
			return f"{name}.{extension}"
		if name:
			return name
		if extension:
			return f"*.{extension}"
		return "*"


# Test cases
if __name__ == '__main__':
	simulator = Simulator()

	cases = [
		("mkdir folder",            {'action': 'mkdir', 'name': 'projects'}),
		("rm folder",               {'action': 'rm',    'verb': 'delete',   'object_type': 'folder', 'name': 'old',     'extension': None,  'destination': None}),
		("rm files .pdf",           {'action': 'rm',    'verb': 'delete',   'object_type': 'file', 'name': None,      'extension': 'pdf', 'destination': None}),
		("rm folder/* (SP)",        {'action': 'rm',    'verb': 'delete',   'object_type': 'file', 'name': None,      'extension': None,  'destination': 'documents'}),
		("mv *.pdf to projects",    {'action': 'mv',    'verb': 'move',     'object_type': 'file', 'name': None,      'extension': 'pdf', 'destination': 'projects'}),
		("mv rename",               {'action': 'mv',    'verb': 'rename',   'object_type': 'folder', 'name': 'old',     'extension': None,  'destination': 'new'}),
		("cp *.txt to backup",      {'action': 'cp',    'verb': 'copy',     'object_type': 'file', 'name': None,      'extension': 'txt', 'destination': 'backup'}),
		("ls files",                {'action': 'ls',    'object_type': 'file', 'extension': None}),
		("ls *.pdf",                {'action': 'ls',    'object_type': 'file', 'extension': 'pdf'}),
		("ls folders",              {'action': 'ls',    'object_type': 'folder', 'extension': None}),
		("compound",                [
			{'action': 'mkdir', 'name': 'data'},
			{'action': 'mv',    'verb': 'move', 'object_type': 'file', 'name': None, 'extension': 'csv', 'destination': 'data'},
		]),
	]
	# Test cases
	simulator = Simulator()



for description, semantic in cases:
	result = simulator.generate(semantic)
	print(f"  {description:<30} ->  {result}")



'''
simulator.show({'action': 'mkdir', 'name': 'projects'})
simulator.show({'action': 'rm', 'verb': 'delete', 'object_type': 'folder', 'name': 'old', 'extension': None, 'destination': None})
simulator.show({'action': 'mv', 'verb': 'move', 'object_type': 'file', 'name': None, 'extension': 'pdf', 'destination': 'projects'})
simulator.show({'action': 'cp', 'verb': 'copy', 'object_type': 'file', 'name': None, 'extension': 'txt', 'destination': 'backup'})
simulator.show([
	{'action': 'mkdir', 'name': 'data'},
	{'action': 'mv', 'verb': 'move', 'object_type': 'file', 'name': None, 'extension': 'csv', 'destination': 'data'},
])'
'''