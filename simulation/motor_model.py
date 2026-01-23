from dataclasses import dataclass
import numpy as np
import math


# ============================================================
# Motor physical parameters (constant – like a datasheet)
# ============================================================
@dataclass(frozen=True)
class PMSMParameters:
    Rs: float          # Stator phase resistance [ohm]
    Ld: float          # d-axis inductance [H]
    Lq: float          # q-axis inductance [H]
    lambda_f: float    # Permanent magnet flux linkage [Wb]
    pole_pairs: int    # Number of pole pairs
    J: float           # Rotor inertia [kg·m²]
    B: float           # Viscous friction coefficient [N·m·s]


# ============================================================
# PMSM dynamic model (dq reference frame)
# ============================================================
class PMSM:
    def __init__(self, params: PMSMParameters):
        self.p = params

        # State vector:
        # x[0] = id        d-axis current [A]
        # x[1] = iq        q-axis current [A]
        # x[2] = omega_m  mechanical speed [rad/s]
        # x[3] = theta_e  electrical rotor angle [rad]
        self.x = np.zeros(4)

    # --------------------------------------------------------
    # Electrical subsystem (current derivatives)
    # --------------------------------------------------------
    def electrical_dynamics(self, v_d, v_q):
        """
        Computes di_d/dt and di_q/dt from the PMSM voltage equations
        in the rotating dq reference frame.
        """

        id_, iq, omega_m, _ = self.x
        p = self.p

        # Electrical angular speed [rad/s]
        # omega_e = pole_pairs * mechanical_speed
        omega_e = p.pole_pairs * omega_m

        # d-axis current derivative
        #
        # Ld * did/dt = vd - Rs*id + omega_e*Lq*iq
        did = (
            - (p.Rs / p.Ld) * id_            # Resistive voltage drop
            + (omega_e * p.Lq / p.Ld) * iq   # Cross-coupling from q-axis
            + (v_d / p.Ld)                   # Applied d-axis voltage
        )

        # q-axis current derivative
        #
        # Lq * diq/dt = vq - Rs*iq - omega_e*(Ld*id + lambda_f)
        diq = (
            - (p.Rs / p.Lq) * iq             # Resistive voltage drop
            - (omega_e * p.Ld / p.Lq) * id_  # Cross-coupling from d-axis
            - (omega_e * p.lambda_f / p.Lq) # Back-EMF from permanent magnets
            + (v_q / p.Lq)                   # Applied q-axis voltage
        )

        return did, diq

    # --------------------------------------------------------
    # Electromagnetic torque
    # --------------------------------------------------------
    def torque(self):
        """
        Computes electromagnetic torque produced by the motor.
        Includes both magnet torque and reluctance torque.
        """

        id_, iq, _, _ = self.x
        p = self.p

        return (
            1.5 * p.pole_pairs *
            (
                p.lambda_f * iq +            # Magnet torque
                (p.Ld - p.Lq) * id_ * iq     # Reluctance torque (saliency)
            )
        )

    # --------------------------------------------------------
    # Mechanical subsystem (speed derivative)
    # --------------------------------------------------------
    def mechanical_dynamics(self, T_load):
        """
        Computes d(omega_m)/dt from Newton's law.
        """

        _, _, omega_m, _ = self.x
        p = self.p

        # J * domega/dt = Te - Tload - B*omega
        domega = (
            self.torque() - T_load - p.B * omega_m
        ) / p.J

        return domega

    # --------------------------------------------------------
    # Integrate one simulation step (explicit Euler)
    # --------------------------------------------------------
    def step(self, v_d, v_q, T_load, dt):
        """
        Advances the motor state by one time step dt.
        """

        # Electrical dynamics
        did, diq = self.electrical_dynamics(v_d, v_q)

        # Mechanical dynamics
        domega = self.mechanical_dynamics(T_load)

        # Integrate currents
        self.x[0] += did * dt
        self.x[1] += diq * dt

        # Integrate mechanical speed
        self.x[2] += domega * dt

        # Integrate electrical angle
        # d(theta_e)/dt = omega_e = pole_pairs * omega_m
        self.x[3] += self.p.pole_pairs * self.x[2] * dt


# ============================================================
# Coordinate transformations (FOC utilities)
# ============================================================

def clarke(a, b):
    """
    Clarke transform (2-phase → αβ stationary frame)

    Assumes:
        ia + ib + ic = 0
    """
    alpha = a
    beta = (a + 2.0 * b) / 1.7320508075688772  # 1/sqrt(3)
    return alpha, beta


def park(alpha, beta, theta):
    """
    Park transform (αβ → dq rotating frame)
    Aligns d-axis with rotor flux.
    """
    c = math.cos(theta)
    s = math.sin(theta)

    d =  c * alpha + s * beta
    q = -s * alpha + c * beta
    return d, q


def inv_park(d, q, theta):
    """
    Inverse Park transform (dq → αβ)
    Used to generate voltage commands for PWM.
    """
    c = math.cos(theta)
    s = math.sin(theta)

    alpha = c * d - s * q
    beta  = s * d + c * q
    return alpha, beta

