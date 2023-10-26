from IPython.display import HTML
import requests
from IPython.display import display
import requests
import networkx as nx
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def anzeigen(user):
    
    username = user['username']
    ice = user['FavIce']
    hobby = user['Hobbies']
    shoe = user['Shoesize']
    age = user['Age']
    pfp = "http://127.0.0.1:8000/media/profile_pictures/" + (user['Profile_pic'].split("profile_pictures")[-1])
    html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    img.fixed {{
                        border: 5px outset lightgray;
                        border-radius: 2%;
                        width: 100%;
                        max-width: 100%; /* Ensure the image doesn't exceed its container */
                    }}

                    /* CSS for the username */
                    .username {{
                        font-size: 14px;
                        /* Add any other username styles here */
                    }}

                    .divider2 {{
                        flex: 0 0 10%; /* 10% width for the divider, doesn't grow or shrink */
                        background-color: #FFF; /* Change the color as needed */
                    }}

                    .container2 {{
                        display: flex;
                        width: 100%;
                    }}

                    .column2 {{
                        flex: 1; /* Automatically distribute remaining space */
                        padding: 10px; /* Optional padding for spacing */
                        /* text-align: center; Remove this line if you don't want center alignment */
                    }}
                </style>
            </head>
            <body>
                <div class="container2">
                    <div class="column2" style="flex: 3;"> <!-- 30% width -->
                        <img src="{pfp}" alt="Profile Picture" class="fixed">
                    </div>
                    <div class="divider2"></div> <!-- 10% divider -->
                    <div class="column2" style="flex: 6;"> <!-- 60% width -->
                        <!-- Replace {username} with the actual username -->
                        <h2 style="font-family: Arial, sans-serif; color: #142b58" class="username">{username}</h2>
                        <table class="table">
                            <tr>
                                <td class="table-label">Alter</td>
                                <td>{age}</td>
                            </tr>
                            <tr>
                                <td class="table-label">Lieblingseis</td>
                                <td>{ice}</td>
                            </tr>
                            <tr>
                                <td class="table-label">Hufgröße</td>
                                <td>{shoe}</td>
                            </tr>
                            <tr>
                                <td class="table-label">Hobbies</td>
                                <td>{hobby}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </body>
            </html>

                    """

    return display(HTML(html_content))
    
    
    
def getInfo(user_id):
    
    url = f"http://127.0.0.1:8000/user/{user_id}/json"
    response = requests.get(url)

    if response.status_code == 200:
        user = response.json()
        
        url = f"http://127.0.0.1:8000/user/{user_id}/friends"
        response = requests.get(url)

        if response.status_code == 200:
            friends = response.json()
            user['friends'] = friends['friends']
            user['friends_names'] = []
            
            for friend in friends['friends']:
                url = f"http://127.0.0.1:8000/user/{friend}/json"
                response = requests.get(url)
                
                if response.status_code == 200:
                    new_user = response.json()
                    
                    user['friends_names'].append(new_user['username'])
            
            return dotdict(user)
    
    else:
        print(f"Fehler! Konnte keine Daten für UserID {user_id} laden.")
        
        
        
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
    
class Netzwerk:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def add_edges(self, edges):
        self.graph.add_edges_from(edges)
        
    def anzeigen(self, markieren=None):
    # Create an interactive plot
        x_e = []
        y_e = []
        x_n = []
        y_n = []
        node_names = []

        # Calculate the positions of nodes in the graph
        pos = nx.spring_layout(self.graph)

        for node, position in pos.items():
            x, y = position[0], position[1]
            x_n.append(x)
            y_n.append(y)
            node_info = getInfo(node)
            username = node_info.username
            node_names.append((node, username))

        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            x_e += [x0, x1, None]
            y_e += [y0, y1, None]

        if markieren == None:
            node_trace = go.Scatter(
                x=x_n,
                y=y_n,
                text=[f"UserID: {id} <br> Username: {username}" for id, username in node_names],
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    size=10,
                    color=1
                )
            )
        else:
            node_trace = go.Scatter(
                x=x_n,
                y=y_n,
                text=[f"UserID: {id} <br> Username: {username}" for id, username in node_names],
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    size=10,
                    color=[int(username == markieren) for id, username in node_names]
                )
            )
            

        edge_trace = go.Scatter(
            x=x_e,
            y=y_e,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines')

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(edge_trace)
        fig.add_trace(node_trace)
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            title_text="Social Network Graph"
        )

        fig.show()


