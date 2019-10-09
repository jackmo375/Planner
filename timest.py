#
#	Read task list from Quire
#	And produce a dependency graph,
#	annotated in time. 
#
######################################
import sys, tasks

#
#	This class is really bdly written! needs work.
#
class TaskEdges:

	def __init__(self,infile):
		instream = open(infile, "r")
		self.edges = []
		self.Nedges = 0
		while True:
			if instream.readline().find('/* Edges */')!=-1:
				break
		while True:
			rawline = instream.readline()
			if rawline.strip()=='}':# or rawline.strip()=='/* Ranks */':
				break
			else:
				self.edges += [rawline.strip()]
				self.Nedges += 1

	def printEdges(self):
		for i in range(self.Nedges):
			print(self.edges[i])

if __name__ == "__main__":

	tl = tasks.TaskList(sys.argv[1], status=sys.argv[2], subgraph=sys.argv[3])

	tl.beginGraph("G")
	print("/* Nodes */")
	tl.printGraphNodes(asrecords=True)
	print("/* Edges */")
	if sys.argv[4] != 'notfound':
		te = TaskEdges(sys.argv[4])
		te.printEdges()
	else:
		tl.printGraphEdges()
	print("/* Ranks */")
	tl.endGraph(-1)
