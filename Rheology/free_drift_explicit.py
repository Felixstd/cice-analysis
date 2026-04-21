"""
Ice-Ocean Momentum Solver — Explicit scheme
============================================
Solves the momentum equations using values known at time t only:
 
  m(u_{t+1} - u_t)/dt =  m*f*v_t + tau_a_x + rho_cw * S_t * u_t
  m(v_{t+1} - v_t)/dt = -m*f*u_t + tau_a_y + rho_cw * S_t * v_t
 
where  S_t = sqrt(u_t^2 + v_t^2)  (speed evaluated at current time).
 
Because every term on the RHS is known, the update is a single
closed-form evaluation — no iteration required:
 
  u_{t+1} = u_t + (dt/m) * ( m*f*v_t  + tau_a_x + rho_cw*S_t*u_t )
  v_{t+1} = v_t + (dt/m) * (-m*f*u_t  + tau_a_y + rho_cw*S_t*v_t )
 
Stability note
--------------
The explicit scheme is conditionally stable.  The water-drag term
introduces a damping time scale  T_drag = m / (rho_cw * S_t).
Stability requires  dt < T_drag, i.e.
 
    dt < m / (rho_cw * S_t)
 
For typical sea-ice parameters (m=300, rho_cw=5.5, S~0.1 m/s) this
gives dt < ~545 s.  The solver emits a warning when this is violated.
"""
 
import numpy as np
import matplotlib.pyplot as plt
 
 
# ---------------------------------------------------------------------------
# Single-timestep update
# ---------------------------------------------------------------------------
 
def solve_step(
    u_t: float,
    v_t: float,
    tau_ax: float,
    tau_ay: float,
    m: float = 300.0,
    dt: float = 3600.0,
    f: float = 1.37e-4,
    rho_cw: float = 5.5,
    verbose: bool = False,
) -> dict:
    """
    Advance one explicit timestep.
 
    Parameters
    ----------
    u_t, v_t        : velocity components at time t (m/s)
    tau_ax, tau_ay  : atmospheric stress components (N/m^2)
    m               : ice mass per unit area (kg/m^2), default 300
    dt              : timestep (s), default 3600
    f               : Coriolis parameter (s^-1), default 1.37e-4 (~70 deg N)
    rho_cw          : ocean drag coefficient rho*C_w (kg/m^3 s), default 5.5
    verbose         : print update summary if True
 
    Returns
    -------
    dict:
        u       : u_{t+1} (m/s)
        v       : v_{t+1} (m/s)
        S_t     : speed at time t (m/s)
        S_new   : speed at time t+1 (m/s)
        stable  : bool — whether dt < drag stability limit
    """
    S_t = np.sqrt(u_t**2 + v_t**2)
 
    # Stability check: dt < m / (rho_cw * S_t)
    # if S_t > 0.0:
    T_drag = m / (rho_cw * S_t)
    stable = dt < T_drag
    if not stable:
        print(f"Warning: stability violated — dt={dt:.1f} s >= "
                f"T_drag={T_drag:.1f} s  (S_t={S_t:.4f} m/s)")
    # else:
    #     T_drag = np.inf
    #     stable = True
 
    # Explicit RHS forces (per unit mass)
    F_x = m * f * v_t  + tau_ax - rho_cw * S_t * u_t
    F_y = -m * f * u_t + tau_ay - rho_cw * S_t * v_t
 
    # Forward-Euler update
    u_new = u_t + (dt / m) * F_x
    v_new = v_t + (dt / m) * F_y
    S_new = np.sqrt(u_new**2 + v_new**2)
 
    if verbose:
        print(f"  S_t    = {S_t:.6f} m/s")
        print(f"  F_x/m  = {F_x/m:.6f} m/s^2   F_y/m = {F_y/m:.6f} m/s^2")
        print(f"  u_t+1  = {u_new:.6f} m/s")
        print(f"  v_t+1  = {v_new:.6f} m/s")
        print(f"  S_t+1  = {S_new:.6f} m/s")
        print(f"  Stable : {stable}  (T_drag = {T_drag:.1f} s)")
 
    return dict(u=u_new, v=v_new, S_t=S_t, S_new=S_new, stable=stable)
 
 
