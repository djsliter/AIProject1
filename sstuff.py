from neato import Genome

parent = Genome(4, 2)
parent.add_connection(0, 4, 0.37373773)
conn = parent.get_connection(0)
print(parent)
print(conn)