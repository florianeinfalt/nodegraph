def print_node(node):
    width = max([
        len(node.name + node.engine) + 3,
        len(node.id),
        max(([len(in_.name) for in_ in node.inputs.values()] or [0])),
        max(([len(put_.name) for put_ in node.outputs.values()] or [0]))
    ]) + 2
    repr_ = '+' + '-' * width + '+'
    repr_ += '\n'
    repr_ += '| {name} ({engine}){padding}|'.format(
        name=node.name.upper(),
        engine=node.engine,
        padding=' ' * ((width - len(node.name + node.engine)) - 4))
    repr_ += '\n'
    # repr_ += '| {engine}{padding}|'.format(
    #     engine=node._engine,
    #     padding=' ' * ((width - len(node.engine)) - 1))
    # repr_ += '\n'
    repr_ += '| {id}{padding}|'.format(
        id=node.id,
        padding=' ' * ((width - len(node.id)) - 1))
    repr_ += '\n'
    repr_ += '+' + '-' * width + '+'
    repr_ += '\n'
    for input_ in sorted(node.inputs.values(), key=lambda x: x.name):
        repr_ += print_plug(input_, width, input_=True)
    for output_ in sorted(node.outputs.values(), key=lambda x: x.name):
        repr_ += print_plug(output_, width, input_=False)
    repr_ += '+' + '-' * width + '+'
    repr_ += '\n'
    return repr_


def print_plug(plug, width, input_=True):
    is_conn = plug.is_connected

    repr_ = ''
    if input_:
        repr_ += 'o {name}{is_connected}{padding}|'.format(
            name=plug.name,
            is_connected=' *' if is_conn else '',
            padding=' ' * (width - len(plug.name) - (3 if is_conn else 1)))
    else:
        repr_ += '|{padding}{is_connected}{name} o'.format(
            name=plug.name,
            is_connected='* ' if is_conn else '',
            padding=' ' * (width - len(plug.name) - (3 if is_conn else 1)))
    repr_ += '\n'
    return repr_
