# wikipedia-solver
A Wikipedia Game solver in python using bidirectional bfs and the Wikipedia API.

# What is the Wikipedia game?
Wikipedia is an online encyclopedia written by volunteers. Each content page features hyperlinks to related articles to allow the user to quickly connect information between topics.  
The Wikipedia Game requires the user to move from a source page to a target page using only the hyperlinks on the page. Shorter solutions are usually preferred.  

# What is BFS? (Breadth First Search)
BFS is a searching algorithm that can be used to traverse a graph in its entirety, or to find a path from one node to another. It works by dequeuing nodes of a graph, fetching their neighbours, queueing the neighbours and marking them as explored, and repeating this process until the target nodes if found.  

This project uses an implementation of bidirectional BFS to reduce the total search space. This approach starts two BFS searches, one 'forward' from the start node and one 'in reverse' from the target node. I am also expanding the search frontier from the smallest queue to further optimize the search.  

# How can I run this?
The project features a `requirements.txt` document that enables you to run `pip install -r requirements.txt` in your Python virtual environment. This should install the dependencies required to run the program. You will also want to review the Wikipedia API etiquette suggestions to ensure that you query the API safely. Notably, the program attempts to read a file `header.txt` from the `resources` directory. You may change this as you please, but it is recommended to include an informative user agent string when querying the Wikipedia API.

# Further improvements
Further improvements could be made to the search algorithm.
* Caching explored pages for future runs.
* Implementing a heuristic, such as number of links, to prioritize promising pages first for dequeuing (Best First Search)

The most expensive operation in the process is fetching links from the Wikipedia API. Caching pages would make the process faster but is only beneficial for successive runs. I may implement this if I create an API for the service that runs more than one query in a session.
