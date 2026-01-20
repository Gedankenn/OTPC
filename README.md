# Open Traction PMSM Controller

> Open-source, industrial-grade Field-Oriented Control (FOC) platform for PMSM motors,  
> designed to scale from low-power laboratory setups to electric motorcycle traction drives.

---

## 1. Project Vision

This project aims to design and implement a **traction-grade motor controller** for an electric motorcycle, targeting an eventual **~400 cc equivalent** power level.

The controller is:
- **Industrial in architecture**
- **Open-source in implementation**
- **Research-driven**, with full mathematical derivation and validation
- **Scalable**, starting from a low-power PMSM test motor

This is **not** a hobby ESC.  
It is a full **traction inverter + control system**, built step by step with correctness, safety, and extensibility as primary goals.

---

## 2. Design Philosophy

The project follows these core principles:

- **Field-Oriented Control (FOC)** as the fundamental control strategy
- **Torque-controlled architecture**
- **dq-frame control** with proper reference frame separation
- **Explicit modeling of electrical and mechanical dynamics**
- **Observer-based state estimation**
- **Hardware-aware control design**
- **Simulation-first, hardware-second workflow**

All design decisions are documented and justified.

---

## 3. Scope

### Included
- PMSM mathematical modeling
- Reference frame transformations (abc → αβ → dq)
- Current control loops
- Space Vector PWM (SVPWM)
- State observers (planned: EKF / Kalman-based)
- Simulation environment (Python)
- Embedded firmware (STM32)
- Safety-oriented control architecture

### Not Included
- Mechanical vehicle design
- Battery pack design
- BMS hardware (only interface-level integration)

---

## 4. Target Hardware (Planned)

### Control MCU
- STM32 family (motor-control optimized variants)
- Hardware PWM timers
- Synchronized ADC sampling
- Deterministic real-time execution

### Power Stage (Future Phases)
- 3-phase inverter
- DC bus: 72–96 V (development), scalable upward
- Phase current: scalable to traction levels
- Isolated gate drivers
- Hardware protection mechanisms

---

## 5. Development Phases

### Phase 0 — Foundations (Current)
- Mathematical derivation
- Control architecture definition
- Python-based simulation
- Low-power PMSM testing (bench motor)

### Phase 1 — Embedded Control Core
- FOC implementation on STM32
- Current sensing and timing validation
- SVPWM implementation
- Stable closed-loop current control

### Phase 2 — Estimation & Dynamics
- Speed and position estimation
- Observer design and tuning
- Transition from sensored to sensorless operation

### Phase 3 — Traction Features
- Torque request interface
- Regenerative braking
- Field weakening
- CAN communication (vehicle integration)

### Phase 4 — High-Power Scaling
- Traction inverter hardware
- Thermal considerations
- Safety validation
- Vehicle-level testing

---

## 6. Repository Structure

```text
.
├── docs/               # Mathematical derivations, design decisions, papers
│   ├── theory.md
│   ├── control.md
│   └── observers.md
│
├── simulation/         # Python-based motor and control simulation
│   ├── motor_model.py
│   ├── control_loops.py
│   ├── svpwm.py
│   └── sim_main.py
│
├── firmware/           # Embedded firmware (STM32)
│   ├── drivers/
│   ├── control/
│   ├── observers/
│   └── main.c
│
├── hardware/           # Schematics, PCB, power stage (future)
│
└── README.md
```

## 7. Documentation Approach

All mathematical models, assumptions, and control decisions are documented in Markdown papers under docs/.

The documentation is written as a technical thesis-style record, covering:

Model assumptions

Reference frame choices

Control-loop design rationale

Discretization and timing

Observer structure

Practical implementation constraints

The goal is full transparency and reproducibility.

## 8. Simulation First

No firmware is written without prior simulation.

The simulation environment:

Uses fixed-step integration

Mimics real-time control execution

Includes saturation, limits, and delays

Is structured to map directly to embedded code

If it does not behave correctly in simulation, it is not deployed to hardware.

## 9. Safety Disclaimer

This project involves high-power electrical systems.

Improper implementation can cause:

Equipment damage

Fire

Severe injury or death

This repository is provided for educational and research purposes only.
The author assumes no responsibility for misuse or unsafe implementations.

## 10. License

This project is released under an open-source license (to be defined).

## 11. Status

🚧 Active development
Early-stage mathematical modeling and simulation phase.

## 12. Long-Term Goal

To build a fully open, industrial-quality traction motor controller that:

Is technically rigorous

Is practically usable

Can power a real electric motorcycle

Serves as a reference-quality learning and research platform

“This project is not about making a motor spin.
It is about understanding and controlling energy, torque, and motion — correctly.”
