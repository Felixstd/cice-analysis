"""
Ice-Ocean Momentum Solver
=========================
Solves the implicit coupled equations:
 
  m(u_{t+1} - u_t)/dt =  m*f*v_{t+1} + tau_a_x + rho_cw * S * u_{t+1}
  m(v_{t+1} - v_t)/dt = -m*f*u_{t+1} + tau_a_y + rho_cw * S * v_{t+1}
 
where S = sqrt(u_{t+1}^2 + v_{t+1}^2) (implicit water drag speed).
 
Method: fixed-point iteration on the scalar speed S, with an inner
analytical solve of the 2x2 linear system at each iteration.
 
At each iteration n:
  alpha = dt * (rho_cw/m) * S^(n)
  Omega = dt * f
  A     = u_t + (dt/m) * tau_a_x
  B     = v_t + (dt/m) * tau_a_y
 
  u^(n+1) = [(1-alpha)*A + Omega*B] / [(1-alpha)^2 + Omega^2]
  v^(n+1) = [(1-alpha)*B - Omega*A] / [(1-alpha)^2 + Omega^2]
  S^(n+1) = sqrt(u^2 + v^2)
"""
 
import numpy as np
 
 
def solve_step(
    u_t: float,
    v_t: float,
    tau_ax: float,
    tau_ay: float,
    m: float = 300.0,
    dt: float = 3600.0,
    f: float = 1.37e-4,
    rho_cw: float = 5.5,
    tol: float = 1e-8,
    max_iter: int = 2000,
    verbose: bool = False,
) -> dict:
    """
    Solve one timestep of the implicit ice-ocean momentum equations.
 
    Parameters
    ----------
    u_t, v_t   : float  — velocity components at time t (m/s)
    tau_ax, tau_ay : float — atmospheric stress components (N/m^2)
    m          : float  — ice mass per unit area (kg/m^2), default 300
    dt         : float  — timestep (s), default 3600
    f          : float  — Coriolis parameter (s^-1), default 1.37e-4 (~70 deg N)
    rho_cw     : float  — ocean drag coefficient rho*C_w (kg/m^3 s), default 5.5
    tol        : float  — convergence tolerance on |delta S| (m/s), default 1e-8
    max_iter   : int    — maximum iterations, default 50
    verbose    : bool   — print iteration log if True
 
    Returns
    -------
    dict with keys:
        u       : u_{t+1} (m/s)
        v       : v_{t+1} (m/s)
        S       : final speed sqrt(u^2 + v^2) (m/s)
        iters   : number of iterations taken
        converged : bool
        history : list of (iter, S, u, v, dS) tuples
    """
    k   = rho_cw / m       # drag per unit mass per speed (m^-1)
    c   = dt * k           # dimensionless drag coefficient
    Om  = dt * f           # dimensionless Coriolis parameter
    A   = u_t + (dt / m) * tau_ax   # known RHS, x
    B   = v_t + (dt / m) * tau_ay   # known RHS, y
 
    # Initial guess: speed at current timestep
    S = np.sqrt(u_t**2 + v_t**2)
    u, v = u_t, v_t
    history = []
 
    for n in range(1, max_iter + 1):
        alpha = c * S
        denom = (1.0 - alpha)**2 + Om**2
 
        u_new = ((1.0 - alpha) * A + Om * B) / denom
        v_new = ((1.0 - alpha) * B - Om * A) / denom
        S_new = np.sqrt(u_new**2 + v_new**2)
 
        dS = abs(S_new - S)
        history.append((n, S_new, u_new, v_new, dS))
 
        if verbose:
            print(f"  iter {n:3d}:  S = {S_new:.6f} m/s  "
                  f"u = {u_new:.6f}  v = {v_new:.6f}  dS = {dS:.2e}")
 
        u, v, S = u_new, v_new, S_new
 
        if dS < tol:
            break
 
    converged = dS < tol
    if not converged:
        print(f"Warning: did not converge in {max_iter} iterations (dS={dS:.2e})")
 
    return dict(u=u, v=v, S=S, iters=n, converged=converged, history=history)
 
 
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
    tau_ax_series   : array-like of length n_steps, atmospheric x-stress (N/m^2)
    tau_ay_series   : array-like of length n_steps, atmospheric y-stress (N/m^2)
    n_steps         : number of timesteps
    **kwargs        : passed to solve_step (m, dt, f, rho_cw, tol, max_iter)
 
    Returns
    -------
    dict with keys:
        u       : array of u velocities (length n_steps+1)
        v       : array of v velocities (length n_steps+1)
        S       : array of speeds       (length n_steps+1)
        iters   : array of iteration counts per step
    """
    u_arr = np.zeros(n_steps + 1)
    v_arr = np.zeros(n_steps + 1)
    S_arr = np.zeros(n_steps + 1)
    iter_arr = np.zeros(n_steps, dtype=int)
 
    u_arr[0], v_arr[0] = u0, v0
    S_arr[0] = np.sqrt(u0**2 + v0**2)
 
    for i in range(n_steps):
        res = solve_step(
            u_arr[i], v_arr[i],
            tau_ax_series[i], tau_ay_series[i],
            **kwargs
        )
        u_arr[i+1]  = res['u']
        v_arr[i+1]  = res['v']
        S_arr[i+1]  = res['S']
        iter_arr[i] = res['iters']
 
    return dict(u=u_arr, v=v_arr, S=S_arr, iters=iter_arr)
 
 
# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
 
    print("=" * 55)
    print("Example 1: single timestep, verbose iteration log")
    print("=" * 55)
    result = solve_step(
         u_t=6.7, v_t=-0.9,
        tau_ax=6.711e-2, tau_ay=8.45e-3,
        m=22, dt=10800.0, f=1.26e-4, rho_cw=-.536,
        verbose=True,
    )
    print(f"\nConverged: {result['converged']}  ({result['iters']} iterations)")
    print(f"  u_{{t+1}} = {result['u']:.6f} m/s")
    print(f"  v_{{t+1}} = {result['v']:.6f} m/s")
    print(f"  S       = {result['S']:.6f} m/s")
 
    # print()
    # print("=" * 55)
    # print("Example 2: 24-hour integration with constant forcing")
    # print("=" * 55)
    # import matplotlib.pyplot as plt
 
    # n_steps = 24
    # dt = 3600.0
    # tau_ax_arr = np.full(n_steps, 0.2)
    # tau_ay_arr = np.full(n_steps, 0.05)
 
    # traj = time_integrate(
    #     u0=0.0, v0=0.0,
    #     tau_ax_series=tau_ax_arr,
    #     tau_ay_series=tau_ay_arr,
    #     n_steps=n_steps,
    #     m=300.0, dt=dt, f=1.37e-4, rho_cw=5.5,
    # )
 
    # t_hours = np.arange(n_steps + 1)
 
    # fig, axes = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
 
    # axes[0].plot(t_hours, traj['u'], label='u (x)', color='#185FA5')
    # axes[0].plot(t_hours, traj['v'], label='v (y)', color='#D85A30')
    # axes[0].set_ylabel("Velocity (m/s)")
    # axes[0].legend()
    # axes[0].grid(True, linewidth=0.5, alpha=0.5)
    # axes[0].set_title("Ice velocity — implicit solver (24 h, constant forcing)")
 
    # axes[1].plot(t_hours, traj['S'], color='#0F6E56')
    # axes[1].set_ylabel("Speed S (m/s)")
    # axes[1].set_xlabel("Time (hours)")
    # axes[1].grid(True, linewidth=0.5, alpha=0.5)
 
    # plt.tight_layout()
    # plt.savefig("/mnt/user-data/outputs/ice_ocean_trajectory.png", dpi=150)
    # print("Plot saved to ice_ocean_trajectory.png")
    # plt.show()
 
    # print(f"\nMean iterations per step: {traj['iters'].mean():.1f}")
    # print(f"Final speed: {traj['S'][-1]:.4f} m/s")