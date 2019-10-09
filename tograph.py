#
#	Read task list from Quire
#	And produce a dependency graph.
#
######################################
import sys, tasks

if __name__ == "__main__":

	tl = tasks.TaskList(sys.argv[1], status=sys.argv[2], subgraph=sys.argv[3])
	tl.printGraph()
