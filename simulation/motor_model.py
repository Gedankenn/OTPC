from dataclasses import dataclass
import numpy as np
import math

@dataclass(frozen=True)
class PMSMParameters:
    Rs: float
    Ld: float
    Lq: float
    lambda_f: float
    pole_pairs: int
    J: float
    B: float

class PMSM:
    def __init__(self, params: PMSMParameters):
        self.p = params

        # State vector: [id, iq, omega_m, theta_e]
        self.x = np.zeros(4)

    def electrical_dynamics(self, v_d, v_q):
        id_, iq, omega_m, _ = self.x
        p = self.p

        omega_e = p.pole_pairs * omega_m

        did = (
            -p.Rs / p.Ld * id_              # -Rs/Ld * id
            + omega_e * p.Lq / p.Ld * iq    # +ωe Lq/Ld * iq
            + v_d / p.Ld                    # +vd/Ld
        )


        diq = (
            -p.Rs / p.Lq * iq               # -Rs/Lq * iq
            - omega_e * p.Ld / p.Lq * id_   # -ωe Ld/Lq * id
            - omega_e * p.lambda_f / p.Lq   # -ωe λf/Lq
            + v_q / p.Lq                    # +vq/Lq
        )

        return did, diq

    def torque(self):
        id_, iq, _, _ = self.x
        p = self.p

        return 1.5 * p.pole_pairs * (
            p.lambda_f * iq + (p.Ld - p.Lq) * id_ * iq
        )

    def mechanical_dynamics(self, T_load):
        _, _, omega_m, _ = self.x
        p = self.p

        domega = (self.torque() - T_load - p.B * omega_m) / p.J
        return domega

    def step(self, v_d, v_q, T_load, dt):
        did, diq = self.electrical_dynamics(v_d, v_q)
        domega = self.mechanical_dynamics(T_load)

        self.x[0] += did * dt
        self.x[1] += diq * dt
        self.x[2] += domega * dt
        self.x[3] += self.p.pole_pairs * self.x[2] * dt

def clarke(a, b):
    alpha = a
    beta = (a + 2.0 * b) / 1.7320508075688772
    return alpha, beta

def park(alpha, beta, theta):
    c = math.cos(theta)
    s = math.sin(theta)

    d =  c * alpha + s * beta
    q = -s * alpha + c * beta
    return d, q

def inv_park(d, q, theta):
    c = math.cos(theta)
    s = math.sin(theta)

    alpha = c * d - s * q
    beta  = s * d + c * q
    return alpha, beta
