def get_input(component, question):
    while True:
        try:
            component = float(input(question))

            if component <= 0:
                raise ValueError

        except ValueError:
            print('Please input a positive integer.')
            continue
        break

    return component


t_deck = 0
fpc = 0
s = 0
d = 0
w_flange = 0
t_flange = 0
t_web = 0
fy = 0
questions = {
    't_deck': 'Concrete deck thickness (in.): ',
    'fpc': 'Concrete design strength (ksi): ',
    's': 'Beam spacing (ft.): ',
    'd': 'Beam depth (in.): ',
    'w_flange': 'Flange width (in.): ',
    't_flange': 'Flange thickness (in.): ',
    't_web': 'Web thickness (in.): ',
    'fy': 'Yeild strenght of steel (ksi): '
}

t_deck = get_input(t_deck, questions['t_deck'])
fpc = get_input(fpc, questions['fpc'])
s = get_input(s, questions['s'])
d = get_input(d, questions['d'])
w_flange = get_input(w_flange, questions['w_flange'])
t_flange = get_input(t_flange, questions['t_flange'])
t_web = get_input(t_web, questions['t_web'])
fy = get_input(fy, questions['fy'])
