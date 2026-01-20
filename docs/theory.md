# PMSM Motor Theory – Mathematical Model

This document presents the mathematical model of a three-phase Permanent Magnet
Synchronous Motor (PMSM), derived explicitly for control, simulation, and real-time
embedded implementation.

The objective is to obtain a **control-oriented model** that can be directly mapped
to software running on a microcontroller.

---

## 1. Three-Phase Stator Voltage Equations (abc frame)

The electrical behavior of each stator phase is described by Kirchhoff’s voltage law.

For each phase:

$$
v_a = R_s i_a + \frac{d\lambda_a}{dt}
$$

$$
v_b = R_s i_b + \frac{d\lambda_b}{dt}
$$

$$
v_c = R_s i_c + \frac{d\lambda_c}{dt}
$$

Where:
- $v_a, v_b, v_c$ are the stator phase voltages
- $i_a, i_b, i_c$ are the stator phase currents
- $R_s$ is the stator phase resistance
- $\lambda_a, \lambda_b, \lambda_c$ are the stator flux linkages

These equations represent the physical motor exactly, but are not convenient for control
due to strong coupling and time-varying flux terms.

---

## 2. Flux Linkage Components

Each phase flux linkage is composed of a stator-induced component and a rotor magnet component:

$$
\lambda_a = \lambda_{a,s} + \lambda_{a,m}
$$

$$
\lambda_b = \lambda_{b,s} + \lambda_{b,m}
$$

$$
\lambda_c = \lambda_{c,s} + \lambda_{c,m}
$$

The stator component depends on phase currents and inductances.
The magnet component depends on rotor electrical position.

---

## 3. Balanced Three-Phase Constraint

For a balanced three-phase motor without neutral connection, the phase currents satisfy:

$$
i_a + i_b + i_c = 0
$$

This constraint reduces the system to two independent electrical degrees of freedom.

---

## 4. Clarke Transformation (abc → αβ)

To eliminate redundancy, three-phase quantities are mapped to a stationary two-axis reference frame.

The Clarke transformation is defined by the scalar relations:

$$
x_\alpha = x_a
$$

$$
x_\beta = \frac{1}{\sqrt{3}} (x_a + 2x_b)
$$

Where $x$ represents voltage, current, or flux.

The $\alpha\beta$ frame is stationary and fixed to the stator.

---

## 5. Park Transformation (αβ → dq)

To obtain time-invariant quantities, the stationary reference frame is rotated
synchronously with the rotor magnetic field.

The Park transformation is defined as:

$$
x_d = x_\alpha \cos\theta_e + x_\beta \sin\theta_e
$$

$$
x_q = -x_\alpha \sin\theta_e + x_\beta \cos\theta_e
$$

Where $\theta_e$ is the electrical rotor angle.

In steady-state operation, $d$- and $q$-axis quantities become constant.

---

## 6. Electrical Model in dq Reference Frame

Applying the Clarke and Park transformations to the stator voltage equations yields
the PMSM electrical model in the rotating reference frame.

The direct-axis voltage equation is:

$$
v_d = R_s i_d + L_d \frac{di_d}{dt} - \omega_e L_q i_q
$$

The quadrature-axis voltage equation is:

$$
v_q = R_s i_q + L_q \frac{di_q}{dt} + \omega_e (L_d i_d + \lambda_f)
$$

Where:
- $L_d$ is the direct-axis inductance
- $L_q$ is the quadrature-axis inductance
- $\lambda_f$ is the permanent magnet flux linkage
- $\omega_e = \frac{d\theta_e}{dt}$ is the electrical angular speed

The terms proportional to $\omega_e$ represent cross-coupling introduced by the rotating
reference frame.

---

## 7. Interior PMSM Saliency

For an Interior PMSM (IPMSM), the inductances differ:

$$
L_d \neq L_q
$$

This inductance saliency introduces an additional torque-producing mechanism and increases
the coupling between electrical and mechanical dynamics.

The model retains both inductances independently to ensure scalability to traction motors.

---

## 8. Electromagnetic Torque Equation

The electromagnetic torque is given by:

$$
T_e = \frac{3}{2} p \left( \lambda_f i_q + (L_d - L_q) i_d i_q \right)
$$

Where $p$ is the number of pole pairs.

This expression shows that torque consists of:
- Magnetic torque from permanent magnets
- Reluctance torque due to saliency

---

## 9. Mechanical Dynamics

The mechanical dynamics of the rotor are described by:

$$
J \frac{d\omega_m}{dt} = T_e - T_L - B \omega_m
$$

Where:
- $J$ is the rotor inertia
- $\omega_m$ is the mechanical angular speed
- $T_L$ is the load torque
- $B$ is the viscous friction coefficient

Electrical and mechanical speeds are related by:

$$
\omega_e = p \cdot \omega_m
$$

---

## 10. State Variables for Control and Estimation

For control and observer design, the system state variables are defined as:

$$
i_d,\quad i_q,\quad \omega_m,\quad \theta_e
$$

Control inputs are the dq-axis voltages:

$$
v_d,\quad v_q
$$

Measured outputs are phase currents and, optionally, rotor position.

---

## 11. Practical Implementation Notes

- dq voltages are virtual control quantities
- Physical inverter limits are applied after inverse Park transformation
- Dead-time, PWM nonlinearity, and sampling delays are not included here
- These effects are handled at the modulation and hardware layers

---

## 12. Summary

This chapter derives a complete PMSM mathematical model starting from physical
three-phase stator equations and ending with a dq-frame representation suitable
for real-time, industrial-grade motor control.

All subsequent control and observer designs build directly upon this formulation.

