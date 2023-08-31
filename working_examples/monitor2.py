def main():
    # Initialize the current and previous versions of all nodes
    current = {'node1': False, 'node2': False, 'node3': False, 'node4': False, 'node5': False, 'node6': True, 'node7': True, 'node8': False}
    previous = current.copy()

    while True:
        # Get the event from the user
        event = input()
        if event == 'abort':
            break

        # Update the current versions of the leaf nodes based on the event
        for var, value in [pair.split('=') for pair in event.split(',')]:
            current[f'node{int(var[1])}'] = value == 'True'

        # Update the current versions of the non-leaf nodes
        current['node4'] = not current['node3']
        current['node5'] = not current['node2'] or current['node4']
        current['node6'] = current['node1'] and previous['node6']
        current['node7'] = current['node5'] and previous['node7']
        current['node8'] = current['node6'] and current['node7']

        # Update the previous versions of all nodes
        previous = current.copy()

        # Print the current version of the root node
        print(current['node8'])

if __name__ == '__main__':
    main()
