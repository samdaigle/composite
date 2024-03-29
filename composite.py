from properties import t_deck, fpc, s, d, w_flange, t_flange, t_web, w_flange, fy


class Deck:
    def __init__(self, deck_c, deck_thickness, deck_width, strength):
        self.c = deck_c
        self.t_deck = deck_thickness
        self.width = deck_width * 12
        self.fpc = strength

    def beta(self):
        beta_1 = max(0.65, min(0.85, 0.85 - 0.05 * (self.fpc - 4)))
        return beta_1

    def a(self):
        a_pot = self.beta() * self.c
        a = min(self.t_deck, a_pot)
        return a

    def get_deck_compression(self):
        abba = self.a() * self.width
        c_c = 0.85 * (self.fpc)*(abba)
        return c_c

    def get_c_tft(self):
        return self.a() / 2

    def get_mp(self):
        return self.get_deck_compression * abs(self.get_c_tft - self.c)


class Beam:
    def __init__(self, depth, flange_width, flange_thick, web_thick, strength, deck_c, deck_thickness):
        self.depth = depth - (2 * flange_thick)
        self.b_f = flange_width
        self.t_f = flange_thick
        self.t_w = web_thick
        self.fy = strength
        self.c_totf = deck_thickness
        self.c = deck_c
        self.c_tow = self.c_totf + self.t_f
        self.c_tobf = self.c_tow + self.depth

    def top_flange_comp(self):
        a_tfc = min(self.t_f, max(0, self.c - self.c_totf))
        cs_tf = a_tfc * self.b_f * self.fy
        c_tfc = self.c_totf + (a_tfc / 2)
        return (cs_tf, c_tfc)

    def top_flange_ten(self):
        a_tft = min(self.t_f, max(0, (self.c_totf + self.t_f) - self.c))
        ts_tf = a_tft * self.b_f * self.fy
        c_tft = self.c_tow - (a_tft / 2)
        return (ts_tf, c_tft)

    def web_comp(self):
        a_wc = max(0, self.c - self.c_tow)
        cs_w = a_wc * self.t_w * self.fy
        c_wc = self.c_tow + (a_wc / 2)
        return (cs_w, c_wc)

    def web_ten(self):
        a_wt = min(self.depth, self.c_tow + self.depth - self.c)
        ts_w = a_wt * self.t_w * self.fy
        c_wt = self.c_tobf - a_wt
        return (ts_w, c_wt)

    def bot_flange_ten(self):
        ts_bf = self.t_f * self.b_f * self.fy
        c_bft = self.c_tobf - (self.t_f / 2)
        return (ts_bf, c_bft)


def get_compression(deck, beam):
    compression = deck.get_deck_compression() + beam.top_flange_comp()[0] + \
        beam.web_comp()[0]
    return round(compression, 0)


def get_tension(beam):
    tension = beam.top_flange_ten(
    )[0] + beam.web_ten()[0] + beam.bot_flange_ten()[0]
    return round(tension, 0)


def find_c(low=0, high=(t_deck + d)):
    c = ((high - low) / 2 + low)

    deck = Deck(c, t_deck, s, fpc)
    beam = Beam(d, w_flange, t_flange, t_web, fy, c, t_deck)
    compression = round(get_compression(deck, beam), 0)
    tension = round(get_tension(beam), 0)
    if compression == tension:
        print(f'c = {round(c, 2)} in.')
        print(f'tension = {tension} k')
        print(f'compression = {compression} k')
        return round(c, 2)
    elif compression > tension:
        high = c
        return find_c(low, high)
    else:
        low = c
        return find_c(low, high)


def plastic_moment(c, deck, beam):
    if find_c:
        mp_deck = deck.get_deck_compression() * (c - deck.get_c_tft())
        mp_tf = (beam.top_flange_ten()[0] * abs(beam.top_flange_ten()[1] - c)) + (
            beam.top_flange_comp()[0] * abs(beam.top_flange_comp()[1] - c))
        mp_w = (beam.web_ten()[0] * abs(beam.web_ten()[1] - c)) + (
            beam.web_comp()[0] * abs(beam.web_comp()[1] - c))
        mp_bf = beam.bot_flange_ten()[0] * abs(beam.bot_flange_ten()[1] - c)
        mp = round(0.9 * (mp_deck + mp_tf + mp_w + mp_bf) / 12, 0)
        print(f'Plastic moment (Φmₙ): {mp} k-ft')
        return mp
    print('Tension could not equal compression. Please check properties and try again.')


if __name__ == '__main__':
    print('\nResults: \n')
    c = find_c()
    deck = Deck(c, t_deck, s, fpc)
    beam = Beam(d, w_flange, t_flange, t_web, fy, c, t_deck)
    plastic_moment(c, deck, beam)
    print('\n')