# ---------------------------------------------------------------------------
# Multi-step time integrator
# ---------------------------------------------------------------------------
 
def time_integrate(
    u0: float,
    v0: float,
    tau_ax_series,
    tau_ay_series,
    n_steps: int,
    **kwargs,
) -> dict:
    """
    Integrate over multiple timesteps.
 
    Parameters
    ----------
    u0, v0          : initial velocity (m/s)
    tau_ax_series   : array-like length n_steps, atmospheric x-stress (N/m^2)
    tau_ay_series   : array-like length n_steps, atmospheric y-stress (N/m^2)
    n_steps         : number of timesteps
    **kwargs        : passed to solve_step (m, dt, f, rho_cw)
 
    Returns
    -------
    dict:
        u, v, S  : arrays of length n_steps+1
        stable   : bool array of length n_steps (per-step stability flag)
    """
    u_arr      = np.zeros(n_steps + 1)
    v_arr      = np.zeros(n_steps + 1)
    S_arr      = np.zeros(n_steps + 1)
    stable_arr = np.ones(n_steps, dtype=bool)
 
    u_arr[0], v_arr[0] = u0, v0
    S_arr[0] = np.sqrt(u0**2 + v0**2)
 
    for i in range(n_steps):
        res = solve_step(
            u_arr[i], v_arr[i],
            tau_ax_series[i], tau_ay_series[i],
            **kwargs,
        )
        u_arr[i+1]    = res['u']
        v_arr[i+1]    = res['v']
        S_arr[i+1]    = res['S_new']
        stable_arr[i] = res['stable']
 
    return dict(u=u_arr, v=v_arr, S=S_arr, stable=stable_arr)
 
 
# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
 
    print("=" * 55)
    print("Example 1: single explicit timestep")
    print("=" * 55)
    result = solve_step(
       u_t=-9.44e-3, v_t=1.0066e-2,
        tau_ax=6.711e-2, tau_ay=8.45e-3,
        m=22, dt=60.0, f=1.26e-4, rho_cw=.536,
        verbose=True,
    )
 
    # print()
    # print("=" * 55)
    # print("Example 2: 24-hour integration, constant forcing")
    # print("=" * 55)
    # import matplotlib.pyplot as plt
 
    # Use a small stable timestep for the explicit scheme
    dt_stable = 60.0       # s  (well below T_drag for typical speeds)
    T_total   = 300       # 24 hours
    n_steps   = int(T_total / dt_stable)
 
    tau_ax_arr = np.full(n_steps, 6.711e-2)
    tau_ay_arr = np.full(n_steps, 1.0066e-2)
 
    traj = time_integrate(u0=-9.44e-3, v0=1.0066e-2,
        tau_ax_series=tau_ax_arr,
        tau_ay_series=tau_ay_arr,
        n_steps=n_steps,
        m=22.0, dt=dt_stable, f=1.37e-4, rho_cw=0.536,
    )
 
    t_hours = np.arange(n_steps + 1) * dt_stable / 3600.0
 
    fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
 
    axes[0].plot(t_hours, traj['u'], label='u (x)', color='#185FA5')
    axes[0].plot(t_hours, traj['v'], label='v (y)', color='#D85A30')
    axes[0].set_ylabel("Velocity (m/s)")
    axes[0].legend()
    axes[0].grid(True, linewidth=0.5, alpha=0.5)
    axes[0].set_title(
        f"Ice velocity — explicit scheme  (dt={dt_stable:.0f} s, "
        f"constant forcing)"
    )
 
    axes[1].plot(t_hours, traj['S'], color='#0F6E56')
    axes[1].set_ylabel("Speed S (m/s)")
    axes[1].set_xlabel("Time (hours)")
    axes[1].grid(True, linewidth=0.5, alpha=0.5)
 
    unstable_steps = np.where(~traj['stable'])[0]
    if len(unstable_steps):
        print(f"Unstable steps: {len(unstable_steps)} / {n_steps}")
    else:
        print("All steps stable.")
 
    plt.tight_layout()
    plt.savefig("ice_ocean_trajectory.png", dpi=150)
    print("Plot saved to ice_ocean_trajectory.png")
    plt.show()
 
    print(f"\nFinal speed : {traj['S'][-1]:.4f} m/s")