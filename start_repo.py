from bottle import Bottle, run, static_file, request, template
import os
import threading

from ete4 import Tree
from treeprofiler import tree_plot
from treeprofiler.src import utils
from treeprofiler import layouts

app = Bottle()

# Root folder where tree files are stored
TREE_FOLDER = "/home/deng/Projects/metatree_drawer/treeprofiler_test/claudia_tree/thesis"

# Serve the homepage
@app.route('/')
def index():
    return static_file('index.html', root='./static')

# Serve static files (CSS, JavaScript)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

# API endpoint to retrieve categorized tree data
@app.route('/api/trees', method='GET')
def get_trees():
    global treeid2tree
    treeid2tree = {}
    tree_data = {
        "01-crs_gtdb": [
            {"id": 1, "name": "gtdb_r207_genus_crs", "path": f"{TREE_FOLDER}/01-crs_gtdb/genus/gtdb_r207_genus_crs.nw", "url": "http://localhost:5001"},
            {"id": 2, "name": "gtdb_r207_order_crs.nw", "path": f"{TREE_FOLDER}/01-crs_gtdb/order/gtdb_r207_order_crs.nw", "url": "http://localhost:5002"},
            {"id": 3, "name": "gtdb_r207_phylum_crs.nw", "path": f"{TREE_FOLDER}/01-crs_gtdb/phylum/gtdb_r207_phylum_crs.nw", "url": "http://localhost:5003"}
        ],
        "02-globalcr_mcpsignal": [
            {
                "id": 4, 
                "name": "Globalcr_MCPsignal", 
                "path": f"{TREE_FOLDER}/02-globalcr_mcpsignal/mcpsignal_globalcr_lca.nw", 
                "url": "http://localhost:5011"
            }
        ],
        "03-capture_mcpsignal": [
            {
                "id": 5, 
                "name": "Capture_MCPsignal", 
                "path": f"{TREE_FOLDER}/03-capture_mcpsignal/MCPsignal_all_gtdbr207.faa.dedup.alg_annotated_dups_collapsing.nw",
                "url": "http://localhost:5012"
            }
        ]
    }
    #treeid2tree[1] = Tree(open(tree_data["01-crs_gtdb"][1]["path"]), parser=1)
    return {"categories": tree_data}


@app.route('/tree/<tree_id:int>')
def view_tree(tree_id):
    # Map tree IDs to file paths and corresponding URLs
    tree_files = {
        1: {"path": f"{TREE_FOLDER}/01-crs_gtdb/genus/gtdb_r207_genus_crs.nw", "url": "http://localhost:5001"},
        2: {"path": f"{TREE_FOLDER}/01-crs_gtdb/order/gtdb_r207_order_crs.nw", "url": "http://localhost:5002"},
        3: {"path": f"{TREE_FOLDER}/01-crs_gtdb/phylum/gtdb_r207_phylum_crs.nw", "url": "http://localhost:5003"},
        4: {"path": f"{TREE_FOLDER}/02-globalcr_mcpsignal/mcpsignal_globalcr_lca.nw", "url": "http://localhost:5011"},
        5: {"path": f"{TREE_FOLDER}/03-capture_mcpsignal/MCPsignal_all_gtdbr207.faa.dedup.alg_annotated_dups_collapsing.nw", "url": "http://localhost:5012"}
    }
    
    # Get the file path and URL for the given tree ID
    tree_info = tree_files.get(tree_id)
    if not tree_info or not os.path.exists(tree_info["path"]):
        return "Tree not found", 404

    tree_name = os.path.basename(tree_info["path"])
    url_link = tree_info["url"]

    # Render the tree detail page with iframe
    return template('./static/tree_detail.html', tree_name=tree_name, tree_id=tree_id, url_link=url_link)

# def start_explore_thread(t, treename, current_layouts, current_props):
#     """
#     Starts the ete exploration in a separate thread.
#     """

#     def explore():
#         t.explore(name=treename, layouts=current_layouts, port=5051, open_browser=False, include_props=current_props)
    
#     explorer_thread = threading.Thread(target=explore)
#     explorer_thread.start()

# Run the app
if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=True)