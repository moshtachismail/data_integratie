with open('CT1-All.pdf', 'rb') as f:
    for line in f:
        if line.startswith('#'):
            next
        