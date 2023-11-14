from Functions import saturation_vapor_pressure_at

class Thermal_Model:

    c_cr = 0.97*78.3
    c_sk = 0.97*3.4
    k_min = 5.28
    normal_V_bl = 6.3
    def __init__(self, env_Factor):
        self.T_sk = 34.1
        self.T_cr = 36.6
        self.E_rsw = 0
        self.m_rsw = 0
        self.V_bl = Thermal_Model.normal_V_bl
        self.env_Factor = env_Factor
        self.E_res = 0.0023*self.env_Factor.met*(44 - self.env_Factor.phi*saturation_vapor_pressure_at(self.env_Factor.db_T))
        self.E_dif = 5
        self.E = self.E_rsw + self.E_res +self.E_dif
        self.F_cl = 1/(1+0.155*self.env_Factor.h*self.env_Factor.clo)
        self.F_pcl = 1/(1+0.143*self.env_Factor.h_c*self.env_Factor.clo)

    def heat_balance(self):

        self.E_rsw = 0.7*self.m_rsw*(2**((self.T_sk-34.1)/3))
        E_max = 2.2*self.env_Factor.h_c*(saturation_vapor_pressure_at(self.T_sk) - self.env_Factor.phi*saturation_vapor_pressure_at(self.env_Factor.db_T))*self.F_pcl
        if E_max > self.E_rsw:
            P_rsw = self.E_rsw/E_max
            P_wet = (0.06 + 0.94*P_rsw)
            self.E_dif = P_wet * E_max - self.E_rsw
            self.E = self.E_rsw + self.E_res +self.E_dif
        else:
            self.E_rsw = E_max
            self.E = self.E_res + self.E_rsw
            self.E_dif = 0

        S_cr = self.env_Factor.met - (self.T_cr - self.T_sk)*(Thermal_Model.k_min + 1.163*self.V_bl) - self.E_res - self.env_Factor.work
        S_sk = (self.T_cr - self.T_sk)*(Thermal_Model.k_min + 1.163*self.V_bl) - self.env_Factor.h*(self.T_sk - self.env_Factor.db_T)*self.F_cl - (self.E_rsw + self.E_dif)

        dT_cr = (S_cr*2)/Thermal_Model.c_cr
        dT_sk = (S_sk*2)/Thermal_Model.c_sk

        dt = 1/60
        while abs(dT_cr)*dt >= 0.1 or abs(dT_sk)*dt >= 0.1:
            dt = dt/2

        self.T_cr = self.T_cr + dT_cr*dt
        self.T_sk = self.T_sk + dT_sk*dt

        return dt

    def self_control(self, dt):

                ### control blood flow ###

        cr_sig = self.T_cr - 36.6
        sk_sig = self.T_sk - 34.1
        if cr_sig <= 0:
            cr_cold = cr_sig
            cr_warm = 0
        else:
            cr_cold = 0
            cr_warm = cr_sig
        if sk_sig <= 0:
            sk_cold = sk_sig
            sk_warm = 0
        else:
            sk_cold = 0
            sk_warm = sk_sig

        self.V_bl = (Thermal_Model.normal_V_bl + 75*cr_warm)/(1 - 0.5*sk_cold)

                ### control sweating ###

        if self.env_Factor.met < 60:
            self.m_rsw = 100*cr_warm*sk_warm
        else:
            self.m_rsw = 250*cr_warm + 100*cr_warm*sk_warm


'''
    def self_control(self, dt):
        cr_sig = self.T_cr - 36.6
        sk_sig = self.T_sk - 34.1
        if cr_sig <= 0:
            cr_cold = cr_sig
            cr_warm = 0
        else:
            cr_cold = 0
            cr_warm = cr_sig
        if sk_sig <= 0:
            sk_cold = sk_sig
            sk_warm = 0
        else:
            sk_cold = 0
            sk_warm = sk_sig

        self.V_bl = (Thermal_Model.normal_V_bl + 75*cr_warm)/(1 - sk_cold)

                ### control sweating ###

        if self.env_Factor.met < 60:
            m_rsw = 100*cr_warm*sk_warm
        else:
            m_rsw = 250*cr_warm + 100*cr_warm*sk_warm

        self.E_rsw = 0.7*m_rsw*(2**((self.T_sk-34.1)/3))
        self.W_rsw = self.W_rsw +(self.E_rsw*2/(0.7*100))*dt
        E_max = 2.2*self.env_Factor.h_c*(saturation_vapor_pressure_at(self.T_sk) - self.env_Factor.phi*saturation_vapor_pressure_at(self.env_Factor.db_T))*self.F_pcl
        P_rsw = self.E_rsw/E_max
        P_wet = (0.06 + 0.94*P_rsw)
        self.E_dif = P_wet * E_max - self.E_rsw
        self.E = self.E_rsw + self.E_res +self.E_dif

        if self.E_rsw > E_max:
            self.E = self.E_res + self.E_rsw
            self.E_rsw = E_max
            self.E_dif = 0
            '''


