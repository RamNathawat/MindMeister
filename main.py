import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import networkx as nx

def parse_text(text):
    lines = text.strip().split('\n')
    hierarchy = {}
    stack = []
    current_level = -1

    for line in lines:
        stripped = line.lstrip()
        level = (len(line) - len(stripped)) // 4  # Assuming each level is indented by 4 spaces

        if level > current_level:
            stack.append(stripped)
        elif level == current_level:
            stack.pop()
            stack.append(stripped)
        else:
            while len(stack) > level + 1:
                stack.pop()
            stack.pop()
            stack.append(stripped)

        parent = stack[-2] if len(stack) > 1 else None
        if parent:
            if parent not in hierarchy:
                hierarchy[parent] = []
            hierarchy[parent].append(stripped)
        else:
            current_node = stripped

        current_level = level

    return current_node, hierarchy

def add_edges(graph, node, hierarchy):
    if node in hierarchy:
        for child in hierarchy[node]:
            graph.add_edge(node, child)
            add_edges(graph, child, hierarchy)

def create_mindmap(text):
    root, hierarchy = parse_text(text)
    G = nx.DiGraph()
    G.add_node(root)
    add_edges(G, root, hierarchy)
    return G

def graph_to_cytoscape_elements(G):
    elements = []
    for node in G.nodes:
        elements.append({'data': {'id': node, 'label': node}})
    for edge in G.edges:
        elements.append({'data': {'source': edge[0], 'target': edge[1]}})
    return elements

app = dash.Dash(__name__)

text = """
Main Topic
    Component Life Cycle
    Lists and Keys
    Composition vs Inheritance
    Events
    Basic Hooks
        useState
        useEffect
    High Order Components
        Portals
        Error Boundaries
        Fiber Architecture
    Forms
    Testing
"""

G = create_mindmap(text)
elements = graph_to_cytoscape_elements(G)

stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'width': '190px',
            'height': '50px',
            'background-color': '#0074D9',
            'color': 'white',
            'font-size': '16px',
            'text-valign': 'center',
            'text-halign': 'center',
            'shape': 'round-rectangle',
            'padding': '10px'
        }
    },
    {
        'selector': '[label ^= "use"]',
        'style': {
            'background-color': '#FF4136',
            'font-size': '14px'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'width': 2,
            'line-color': '#0074D9',
            'target-arrow-color': '#0074D9',
            'target-arrow-shape': 'triangle'
        }
    },
    {
        'selector': '[source = "High Order Components"]',
        'style': {
            'line-color': '#2ECC40',
            'target-arrow-color': '#2ECC40'
        }
    },
    {
        'selector': '[source = "Forms"]',
        'style': {
            'line-color': '#FF851B',
            'target-arrow-color': '#FF851B'
        }
    },
    {
        'selector': 'node:parent',
        'style': {
            'background-opacity': 0.333
        }
    }
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-mindmap',
        elements=elements,
        layout={'name': 'breadthfirst', 'roots': ['Main Topic']},
        style={'width': '100%', 'height': '600px', 'background-color': '#1e1e1e'},
        stylesheet=stylesheet
    ),
    html.Div([
        dcc.Input(id='new-node-label', type='text', placeholder='New node label'),
        dcc.Dropdown(id='parent-node-dropdown', placeholder='Select parent node'),
        html.Button('Add Node', id='add-node-button', n_clicks=0),
    ], style={'marginTop': '20px'}),
    html.Div(id='node-info', style={'marginTop': '20px', 'color': 'white'})
])

@app.callback(
    Output('cytoscape-mindmap', 'elements'),
    Output('parent-node-dropdown', 'options'),
    Input('add-node-button', 'n_clicks'),
    State('new-node-label', 'value'),
    State('parent-node-dropdown', 'value'),
    State('cytoscape-mindmap', 'elements')
)
def add_node(n_clicks, new_label, parent_label, elements):
    if n_clicks > 0 and new_label and parent_label:
        elements.append({'data': {'id': new_label, 'label': new_label}})
        elements.append({'data': {'source': parent_label, 'target': new_label}})
    node_options = [{'label': el['data']['label'], 'value': el['data']['id']} for el in elements if 'source' not in el['data']]
    return elements, node_options

@app.callback(
    Output('cytoscape-mindmap', 'layout'),
    Input('cytoscape-mindmap', 'tapNodeData')
)
def display_tap_node_data(data):
    if data:
        return {'name': 'breadthfirst', 'roots': [data['id']]}
    return {'name': 'breadthfirst', 'roots': ['Main Topic']}

@app.callback(
    Output('node-info', 'children'),
    Input('cytoscape-mindmap', 'tapNodeData')
)
def display_node_info(data):
    if data:
        return f"You clicked on node: {data['label']}"
    return "Click a node to see its details."

if __name__ == '__main__':
    app.run_server(debug=True)
