class Enverionmental_Factor:

    def __init__(self, met, h_r, h_c, clo, db_T, phi, mu):
        self.met = met
        self.h_r = h_r
        self.h_c = h_c
        self.h = h_r + h_c
        self.clo = clo
        self.db_T = db_T
        self.phi = phi
        self.mu = mu
        self.work = self.met * self.mu