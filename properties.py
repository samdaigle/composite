from beam_data import df


def get_input(question):
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


def get_beam():
    while True:
        try:
            beam_name = input('WF beam size (ex. W12x30): ').lower()

            if beam_name not in df.index:
                raise ValueError
        except ValueError:
            print('Please input a valid WF beam size.')
            continue
        break
    return beam_name


questions = {
    't_deck': 'Concrete deck thickness (in.): ',
    'fpc': 'Concrete design strength (ksi): ',
    's': 'Beam spacing (ft.): ',
    'fy': 'Yeild strenght of steel (ksi): '
}

t_deck = get_input(questions['t_deck'])
fpc = get_input(questions['fpc'])
s = get_input(questions['s'])
fy = get_input(questions['fy'])
beam = get_beam()
d = df.at[beam, 'Depth']
w_flange = df.at[beam, "Width"]
t_flange = df.at[beam, "Flange Thickness"]
t_web = df.at[beam, 'Web Thickness']
