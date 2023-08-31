def main():
    # Initialize the previous and current versions of each node
    prev = {'node1': False, 'node2': False, 'node3': True, 'node4': False}
    curr = {'node1': False, 'node2': False, 'node3': True, 'node4': False}

    while True:
        # Get the next event from the user
        event = input()

        # Terminate if the user entered "abort"
        if event == 'abort':
            break

        # Parse the event into a dictionary of variable assignments
        assignments = dict(item.split('=') for item in event.split(','))

        # Update the current version of each node
        curr['node1'] = assignments['q1'] == 'True'
        curr['node2'] = assignments['q2'] == 'True'
        curr['node3'] = curr['node1'] and prev['node3']
        curr['node4'] = curr['node3'] or (curr['node2'] and prev['node4'])

        # Print the current version of the root node
        print(curr['node4'])

        # Update the previous version of each node
        for node in prev:
            prev[node] = curr[node]


if __name__ == '__main__':
    main()
