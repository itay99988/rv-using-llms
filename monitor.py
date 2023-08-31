def update_nodes(nodes, event):
    # Update current versions
    nodes['node1']['current'] = event['q1']
    nodes['node2']['current'] = event['q2']
    nodes['node3']['current'] = event['q3']
    nodes['node4']['current'] = not nodes['node3']['current']
    nodes['node5']['current'] = not nodes['node2']['current'] or nodes['node4']['current']
    nodes['node6']['current'] = nodes['node1']['current'] and nodes['node6']['previous']
    nodes['node7']['current'] = nodes['node5']['current'] and nodes['node7']['previous']
    nodes['node8']['current'] = nodes['node6']['current'] and nodes['node7']['current']
    
    # Update previous versions
    for node in nodes.values():
        node['previous'] = node['current']
    return nodes

def main():
    nodes = {
        'node1': {'current': False, 'previous': False},
        'node2': {'current': False, 'previous': False},
        'node3': {'current': False, 'previous': False},
        'node4': {'current': False, 'previous': False},
        'node5': {'current': False, 'previous': False},
        'node6': {'current': True, 'previous': True},
        'node7': {'current': True, 'previous': True},
        'node8': {'current': False, 'previous': False},
    }
    
    while True:
        event_str = input()
        if event_str == 'abort':
            break
        event = dict(item.split('=') for item in event_str.split(','))
        for key in event:
            event[key] = event[key] == 'True'
        nodes = update_nodes(nodes, event)
        print(nodes['node8']['current'])

if __name__ == "__main__":
    main()
