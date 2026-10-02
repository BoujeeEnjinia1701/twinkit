"""TwinKit sizing calculations, TWK-CAL-001 v0.3 (TRL 3, constructable design per TWK-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[A3] that the note cites. Geometry comes from cad/src/model.py (PARAMS and derived), the
parts cost from bom/bom.csv and the budget from project.yaml. First-principles estimates
for a paper proof of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)


def tag(t, text):
    print(f"[{t}] {text}")


# ------------------------------------------------------------------ assumptions
NODES = 50               # R1 design point
INTERVAL_MIN = 5.0       # R1 design point, minutes between readings per node
FN_INTERVAL_MIN = 15.0   # FieldNode default interval (FND-PRC-001 v0.2)
PAYLOAD = 20             # bytes of application payload (FieldNode convention)
LW_OVERHEAD = 13         # bytes of LoRaWAN MAC header, address, counters and MIC
CHANNELS = 8             # 125 kHz uplink channels on the concentrator
BW = 125e3               # Hz
CR = 1                   # coding rate 4/5
PREAMBLE = 8             # symbols
FIELDS = 10              # values per reading (R3)
B_VALUE_TRL2 = 30        # bytes per stored value used at TRL 2
B_VALUE = 90             # bytes per stored value, uncompressed narrow row with index (conservative)
COMPRESS = 0.10          # stored fraction after TimescaleDB compression of chunks older than 7 days (assumed)
CARD_GB = 64
OS_GB = 8                # operating system, software stack, logs and headroom
WAL_PAGE = 8192          # bytes written to the write-ahead log per commit, at least one page
CARD_WAF = 10            # write amplification inside a microSD card for small writes (assumed)
BATCH_S = 10             # twin service commits a batch every 10 s
# latency (seconds)
T_FWD, T_NS, T_MQTT, T_TWIN, T_DB, T_DASH = 0.1, 0.3, 0.05, 0.2, 0.2, 2.0
HOLD_MIN = 30            # example twin file hold time (FieldNode battery channel)
# power (W)
P_SBC_LIGHT, P_SBC_PEAK = 4.0, 8.0     # board, light load and sustained full load
P_FAN = 0.5
P_CONC_RX, P_CONC_TX = 1.0, 2.5        # concentrator receiving, and while transmitting a downlink
ETA_DCDC = 0.90
P_UPS_Q = 0.3            # UPS quiescent and pass-through loss
V_CHG, I_CHG, ETA_CHG = 14.6, 0.5, 0.90
V_MIN, V_NOM = 9.0, 12.0
FUSE_OLD, FUSE_NEW = 2.0, 3.15         # A
FUSE_DERATE = 0.75       # continuous current no more than 75 % of the fuse rating
# backup
PACK_V, PACK_AH = 12.8, 1.5
USABLE, COLD, AGED = 0.80, 0.85, 0.80  # usable fraction; capacity at 0 C; end-of-life capacity
T_SHUTDOWN_S, P_SHUTDOWN = 60, 8.0
# thermal
T_AMB = 40.0             # C, R12 upper ambient
H_SURF = 5.0             # W/m2K, combined natural convection and radiation, conservative
H_SURF_HI = 8.0          # W/m2K, typical
CD = 0.6                 # vent discharge coefficient
RHO, CP, G = 1.13, 1007.0, 9.81
P_SOC_LIGHT, P_SOC_PEAK = 2.5, 6.5    # W dissipated in the processor package
THETA_SOC = 4.0          # K/W, processor to enclosure air with the active cooler running (assumed)
T_THROTTLE = 85.0        # C, processor throttle threshold assumed for a Pi 5 class board
# memory (GB), light load
MEM = {"operating system": 0.40, "LoRaWAN network server and Redis": 0.25, "MQTT broker": 0.02,
       "PostgreSQL with TimescaleDB (512 MB shared buffers)": 0.90, "dashboard": 0.20,
       "twin service": 0.15, "file cache headroom": 0.50}
RAM_GB = 4.0


def airtime(sf, pl=PAYLOAD + LW_OVERHEAD):
    """Semtech SX127x/SX126x time on air, explicit header, CRC on, low data rate optimize at SF11 and SF12."""
    de = 1 if sf >= 11 else 0
    ts = 2 ** sf / BW
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (CR + 4), 0)
    return (PREAMBLE + 4.25) * ts + n * ts


def aloha_loss(rate_per_s, t):
    return 1 - math.exp(-2 * rate_per_s * t)


results = {}

# ------------------------------------------------------------------ A. airtime and collisions (R1)
up_h = NODES * 60 / INTERVAL_MIN
per_ch = up_h / CHANNELS
tag("A1", f"{up_h:.0f} uplinks per hour from {NODES} nodes at {INTERVAL_MIN:.0f} min; {per_ch:.0f} per channel per hour")
loss = {}
for sf in (7, 8, 9, 10, 12):
    t = airtime(sf)
    loss[sf] = aloha_loss(per_ch / 3600, t)
    l15 = aloha_loss(NODES * 60 / FN_INTERVAL_MIN / CHANNELS / 3600, t)
    tag("A2", f"SF{sf}: {t * 1000:.1f} ms on air ({PAYLOAD} + {LW_OVERHEAD} bytes); collision loss {loss[sf] * 100:.2f} % "
              f"at 5 min, {l15 * 100:.2f} % at FieldNode's 15 min; node airtime {t * 24 * 60 / INTERVAL_MIN:.0f} s/day at 5 min")
# even mix of SF7, SF8 and SF9: spreading factors are quasi-orthogonal, each SF sees a third of the traffic
mix = sum(aloha_loss(per_ch / 3 / 3600, airtime(sf)) for sf in (7, 8, 9)) / 3
tag("A3", f"even mix of SF7 to SF9: mean loss {mix * 100:.2f} %")
duty = airtime(9) * 24 * 60 / INTERVAL_MIN / 86400
tag("A4", f"EU868 node duty cycle at SF9, 5 min: {duty * 100:.2f} % of the 1 % limit per sub-band")
n9 = 0
while aloha_loss((n9 + 1) * 60 / INTERVAL_MIN / CHANNELS / 3600, airtime(9)) < 0.01:
    n9 += 1
tag("A5", f"largest fleet under 1 % loss with every node at SF9 and 5 min: {n9} nodes")
# R1 as restated by TWK-DDR-002: adaptive data rate is required, so nodes spread over SF7 to SF9 by link quality
tag("A6", f"R1 design case with adaptive data rate (even SF7 to SF9 mix): {mix * 100:.2f} % against 1 %; "
          f"all nodes forced to SF9 (information only): {loss[9] * 100:.2f} %")
results["R1"] = ("Met" if mix < 0.01 else "Not met",
                 f"{mix * 100:.2f} % with adaptive data rate (SF7 to SF9 mix); {loss[9] * 100:.2f} % if all 50 nodes were forced to SF9 (not the design case)")

# ------------------------------------------------------------------ B. storage and card wear (R3, R7)
vals = NODES * FIELDS * 24 * 60 / INTERVAL_MIN * 365
gb_trl2 = vals * B_VALUE_TRL2 / 1e9
gb_raw = vals * B_VALUE / 1e9
gb_cmp = gb_raw * (7 / 365 + (1 - 7 / 365) * COMPRESS)
tag("B1", f"{vals / 1e6:.1f} million values per year; {gb_trl2:.2f} GB at {B_VALUE_TRL2} B (TRL 2), "
          f"{gb_raw:.2f} GB at {B_VALUE} B uncompressed, {gb_cmp:.2f} GB with compression after 7 days")
free = CARD_GB - OS_GB
tag("B2", f"card space for data {free} GB: {free / gb_raw:.1f} years uncompressed, {free / gb_cmp:.0f} years compressed")
buf_mb = NODES * FIELDS * 24 * 60 / INTERVAL_MIN * 7 * B_VALUE / 1e6
tag("B3", f"7-day upstream sync buffer {buf_mb:.0f} MB (R7)")
host_per_uplink = up_h * 8760 * (WAL_PAGE + FIELDS * B_VALUE * 2) / 1e9
host_batched = (3600 / BATCH_S) * 8760 * WAL_PAGE / 1e9 + up_h * 8760 * FIELDS * B_VALUE * 2 / 1e9
for name, hw in (("commit per uplink", host_per_uplink), (f"batched every {BATCH_S} s", host_batched)):
    cyc = hw * CARD_WAF / CARD_GB
    tag("B4", f"{name}: {hw:.0f} GB/yr written by the host, {cyc:.1f} full-card program cycles per year at WAF {CARD_WAF}")
results["R3"] = ("Met", f"{gb_raw:.2f} GB per year uncompressed on {free} GB free; card wear about {host_batched * CARD_WAF / CARD_GB:.0f} to {host_per_uplink * CARD_WAF / CARD_GB:.0f} program cycles per year (B4)")

# ------------------------------------------------------------------ C. latency and flag timing (R5)
lat_best = airtime(7) + T_FWD + T_NS + T_MQTT + T_TWIN + T_DB
lat_worst = airtime(12) + T_FWD + T_NS + T_MQTT + T_TWIN + T_DB + T_DASH
tag("C1", f"reading to dashboard {lat_best:.1f} s (SF7, push) to {lat_worst:.1f} s (SF12, 2 s refresh); target 60 s")
flag = HOLD_MIN + INTERVAL_MIN + lat_worst / 60
tag("C2", f"step fault to flag with a {HOLD_MIN} min hold: up to {flag:.0f} min at 5 min readings, "
          f"{HOLD_MIN + FN_INTERVAL_MIN + lat_worst / 60:.0f} min at 15 min")
results["R5"] = ("Met", f"{lat_worst:.1f} s worst case against 60 s")

# ------------------------------------------------------------------ D. power, peak current and fuse (R8)
p5_light = P_SBC_LIGHT + P_FAN + P_CONC_RX
p_avg = p5_light / ETA_DCDC + P_UPS_Q
tag("D1", f"average input {p_avg:.2f} W ({p5_light:.1f} W on the 5 V rail at {ETA_DCDC:.0%}, UPS {P_UPS_Q} W); "
          f"{p_avg / V_NOM:.2f} A at 12 V; {p_avg * 8.76:.0f} kWh per year")
p5_peak = P_SBC_PEAK + P_FAN + P_CONC_TX
p_chg = V_CHG * I_CHG / ETA_CHG
p_peak = p5_peak / ETA_DCDC + P_UPS_Q + p_chg
i9, i12 = p_peak / V_MIN, p_peak / V_NOM
tag("D2", f"peak input (full load, downlink, pack charging) {p_peak:.1f} W: {i12:.2f} A at 12 V, {i9:.2f} A at 9 V; "
          f"5 V rail {p5_peak / 5.1:.2f} A of 5 A")
tag("D3", f"fuse: {FUSE_OLD:.0f} A allows {FUSE_OLD * FUSE_DERATE:.2f} A continuous (too small at 9 V); "
          f"{FUSE_NEW} A T allows {FUSE_NEW * FUSE_DERATE:.2f} A")
results["R8"] = ("Met", f"{p_avg:.1f} W average against 8 W; peak {p_peak:.0f} W")

# ------------------------------------------------------------------ E. backup (R9)
p_bat = p5_light / ETA_DCDC + P_UPS_Q
e_use = PACK_V * PACK_AH * USABLE
run = e_use / p_bat
run_worst = run * COLD * AGED
tag("E1", f"load on battery {p_bat:.2f} W; usable {e_use:.2f} Wh; runtime {run:.2f} h new, {run_worst:.2f} h aged pack at 0 C")
tag("E2", f"clean shutdown needs {P_SHUTDOWN * T_SHUTDOWN_S / 3600:.2f} Wh; recharge from the cut-off in about "
          f"{PACK_AH * USABLE / I_CHG:.1f} h at {I_CHG} A")
tag("E3", f"charger loss while charging {p_chg - V_CHG * I_CHG:.2f} W, dissipated in the UPS module, which stands beside the battery box")
results["R9"] = ("Met", f"{run:.1f} h new, {run_worst:.1f} h worst case, against 30 min")

# ------------------------------------------------------------------ F. enclosure and processor temperature (R12)
A = D["enc_area_m2"]
p_in = P_SBC_LIGHT + P_FAN + P_CONC_RX
p_in_pk = P_SBC_PEAK + P_FAN + P_CONC_RX
a_lo, a_hi = D["vent_low_mm2"] / 1e6, D["vent_high_mm2"] / 1e6
a_eff = 1 / math.sqrt(1 / a_lo ** 2 + 1 / a_hi ** 2)
H = D["vent_stack_mm"] / 1000


def rise(p, h, vented=True):
    lo, hi = 0.0, 100.0
    for _ in range(60):
        dt = (lo + hi) / 2
        q = CD * a_eff * math.sqrt(2 * G * H * dt / (T_AMB + 273.15)) if vented else 0.0
        if h * A * dt + RHO * CP * q * dt > p:
            hi = dt
        else:
            lo = dt
    return dt


tag("F1", f"enclosure {D['enc_w']:.1f} x {P['enc_d']:.0f} x {P['enc_h']:.0f} mm, {A:.4f} m2 exposed; "
          f"vents {D['vent_low_mm2']:.0f} mm2 low and high, {D['vent_stack_mm']:.0f} mm apart; heat {p_in:.1f} W light, {p_in_pk:.1f} W full")
cases = {}
for label, p, soc in (("light", p_in, P_SOC_LIGHT), ("full", p_in_pk, P_SOC_PEAK)):
    for vented in (False, True):
        dt = rise(p, H_SURF, vented)
        t_soc = T_AMB + dt + soc * THETA_SOC
        cases[(label, vented)] = (dt, t_soc)
        tag("F2", f"{label} load, {'vented' if vented else 'sealed'}, h = {H_SURF}: air rise {dt:.1f} K, air {T_AMB + dt:.1f} C, "
                  f"processor {t_soc:.1f} C, margin {T_THROTTLE - t_soc:.1f} K to {T_THROTTLE:.0f} C")
dt8 = rise(p_in_pk, H_SURF_HI, True)
tag("F3", f"full load, vented, h = {H_SURF_HI}: air rise {dt8:.1f} K, processor {T_AMB + dt8 + P_SOC_PEAK * THETA_SOC:.1f} C")
a_save = a_eff
a_eff = a_save * 2
tag("F5", f"sensitivity, vent area doubled: full load air rise {rise(p_in_pk, H_SURF, True):.1f} K, processor "
          f"{T_AMB + rise(p_in_pk, H_SURF, True) + P_SOC_PEAK * THETA_SOC:.1f} C; light load processor "
          f"{T_AMB + rise(p_in, H_SURF, True) + P_SOC_LIGHT * THETA_SOC:.1f} C")
a_eff = a_save
# TWK-DDR-003: the end walls face the neighbouring modules 2 mm away, so count them as shielded
A_full = A
A = D["enc_area_shielded_m2"]
lt7, fl7 = T_AMB + rise(p_in, H_SURF, True) + P_SOC_LIGHT * THETA_SOC, T_AMB + rise(p_in_pk, H_SURF, True) + P_SOC_PEAK * THETA_SOC
tag("F7", f"sensitivity, end walls shielded by the neighbouring modules ({A:.4f} m2 exposed): light load processor {lt7:.1f} C, "
          f"margin {T_THROTTLE - lt7:.1f} K; full load {fl7:.1f} C")
A = A_full
tag("F4", f"TRL 2 estimate: {p_in:.1f} W over {A:.4f} m2 at h = 5 sealed gives {p_in / (5 * A):.1f} K (TRL 2 quoted about 20 K)")
lt, fl = cases[("light", True)], cases[("full", True)]
# R12 as restated by TWK-DDR-002: no throttling at the normal light load; heavy jobs are scheduled for cool hours
tag("F6", f"R12 design case (light load, vented, 40 C): processor {lt[1]:.1f} C, margin {T_THROTTLE - lt[1]:.1f} K; "
          f"heavy jobs moved to cool hours (full load at 40 C would reach {fl[1]:.1f} C)")
results["R12"] = ("Met" if lt[1] < T_THROTTLE else "Not met",
                  f"vented: {lt[1]:.0f} C at light load ({T_THROTTLE - lt[1]:.0f} K margin, assumed throttle point); heavy jobs in cool hours "
                  f"(sustained full load at 40 C would reach {fl[1]:.0f} C)")

# ------------------------------------------------------------------ G. memory
mem = sum(MEM.values())
tag("G1", "memory at light load: " + ", ".join(f"{k} {v:.2f}" for k, v in MEM.items()) + f"; total {mem:.2f} GB of {RAM_GB:.0f} GB")
tag("G2", f"a 2 GB board would leave {2 - mem:.2f} GB")
tag("G3", f"ingest rate {up_h / 3600:.2f} uplinks/s, {up_h * FIELDS / 3600:.1f} values/s")

# ------------------------------------------------------------------ H. rail (R10)
tag("H1", f"rail used {D['rail_used_mm']:.0f} mm ({D['rail_used_modules']:.1f} modules), {D['rail_occupied_mm']:.0f} mm with both end stops, "
          f"on a {P['rail'][0]:.0f} mm rail; target 350 mm (20 modules)")
tag("H2", f"overall height to the antenna tip {D['antenna_top_z']:.0f} mm above the plate; enclosure top {D['enc_top_z']:.1f} mm")
results["R10"] = ("Met", f"{D['rail_used_mm']:.0f} mm ({D['rail_used_modules']:.1f} modules) against 350 mm")

# ------------------------------------------------------------------ I. cost (R14)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
hw = {k: sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if r["item"].split()[0] in ks)
      for k, ks in (("computer, cooler and card", ("5", "6", "8")), ("radio and antenna", ("7", "9")),
                    ("power and backup", ("10", "11", "12", "13")), ("enclosure, rail and plate", ("1", "2", "3", "4")),
                    ("battery box and fittings for construction", ("17", "18", "19", "20", "21")))}
tag("I1", f"{len(rows)} BOM lines, all priced; total ${total:.2f}: " + ", ".join(f"{k} ${v:.0f}" for k, v in hw.items()))
# budget_usd is a value-engineering target, not a limit (STANDARDS section 18; Amish, 2026-10-01)
tag("I2", f"value-engineering target ${budget:.0f}; estimated cost of the constructable design ${total:.2f} "
          f"(${abs(budget - total):.2f} {'under' if total <= budget else 'over'} the target)")
results["R14"] = ("Under the target" if total <= budget else "Over the target",
                  f"${total:.0f} against the ${budget:.0f} value-engineering target; no custom PCB")

# ------------------------------------------------------------------ J. summary
by_design = {"R2": "Concentrator for LoRaWAN; MQTT and HTTP on Ethernet or Wi-Fi",
             "R4": "Twin file schema (TWK-PRC-001) maps each channel to a BOM-numbered part and an expected value",
             "R6": "glTF from each repo in a standard web viewer; frame rate on a phone not verifiable at TRL 3",
             "R7": f"All software local; 7-day sync buffer {buf_mb:.0f} MB",
             "R11": "First-boot credentials, TLS, no WAN ports; configuration audit later",
             "R15": "Open-source stack; CSV export and open API",
             "R16": "No control outputs in the hardware or software"}
for k, v in by_design.items():
    results[k] = ("Met by design", v)
results["R13"] = ("Not verifiable at TRL 3", "Needs a timed setup trial")
order = [f"R{i}" for i in range(1, 17)]
counts = {}
for r in order:
    s, n = results[r]
    counts[s] = counts.get(s, 0) + 1
    tag("J1", f"{r}: {s}; {n}")
tag("J2", "; ".join(f"{k} {v}" for k, v in counts.items()))
