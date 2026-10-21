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

Current contents of the repository:

```text
.
├── docs/
│   ├── theory.md        # PMSM mathematical model: abc/αβ/dq frames, Clarke/Park, dq electrical model, torque, mechanical dynamics
│   ├── control.md       # (placeholder, empty)
│   └── observers.md     # (placeholder, empty)
│
├── simulation/
│   ├── motor_model.py   # PMSMParameters + PMSM class (dq electrical dynamics, torque, mechanical dynamics, step()) and clarke/park/inv_park helpers
│   ├── simulation.py    # Reference-signal (trapezoidal speed profile) generation and plotting
│   ├── control.py       # (placeholder, empty)
│   └── svpwm.py         # (placeholder, empty)
│
├── LICENSE
└── README.md
```

Planned (not yet in the repository): STM32 firmware (`firmware/`) and power-stage hardware (`hardware/`).

### Running the simulation code

The simulation scripts use Python 3 with `numpy`, `matplotlib` and `mplcyberpunk` (there is no requirements file yet):

```bash
pip install numpy matplotlib mplcyberpunk
python3 simulation/simulation.py   # plots the reference signal
```

`simulation/motor_model.py` provides the `PMSM` model class to be imported by the control-loop simulation.

## 7. Documentation Approach

All mathematical models, assumptions, and control decisions are documented in Markdown papers under `docs/`.

The documentation is written as a technical thesis-style record, covering:

- Model assumptions
- Reference frame choices
- Control-loop design rationale
- Discretization and timing
- Observer structure
- Practical implementation constraints

The goal is full transparency and reproducibility.

## 8. Simulation First

No firmware is written without prior simulation.

The simulation environment is intended to:

- Use fixed-step integration
- Mimic real-time control execution
- Include saturation, limits, and delays
- Be structured to map directly to embedded code

If it does not behave correctly in simulation, it is not deployed to hardware.

## 9. Safety Disclaimer

This project involves high-power electrical systems.

Improper implementation can cause:

- Equipment damage
- Fire
- Severe injury or death

This repository is provided for educational and research purposes only.
The author assumes no responsibility for misuse or unsafe implementations.

## 10. License

This project is released under the MIT License. See [LICENSE](LICENSE).

## 11. Status

🚧 Active development
Early-stage mathematical modeling and simulation phase.

## 12. Long-Term Goal

To build a fully open, industrial-quality traction motor controller that:

- Is technically rigorous
- Is practically usable
- Can power a real electric motorcycle
- Serves as a reference-quality learning and research platform

“This project is not about making a motor spin.
It is about understanding and controlling energy, torque, and motion — correctly.”
