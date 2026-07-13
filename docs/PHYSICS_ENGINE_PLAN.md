# PROMETHEUS PHYSICS ENGINE — BEYOND COSMIC LEVEL v2
## Built by: Ghias + Kiro
## Status: PLAN (ready to build)

---

## GAPS IN v1 (ALL FIXED)

| # | Gap | Fix |
|---|-----|-----|
| 1 | No Nuclear/Particle Physics | Added Level 6: full Standard Model + BSM |
| 2 | No Astrophysics | Added Level 10: stellar, compact objects, cosmology |
| 3 | No Plasma Physics | Added Level 9 |
| 4 | No Chaos/Nonlinear Dynamics | Integrated into Level 1 |
| 5 | No Quantum Optics / Nonlinear Optics | Added Level 8 |
| 6 | No Acoustics | Merged into Level 1 (waves) |
| 7 | No Biophysics/Soft Matter | Added Level 11 |
| 8 | No Computational Methods | Added Layer 0 |
| 9 | No Mathematical Physics (special funcs, Green's) | Added Layer 0 |
| 10 | No Tensor Engine for GR | Added Layer 0 |
| 11 | No Symmetry → Physics engine | Added Layer 0 (Lie algebra engine) |
| 12 | "Research" was vague | Now Level 12 with CONCRETE 2026 frontiers |
| 13 | No error propagation | Added Layer 0 |
| 14 | No experimental physics | Added as cross-cutting capability |
| 15 | No math↔physics map | Added Layer 4 with explicit connections |
| 16 | Used 2024 sources | Now 2025/2026: DESI DR2, muon g-2, ER=EPR, swampland |
| 17 | No nuclear reactions | Added (fission, fusion, decay, cross sections) |
| 18 | No solid state proper | Level 7 expanded: phonons, magnons, band theory |
| 19 | No fluid turbulence | Added to Level 1 |
| 20 | No information theory in physics | Added Level 12 |

---

## ARCHITECTURE v2 — BEYOND COSMIC

```
┌───────────────────────────────────────────────────────────────────────────────┐
│              PROMETHEUS PHYSICS ENGINE v2 — ULTIMATE                            │
│              prometheus_physics.py (~8000 lines)                                │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║ LAYER 0: MATHEMATICAL PHYSICS FOUNDATIONS                                ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║                                                                           ║  │
│  ║  PhysicsConstants (80+)          TensorEngine                             ║  │
│  ║  • All CODATA 2022 values        • Index notation (up/down)               ║  │
│  ║  • Natural unit systems           • Contraction, symmetrize               ║  │
│  ║  • Relations (α=e²/4πε₀ℏc)      • Riemann, Ricci, Weyl tensors          ║  │
│  ║  • Uncertainties                  • Christoffel symbols                    ║  │
│  ║                                   • Metric operations                      ║  │
│  ║  DimensionalEngine               SpecialFunctions                         ║  │
│  ║  • SI, CGS, natural, Planck      • Bessel J,Y,I,K                        ║  │
│  ║  • Unit algebra (m/s² × kg = N)  • Legendre P,Q                          ║  │
│  ║  • Buckingham π theorem          • Spherical harmonics Y_lm               ║  │
│  ║  • Auto-check every answer       • Hermite, Laguerre, Chebyshev          ║  │
│  ║  • Convert between systems       • Hypergeometric ₂F₁                    ║  │
│  ║                                   • Gamma, Beta, Zeta                      ║  │
│  ║  SymmetryEngine                   • Airy, Mathieu                         ║  │
│  ║  • Lie groups: SO(3), SU(2),                                              ║  │
│  ║    SU(3), U(1), Poincaré        GreensFunctionDB                         ║  │
│  ║  • Representations → particles   • Laplace, Helmholtz, wave              ║  │
│  ║  • Casimir operators             • Heat equation, Schrödinger             ║  │
│  ║  • Young tableaux                • Dirichlet, Neumann, mixed BC           ║  │
│  ║  • Character tables              • Retarded, advanced, Feynman            ║  │
│  ║                                                                           ║  │
│  ║  ApproximationEngine             ErrorEngine                              ║  │
│  ║  • Taylor/Laurent expansion      • Gaussian propagation                   ║  │
│  ║  • WKB, saddle point, steepest  • Monte Carlo error                      ║  │
│  ║  • Perturbation (regular+sing)   • Systematic + statistical               ║  │
│  ║  • Asymptotic matching           • Significant figures tracking           ║  │
│  ║  • Padé approximants             • χ² fitting                            ║  │
│  ║  • Dimensional regularization                                             ║  │
│  ║                                                                           ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║ LAYER 1: PHYSICS LAW DATABASE (250+ laws)                                ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║  PhysicsLaw:                                                              ║  │
│  ║    name, domain, statement, equation (symbolic),                          ║  │
│  ║    preconditions, consequences, derived_from[],                           ║  │
│  ║    applications[], limiting_cases[], symmetry_origin,                     ║  │
│  ║    experimental_status, year_discovered                                   ║  │
│  ║                                                                           ║  │
│  ║  + DEPENDENCY GRAPH: which law derives from which                         ║  │
│  ║  + AUTO-LEARN: web search for unknown laws                                ║  │
│  ║  + REGIME MAP: when each law is valid (speeds, energies, scales)          ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║ LAYER 2: DOMAIN SOLVERS (12 Levels — see below)                          ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║ LAYER 3: DERIVATION & PROOF ENGINE                                       ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║  • First-principles derivation (axioms → result)                          ║  │
│  ║  • Variational calculus (δS=0 → EOM for ANY Lagrangian)                  ║  │
│  ║  • Symmetry → Conservation (automatic Noether for any symmetry)          ║  │
│  ║  • Limiting cases engine (ℏ→0, c→∞, N→∞, weak/strong coupling)          ║  │
│  ║  • Buckingham π (dimensional analysis → functional form)                  ║  │
│  ║  • Fermi estimation (order-of-magnitude from first principles)           ║  │
│  ║  • Renormalization group (scale → effective theory)                       ║  │
│  ║  • Gauge principle (global → local symmetry → force)                     ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║ LAYER 4: CROSS-DOMAIN INTELLIGENCE                                       ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║  Math→Physics Map (from our 254 theorems):                                ║  │
│  ║    • Differential geometry → General Relativity                           ║  │
│  ║    • Group theory → Particle classification                               ║  │
│  ║    • Hilbert space → Quantum mechanics                                    ║  │
│  ║    • Topology → Topological phases, defects                               ║  │
│  ║    • Representation theory → Selection rules, degeneracy                  ║  │
│  ║    • Complex analysis → Scattering amplitudes                             ║  │
│  ║    • Spectral theory → Quantum spectra                                    ║  │
│  ║    • Stochastic → Brownian motion, Langevin                               ║  │
│  ║    • Category theory → TQFT, functorial QFT                              ║  │
│  ║    • Number theory → String landscape, modular forms in physics           ║  │
│  ║                                                                           ║  │
│  ║  Analogy Engine:                                                          ║  │
│  ║    • EM ↔ fluid dynamics (vortex = monopole)                              ║  │
│  ║    • QM ↔ optics (path integral = Huygens)                               ║  │
│  ║    • Thermodynamics ↔ information theory                                  ║  │
│  ║    • Black holes ↔ thermodynamics                                         ║  │
│  ║    • Condensed matter ↔ high-energy (quasiparticles = particles)          ║  │
│  ║    • Classical mechanics ↔ geometric optics (Hamilton-Jacobi = eikonal)   ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════╝  │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 12 LEVELS — COMPLETE LAW LIST

### Level 1: Classical Mechanics + Nonlinear Dynamics (30 laws)
**Textbooks**: Goldstein, Taylor, Landau Vol 1, Strogatz (Nonlinear)

1. Newton's 2nd (F=dp/dt, vector, variable mass)
2. Newton's 3rd (action-reaction, strong+weak forms)
3. Conservation of energy (with dissipation terms)
4. Conservation of momentum (linear)
5. Conservation of angular momentum
6. Work-energy theorem (path integral of force)
7. Euler-Lagrange equation (with constraints, Lagrange multipliers)
8. Hamilton's principle (δS=0, boundary conditions)
9. Hamilton's equations (q̇=∂H/∂p, ṗ=-∂H/∂q)
10. Poisson brackets ({q,p}=1, Jacobi identity)
11. Canonical transformations (generating functions F₁-F₄)
12. Liouville theorem (phase space incompressible)
13. Noether's theorem (continuous symmetry → conservation)
14. Virial theorem (⟨T⟩=-½Σ⟨F·r⟩, applications to gravity)
15. D'Alembert's principle (virtual work)
16. Kepler's laws (all 3, derived from Newton)
17. Euler equations (rigid body, principal axes)
18. Parallel axis + perpendicular axis theorems
19. Navier-Stokes (incompressible + compressible)
20. Euler fluid equations (inviscid limit)
21. Bernoulli's principle (steady, irrotational)
22. Continuity equation (mass conservation)
23. Reynolds number + turbulence onset
24. KAM theorem (near-integrable stability)
25. Lyapunov exponents (chaos quantification)
26. Poincaré recurrence (ergodic systems)
27. Action-angle variables (integrable systems)
28. Adiabatic invariants (slow parameter change)
29. Bifurcation theory (pitchfork, Hopf, saddle-node)
30. Strange attractors (Lorenz, Rössler, fractal dimension)

### Level 2: Electromagnetism + Optics (30 laws)
**Textbooks**: Jackson, Griffiths, Born & Wolf (Optics)

1. Gauss law (∇·E=ρ/ε₀) + integral form
2. No magnetic monopoles (∇·B=0)
3. Faraday's law (∇×E=-∂B/∂t) + integral form
4. Ampère-Maxwell (∇×B=μ₀J+μ₀ε₀∂E/∂t)
5. Lorentz force (F=q(E+v×B))
6. Coulomb's law (+ superposition)
7. Biot-Savart law
8. Poynting theorem (energy conservation)
9. EM energy density (u=½ε₀E²+B²/2μ₀)
10. EM wave equation (vacuum + medium)
11. Larmor radiation formula (accelerating charge)
12. Liénard-Wiechert potentials (retarded)
13. Gauge transformations (Lorenz, Coulomb, radiation)
14. Multipole expansion (electric + magnetic)
15. Boundary conditions (tangential E, normal B, etc.)
16. Fresnel equations (reflection, transmission, Brewster)
17. Snell's law + total internal reflection
18. Kramers-Kronig relations (causality)
19. Lenz's law (induced EMF)
20. Skin depth (δ=√(2/ωμσ))
21. Waveguide modes (TE/TM, cutoff)
22. Radiation reaction (Abraham-Lorentz)
23. Debye shielding + Debye length
24. Diffraction (Fraunhofer, Fresnel, Kirchhoff)
25. Interference (Young's, thin film, Fabry-Perot)
26. Polarization (Jones matrices, Stokes, Müller)
27. Nonlinear optics (χ², χ³, SHG, self-focusing)
28. Optical resonators (Q factor, finesse, modes)
29. Metamaterials + negative refraction
30. Photonic crystals + band gaps

### Level 3: Quantum Mechanics (35 laws)
**Textbooks**: Sakurai, Griffiths, Shankar, Cohen-Tannoudji, Weinberg

1. Schrödinger equation (time-dependent)
2. Time-independent Schrödinger equation
3. Born rule (measurement postulate)
4. Heisenberg uncertainty (generalized: ΔAΔB≥½|⟨[A,B]⟩|)
5. Canonical commutation [x̂,p̂]=iℏ
6. Angular momentum algebra [Jᵢ,Jⱼ]=iℏεᵢⱼₖJₖ
7. Ehrenfest theorem (quantum→classical bridge)
8. Pauli exclusion principle
9. Spin-statistics theorem (proof from QFT)
10. Harmonic oscillator (ladder operators, coherent states)
11. Hydrogen atom (exact: n,l,m,s quantum numbers)
12. WKB approximation (connection formulas)
13. Variational principle (Rayleigh-Ritz)
14. Non-degenerate perturbation theory (all orders)
15. Degenerate perturbation theory
16. Time-dependent perturbation (Dyson series)
17. Fermi's golden rule (transition rates)
18. Selection rules (electric dipole, magnetic dipole, quadrupole)
19. Clebsch-Gordan decomposition (j₁⊗j₂)
20. Wigner-Eckart theorem (tensor operators)
21. Berry phase + Berry connection + Berry curvature
22. No-cloning theorem
23. Bell's theorem (CHSH inequality violation)
24. Density matrix formalism (mixed states, purification)
25. Path integral formulation (propagator as sum over histories)
26. Tunneling (transmission coefficient, instantons)
27. Decoherence (environment-induced superselection)
28. Adiabatic theorem (+ corrections)
29. Stone-von Neumann theorem (uniqueness of CCR rep)
30. Scattering theory (Born, partial waves, optical theorem)
31. S-matrix (unitarity, analyticity, crossing)
32. Identical particles (symmetrization postulate)
33. Quantum Zeno effect
34. Entanglement entropy (von Neumann: S=-Tr ρ ln ρ)
35. Quantum teleportation protocol

### Level 4: Statistical Mechanics + Thermodynamics (25 laws)
**Textbooks**: Pathria, Landau Vol 5, Kardar, Huang

1. Boltzmann distribution (P∝e^{-βE})
2. Partition function (Z=Σe^{-βEᵢ}, generating function)
3. Free energy (F=-kT ln Z, Legendre transforms)
4. Entropy (S=k ln Ω = -kΣpᵢ ln pᵢ)
5. First law (dU=δQ-δW)
6. Second law (dS≥0, Clausius, Kelvin)
7. Third law (S→0 as T→0, Nernst)
8. Equipartition (½kT per quadratic DOF)
9. Fluctuation-dissipation theorem (FDT)
10. Fermi-Dirac distribution
11. Bose-Einstein distribution + condensation
12. Planck distribution (blackbody radiation)
13. Stefan-Boltzmann law (P=σT⁴)
14. Clausius-Clapeyron (phase boundary slopes)
15. Landau theory (order parameter, mean field)
16. Ising model (1D exact, 2D Onsager solution)
17. Critical exponents + universality classes
18. Renormalization group (Kadanoff blocking, Wilson)
19. Fluctuation theorems (Jarzynski, Crooks)
20. Onsager reciprocal relations (linear response)
21. Boltzmann H-theorem (entropy increase)
22. Maxwell distribution (velocity)
23. Gibbs paradox + resolution (indistinguishability)
24. Phase rule (F=C-P+2)
25. Lee-Yang theorem (zeros of partition function)

### Level 5: Special + General Relativity (25 laws)
**Textbooks**: Carroll, Wald, Misner-Thorne-Wheeler, Weinberg (Gravitation)

1. Lorentz transformations (boosts + rotations)
2. Time dilation (Δτ = Δt/γ)
3. Length contraction (L=L₀/γ)
4. Mass-energy equivalence (E=mc², E²=(pc)²+(mc²)²)
5. Four-momentum (p^μ=(E/c, p⃗))
6. Relativistic Doppler effect
7. Thomas precession
8. Einstein field equations (G_μν+Λg_μν=8πG/c⁴ T_μν)
9. Geodesic equation (free-fall = straightest path)
10. Schwarzschild metric (static spherical BH)
11. Kerr metric (rotating BH, ergosphere)
12. Gravitational redshift (z=ΔΦ/c²)
13. Gravitational lensing (deflection angle = 4GM/bc²)
14. Gravitational waves (h_μν, + and × polarizations)
15. Friedmann equations (a(t), H², expansion)
16. Hubble's law (v=H₀d, cosmological redshift)
17. Penrose singularity theorem (trapped surfaces → singularity)
18. Hawking radiation (T=ℏc³/8πGMk)
19. Bekenstein-Hawking entropy (S=A/4l_P²)
20. ADM formalism (3+1 decomposition, constraints)
21. Birkhoff's theorem (spherical vacuum = Schwarzschild)
22. Frame dragging (Lense-Thirring)
23. Raychaudhuri equation (geodesic focusing)
24. Penrose process (energy extraction from Kerr)
25. Cosmological perturbation theory (scalar, vector, tensor modes)

### Level 6: Particle Physics + QFT (30 laws)
**Textbooks**: Peskin & Schroeder, Weinberg QFT I-III, Schwartz

1. Klein-Gordon equation (spin-0)
2. Dirac equation (spin-½)
3. Proca equation (massive spin-1)
4. Feynman propagator (scalar, fermion, gauge)
5. LSZ reduction formula (S-matrix from Green's functions)
6. Wick's theorem (time-ordering → normal-ordering)
7. Dyson series + Feynman diagrams
8. Ward-Takahashi identity (gauge invariance)
9. QED vertex rule (ieγ^μ)
10. Running coupling (β function, RG equations)
11. Anomalous magnetic moment (g-2, Schwinger correction α/2π)
12. Muon g-2 anomaly (2026 Breakthrough Prize: 5σ deviation!)
13. Lamb shift (vacuum polarization + self-energy)
14. Asymptotic freedom (QCD: β₀<0 for N_f<16.5)
15. Confinement (color singlets only, string breaking)
16. Higgs mechanism (SSB: φ→v+h, W±=gv/2, Z=gv/2cosθ_W)
17. Goldstone theorem (SSB of continuous → massless bosons)
18. Coleman-Mandula theorem (no mixing of internal+spacetime except SUSY)
19. CPT theorem (all local Lorentz QFTs preserve CPT)
20. Optical theorem (σ_tot=4π/k Im f(0))
21. Anomaly cancellation (SM anomaly-free)
22. CKM matrix (quark mixing, CP violation)
23. PMNS matrix (neutrino mixing, oscillations)
24. Neutrino oscillation formula P(ν_α→ν_β)
25. Standard Model gauge group SU(3)×SU(2)×U(1)
26. Cross section formulas (Rutherford, Mott, Compton, Møller)
27. Decay rates (Γ from |M|², phase space)
28. Parton distribution functions (DIS, DGLAP evolution)
29. Effective field theory (power counting, matching)
30. Supersymmetry basics (supermultiplets, MSSM spectrum)

### Level 7: Condensed Matter Physics (25 laws)
**Textbooks**: Ashcroft & Mermin, Altland & Simons, Chaikin & Lubensky

1. Bloch's theorem (ψ_k=e^{ik·r}u_k)
2. Band theory (tight-binding, nearly-free electron)
3. Fermi liquid theory (Landau quasiparticles, effective mass)
4. BCS theory (Cooper pairing, gap equation)
5. Meissner effect (B=0 inside SC, London penetration)
6. London equations (∇²B=B/λ²)
7. Josephson effects (DC: I=I_c sinφ, AC: V=ℏ/2e dφ/dt)
8. Berry phase (γ=∮⟨n|∇_k|n⟩·dk)
9. Chern number (topological invariant, TKNN)
10. Quantum Hall effect (σ_xy=ne²/h, quantized)
11. Anderson localization (disorder → localization)
12. Kondo effect (magnetic impurity screening)
13. Hubbard model (U vs t competition)
14. Mermin-Wagner theorem (no 2D long-range order, continuous sym)
15. Phonons (acoustic + optical branches, Debye model)
16. Magnons (spin waves, Holstein-Primakoff)
17. Landau levels (B field → discrete orbits, degeneracy)
18. Fractional quantum Hall (Laughlin wavefunction, ν=1/3)
19. Topological insulators (Z₂ invariant, edge states)
20. Weyl/Dirac semimetals (band crossing, Fermi arcs)
21. Superconducting gap equation (Δ(T) BCS)
22. Ginzburg-Landau theory (GL equations, vortices)
23. Spin-orbit coupling (Rashba, Dresselhaus)
24. RKKY interaction (indirect exchange via conduction electrons)
25. Density functional theory (Kohn-Sham equations, exchange-correlation)

### Level 8: Quantum Optics + Photonics (20 laws)
**Textbooks**: Gerry & Knight, Walls & Milburn, Scully & Zubairy

1. Photon statistics (Poisson=coherent, sub/super-Poisson)
2. Coherent states (|α⟩=e^{-|α|²/2}Σα^n/√n!|n⟩)
3. Squeezed states (ΔX₁ΔX₂=¼, one quadrature reduced)
4. Jaynes-Cummings model (atom-cavity: Ĥ=ωa†a+Ω σ_z/2+g(aσ⁺+a†σ⁻))
5. Rabi oscillations (P(t)=sin²(Ωt/2))
6. Cavity QED (strong coupling: g>κ,γ)
7. Photon antibunching (g²(0)<1, nonclassical)
8. Hong-Ou-Mandel effect (two-photon interference)
9. Purcell effect (cavity-enhanced spontaneous emission)
10. Laser threshold (population inversion, gain>loss)
11. Master equation (Lindblad form for open quantum systems)
12. Quantum noise (shot noise, thermal noise, SQL)
13. Homodyne/heterodyne detection
14. Parametric down-conversion (SPDC, entangled pairs)
15. Quantum key distribution (BB84, E91 protocols)
16. Nonlinear susceptibility (χ²: SHG, OPA; χ³: Kerr, FWM)
17. Electromagnetically induced transparency (EIT, slow light)
18. Optical Bloch equations (density matrix evolution)
19. Input-output theory (quantum Langevin)
20. Photonic topological insulators (topological photonics)

### Level 9: Plasma Physics + Astrophysical Fluids (20 laws)
**Textbooks**: Chen (Plasma), Bellan, Kulsrud

1. Debye shielding (λ_D=√(ε₀kT/ne²))
2. Plasma frequency (ω_p=√(ne²/ε₀m))
3. Vlasov equation (collisionless Boltzmann)
4. Magnetohydrodynamics (MHD: ideal + resistive)
5. Alfvén waves (v_A=B/√(μ₀ρ))
6. Magnetic reconnection (Sweet-Parker, Petschek)
7. Landau damping (collisionless wave damping)
8. Cyclotron motion (ω_c=eB/m, Larmor radius)
9. Magnetic mirror (μ=mv⊥²/2B adiabatic invariant)
10. Plasma beta (β=nkT/(B²/2μ₀))
11. Pinch effects (Z-pinch, θ-pinch, Bennett)
12. Rayleigh-Taylor instability (heavy on light)
13. Kelvin-Helmholtz instability (shear flow)
14. Jeans instability (gravitational collapse criterion)
15. Virial theorem for self-gravitating gas
16. Chandrasekhar limit (M_Ch=1.4 M☉ for white dwarfs)
17. Eddington luminosity (radiation pressure = gravity)
18. Synchrotron radiation (relativistic cyclotron)
19. Bremsstrahlung (free-free radiation)
20. Magnetic dynamo (self-sustaining B field generation)

### Level 10: Astrophysics + Cosmology (25 laws)
**Textbooks**: Weinberg (Cosmology), Shapiro & Teukolsky, Ryden

1. Friedmann equations (H²=8πGρ/3-k/a², ä/a=...)
2. Hubble law (v=H₀d, H₀≈70 km/s/Mpc)
3. Cosmological redshift (1+z=a₀/a(t))
4. Dark energy equation of state (w=P/ρ, DESI 2026: w evolves!)
5. Inflation (slow-roll: ε=(V'/V)²/16πG ≪1)
6. CMB temperature (T=2.725K, anisotropies ΔT/T~10⁻⁵)
7. Sachs-Wolfe effect (gravitational redshift of CMB)
8. Nucleosynthesis (BBN: H, He, Li abundances)
9. Structure formation (Jeans mass, Press-Schechter)
10. Tolman-Oppenheimer-Volkoff equation (neutron star structure)
11. Chandrasekhar mass (white dwarf limit 1.4 M☉)
12. Oppenheimer-Snyder collapse (dust → BH)
13. Kerr-Newman (charged rotating BH, full solution)
14. No-hair theorem (BH characterized by M,Q,J only)
15. Cosmic censorship (weak: singularity hidden by horizon)
16. Penrose process + superradiance
17. Hawking radiation (BH evaporation, information paradox)
18. Holographic principle (S≤A/4l_P²)
19. Dark matter evidence (rotation curves, lensing, CMB)
20. Baryogenesis (Sakharov conditions)
21. Gravitational wave sources (mergers, inspirals, stochastic)
22. Pulsar timing + GW detection
23. Type Ia supernovae (standard candles, dark energy evidence)
24. Cosmic distance ladder (parallax, Cepheids, Tully-Fisher, SNIa)
25. ΛCDM model (6 parameters: H₀, Ω_b, Ω_c, τ, n_s, A_s)

### Level 11: Nuclear + Atomic + Molecular Physics (20 laws)
**Textbooks**: Krane (Nuclear), Foot (Atomic), Bransden & Joachain

1. Nuclear binding energy (Bethe-Weizsäcker semi-empirical)
2. Shell model (magic numbers: 2,8,20,28,50,82,126)
3. Radioactive decay law (N=N₀e^{-λt}, half-life)
4. Alpha decay (Gamow tunneling factor)
5. Beta decay (Fermi theory, V-A structure)
6. Nuclear reactions (Q-value, cross sections, Breit-Wigner)
7. Fission (liquid drop, barrier, chain reaction, criticality)
8. Fusion (pp-chain, CNO cycle, Lawson criterion)
9. Fine structure (spin-orbit: α²E_n corrections)
10. Hyperfine structure (nuclear magnetic moment)
11. Lamb shift (QED correction to hydrogen)
12. Zeeman effect (weak, strong, anomalous)
13. Stark effect (linear + quadratic)
14. Selection rules (atomic: Δl=±1, ΔJ=0,±1)
15. Born-Oppenheimer approximation (molecular)
16. Molecular orbital theory (bonding/antibonding)
17. Rotational-vibrational spectra (rigid rotor + harmonic)
18. Franck-Condon principle (vertical transitions)
19. Laser cooling (Doppler, Sisyphus, magneto-optical trap)
20. Bose-Einstein condensate (macroscopic quantum state)

### Level 12: RESEARCH FRONTIER — 2025/2026 CUTTING EDGE (25 laws/conjectures)
**Sources**: arXiv 2025-2026, DESI DR2, Muon g-2, Nobel 2025

1. ER=EPR conjecture (entanglement = wormhole, Maldacena-Susskind)
2. AdS/CFT correspondence (bulk gravity ↔ boundary CFT)
3. Ryu-Takayanagi formula (S_A = Area(γ_A)/4G_N)
4. Swampland conjectures (distance, de Sitter, weak gravity)
5. Amplituhedron (scattering amplitudes as geometry, no locality/unitarity assumed)
6. Celestial holography (S-matrix as 2D CFT correlators on celestial sphere)
7. It from Qubit (spacetime from quantum information)
8. Quantum error correction = holography (bulk ↔ logical qubits)
9. Sachdev-Ye-Kitaev model (solvable quantum chaos, near-AdS₂)
10. Eigenstate thermalization hypothesis (ETH)
11. Many-body localization (MBL, breakdown of thermalization)
12. DESI 2025/2026 results (dark energy equation of state EVOLVES: w₀≈-0.7, w_a≈-1.0)
13. Muon g-2 final result (Fermilab 2026: a_μ(exp)-a_μ(SM) = 249±48 × 10⁻¹¹)
14. Neutrino mass ordering (JUNO, DUNE, normal hierarchy favored)
15. Gravitational wave memory effect (permanent displacement after wave passes)
16. Topological quantum computation (non-Abelian anyons, braiding)
17. Quantum supremacy/advantage (superconducting qubits, Nobel 2025)
18. Tensor networks as geometry (MERA = hyperbolic space)
19. Non-equilibrium steady states (driven quantum systems)
20. Floquet engineering (periodic driving → synthetic topology)
21. Quantum thermodynamics (work extraction, quantum engines)
22. PT-symmetric quantum mechanics (non-Hermitian but real spectrum)
23. Fracton topological order (restricted mobility excitations)
24. Machine learning in physics (neural network quantum states, symbolic regression)
25. Measurement-induced phase transitions (entanglement vs monitoring)

---

## PHYSICAL CONSTANTS (80+ with uncertainties)

### Fundamental
| Constant | Symbol | Value | Uncertainty |
|----------|--------|-------|-------------|
| Speed of light | c | 299792458 m/s | exact |
| Planck constant | h | 6.62607015×10⁻³⁴ J·s | exact |
| Reduced Planck | ℏ | 1.054571817×10⁻³⁴ J·s | exact |
| Elementary charge | e | 1.602176634×10⁻¹⁹ C | exact |
| Boltzmann | k_B | 1.380649×10⁻²³ J/K | exact |
| Avogadro | N_A | 6.02214076×10²³ mol⁻¹ | exact |
| Gravitational | G | 6.67430×10⁻¹¹ m³/(kg·s²) | 1.5×10⁻⁵ |
| Fine structure | α | 1/137.035999177 | 2.5×10⁻¹⁰ |
| Electron mass | m_e | 9.1093837090×10⁻³¹ kg | 3.0×10⁻¹⁰ |
| Proton mass | m_p | 1.67262192595×10⁻²⁷ kg | 3.1×10⁻¹⁰ |
| Neutron mass | m_n | 1.67492750056×10⁻²⁷ kg | 5.6×10⁻¹⁰ |

### Electromagnetic
| ε₀ | 8.8541878128×10⁻¹² F/m | exact |
| μ₀ | 1.25663706127×10⁻⁶ H/m | 1.6×10⁻¹⁰ |
| Bohr magneton | μ_B | 9.2740100657×10⁻²⁴ J/T | 3.0×10⁻¹⁰ |
| Nuclear magneton | μ_N | 5.0507837393×10⁻²⁷ J/T | 3.1×10⁻¹⁰ |

### Atomic
| Bohr radius | a₀ | 5.29177210544×10⁻¹¹ m | 1.6×10⁻¹⁰ |
| Rydberg | R_∞ | 10973731.568157 m⁻¹ | 1.1×10⁻¹² |
| Compton (electron) | λ_C | 2.42631023538×10⁻¹² m | 3.0×10⁻¹⁰ |
| Classical e⁻ radius | r_e | 2.8179403205×10⁻¹⁵ m | 4.7×10⁻¹⁰ |

### Nuclear/Particle
| Fermi coupling | G_F | 1.1663787×10⁻⁵ GeV⁻² | 5.1×10⁻⁷ |
| Strong coupling | α_s(M_Z) | 0.1180 | 8.5×10⁻³ |
| W boson mass | M_W | 80.3692 GeV/c² | 2025 value |
| Z boson mass | M_Z | 91.1876 GeV/c² | 2.3×10⁻⁵ |
| Higgs mass | M_H | 125.20 GeV/c² | 8.8×10⁻⁴ |
| Top quark mass | m_t | 172.57 GeV/c² | 1.7×10⁻³ |
| Weinberg angle | sin²θ_W | 0.23121 | 1.3×10⁻⁴ |

### Cosmological
| Hubble constant | H₀ | 67.4±0.5 km/s/Mpc | Planck 2018 |
| Hubble (local) | H₀ | 73.0±1.0 km/s/Mpc | SH0ES (TENSION!) |
| CMB temperature | T_CMB | 2.7255 K | |
| Baryon density | Ω_b h² | 0.02237 | |
| Dark matter density | Ω_c h² | 0.1200 | |
| Dark energy | Ω_Λ | 0.685 | |
| Age of universe | t₀ | 13.797 Gyr | |
| Cosmological constant | Λ | ~1.1×10⁻⁵² m⁻² | |

### Planck Units
| Planck length | l_P | 1.616255×10⁻³⁵ m |
| Planck mass | m_P | 2.176434×10⁻⁸ kg |
| Planck time | t_P | 5.391247×10⁻⁴⁴ s |
| Planck temperature | T_P | 1.416784×10³² K |
| Planck energy | E_P | 1.220890×10¹⁹ GeV |

---

## IMPLEMENTATION PHASES

### Phase 1: Core Foundation (~2000 lines)
```python
class PhysicsLawDB:      # 250+ laws structured
class PhysicsConstants:  # 80+ constants with units
class DimensionalEngine: # unit checking + natural units
class PhysicsIdentifier: # detect domain from question
```
**Time**: 1 session

### Phase 2: Mathematical Physics Layer (~1500 lines)
```python
class TensorEngine:       # indices, contraction, Christoffel
class SpecialFunctions:   # Bessel, Legendre, Ylm, ...
class GreensFunctionDB:   # all standard PDEs
class SymmetryEngine:     # Lie groups → physics
class ApproximationEngine: # WKB, perturbation, saddle
```
**Time**: 1 session

### Phase 3: Classical + EM Solvers (~1500 lines)
```python
class NewtonianSolver:   # F=ma, energy methods, projectiles
class LagrangianSolver:  # generalized coords → EOM
class HamiltonianSolver: # phase space, canonical transforms
class EMSolver:          # Maxwell applications, radiation
class WaveSolver:        # optics, diffraction, interference
```
**Time**: 1 session

### Phase 4: Quantum + StatMech Solvers (~2000 lines)
```python
class QuantumSolver:     # SE for standard potentials
class PerturbationEngine: # all orders, time-dep + indep
class AngularMomentum:   # CG coefficients, selection rules
class StatMechSolver:    # partition functions → thermo
class PhaseTransitions:  # Landau, Ising, RG
```
**Time**: 1 session

### Phase 5: Advanced Solvers (~2000 lines)
```python
class RelativitySolver:  # metrics, geodesics, cosmology
class QFTSolver:         # Feynman rules, cross sections
class CondensedMatter:   # bands, topology, superconductivity
class NuclearSolver:     # decay, reactions, binding energy
class AstroSolver:       # stellar, BH, cosmological models
```
**Time**: 1 session

### Phase 6: Research + Intelligence (~1000 lines)
```python
class DerivationEngine:  # first principles → any result
class PhysicsProofEngine: # verify physics arguments
class FermiEstimator:    # order-of-magnitude from nothing
class CrossDomainPhysics: # connect math theorems ↔ physics
class PhysicsAutoLearn:  # web search for unknown results
```
**Time**: 1 session

---

## REUSE FROM MATH ENGINE (254 theorems)

| Math Theorem/Area | Physics Application |
|---|---|
| Differential geometry (Stokes, de Rham) | General Relativity, gauge theory |
| Group theory (Sylow, classification) | Particle physics, crystal symmetry |
| Representation theory (Schur, Weyl) | Selection rules, angular momentum |
| Linear algebra (spectral theorem) | Quantum mechanics operators |
| Topology (Brouwer, Euler char) | Topological phases, defects |
| Complex analysis (residues, Cauchy) | Scattering amplitudes, Green's functions |
| Functional analysis (Banach, Hilbert) | QM foundations, operators |
| Probability (CLT, large deviations) | Statistical mechanics |
| ODE/PDE theory | All equations of motion |
| Calculus of variations | Lagrangian mechanics, field theory |
| Number theory (modular forms) | String theory, moonshine |
| Category theory (Yoneda, adjoint) | TQFT, functorial QFT |

---

## SUCCESS CRITERIA — BEYOND COSMIC

| Test | Target | Source |
|------|--------|--------|
| Jackson EM problems (Ch 1-12) | >80% correct | Graduate EM |
| Griffiths QM problems (all chapters) | >90% correct | Standard QM |
| Landau Vol 1 problems | >70% correct | Advanced mech |
| PhD qualifying exams (MIT/Stanford/UA) | >80% score | Real exams |
| Dimensional analysis on EVERY answer | 100% | Auto-check |
| Derive F=ma from Lagrangian | ✓ | First principles |
| Derive Maxwell from gauge principle | ✓ | First principles |
| Derive Hawking T from Unruh + equivalence | ✓ | Research |
| Explain 2026 DESI dark energy result | ✓ | Frontier |
| Explain muon g-2 anomaly significance | ✓ | 2026 Breakthrough |
| Cross-domain: use Noether for any symmetry | ✓ | Intelligence |
| Fermi estimate anything | ✓ | Estimation |
| Step-by-step derivation with units | 100% | Every answer |
| Error propagation on numerical results | 100% | Rigor |

---

## TOTAL SCOPE

| Metric | v1 (old plan) | v2 (BEYOND COSMIC) |
|--------|---|---|
| Levels | 8 | 12 |
| Laws | 155 | 255+ |
| Constants | 50 | 80+ |
| Domains covered | 8 | 15+ |
| 2026 frontiers | 0 | 25 |
| Math reuse connections | mentioned | 12 explicit maps |
| Experimental physics | none | error propagation + fitting |
| File size estimate | ~4000 lines | ~10000 lines |
| Nuclear physics | none | full (20 laws) |
| Quantum optics | none | full (20 laws) |
| Plasma physics | none | full (20 laws) |
| Chaos/nonlinear | none | integrated (10 laws) |
| Astrophysics | 2 mentions | full (25 laws) |
| Particle physics | sketch | full SM + BSM (30 laws) |

---

## FILE STRUCTURE

```
src/python/
  prometheus_physics.py       — Main: LawDB + Constants + DimensionalEngine + Identifier
  prometheus_physics_solve.py — Solvers: Classical, EM, QM, StatMech, Relativity, QFT
  prometheus_physics_adv.py   — Advanced: Condensed, Nuclear, Plasma, Astro, Optics
  prometheus_physics_mind.py  — Intelligence: Derivation, Proof, Fermi, CrossDomain, AutoLearn
```

**TOTAL: ~10,000 lines across 4 files**
**COVERS: ALL physics from high school to active research frontiers (2026)**
**DERIVES: from first principles, not lookup**
**VERIFIES: dimensional analysis + error propagation on every answer**
