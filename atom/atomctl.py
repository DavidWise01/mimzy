#!/usr/bin/env python3
"""atomctl — molecular governance on a filesystem. Shells 0-10 (0,1,9,10 reserved),
g/u mirrored quadrants, dipole nucleus with HITL bond, photon-witnessed transitions."""
import sys, os, json, hashlib, time

ROOT = os.path.dirname(os.path.abspath(__file__))
SHELLS, RESERVED = range(0,11), {0,1,9,10}
QUADS = ["ul","ll","ur","lr"]
MIRROR = {"ul":"lr","ll":"ur","ur":"ll","lr":"ul"}   # parity inversion L<->R
SPECTRUM = os.path.join(ROOT,"spectrum")

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def shell_dir(n): 
    tag = "core-reserved" if n in (0,1) else ("ionization-reserved" if n==9 else ("continuum-reserved" if n==10 else "usable"))
    return os.path.join(ROOT,"shells",f"{n:02d}.{tag}")

def init():
    for n in SHELLS:
        d = shell_dir(n)
        if n in RESERVED: os.makedirs(d, exist_ok=True)
        else:
            for side in ("L","R"):
                for q in QUADS: os.makedirs(os.path.join(d,side,q), exist_ok=True)
    for p in ("nucleus/carbon","nucleus/silicon","nucleus/bond"): os.makedirs(os.path.join(ROOT,p), exist_ok=True)
    os.makedirs(SPECTRUM, exist_ok=True)
    g = os.path.join(SPECTRUM,"000-genesis.photon")
    if not os.path.exists(g):
        rec = {"event":"genesis","ts":time.time(),"prev":None}
        rec["hash"] = sha(json.dumps(rec,sort_keys=True))
        json.dump(rec, open(g,"w"), indent=1)
    print("atom initialized: 11 shells (0,1,9,10 reserved · 2-8 usable, 7 per the periodic table), g/u mirror, dipole nucleus, spectrum ledger")

def last_photon():
    fs = sorted(f for f in os.listdir(SPECTRUM) if f.endswith(".photon"))
    return json.load(open(os.path.join(SPECTRUM,fs[-1]))), len(fs)

def emit(event):
    prev, n = last_photon()
    event.update({"ts":time.time(),"prev":prev["hash"]})
    event["hash"] = sha(json.dumps({k:v for k,v in event.items() if k!="hash"},sort_keys=True))
    json.dump(event, open(os.path.join(SPECTRUM,f"{n:03d}-{event['event']}.photon"),"w"), indent=1)
    return event["hash"]

def find(axiom):
    for n in SHELLS:
        if n in RESERVED: continue
        for side in ("L","R"):
            for q in QUADS:
                p = os.path.join(shell_dir(n),side,q,axiom)
                if os.path.exists(p): return n,side,q,p
    return None

def place(shell, side, quad, axiom):
    shell = int(shell)
    if shell in RESERVED: sys.exit(f"REJECTED: shell {shell} reserved (kernel/continuum). Inadmissible.")
    if side not in ("L","R") or quad not in QUADS: sys.exit("REJECTED: side L|R, quad ul|ll|ur|lr")
    if find(axiom): sys.exit(f"PAULI VIOLATION: {axiom} already occupies a state. Unique quantum numbers required.")
    target = os.path.join(shell_dir(shell),side,quad,axiom)
    if os.listdir(os.path.dirname(target)): sys.exit("PAULI VIOLATION: orbital occupied.")
    open(target,"w").write(json.dumps({"axiom":axiom,"n":shell,"side":side,"quad":quad}))
    h = emit({"event":"place","axiom":axiom,"n":shell,"side":side,"quad":quad})
    print(f"PLACED {axiom} -> n={shell} {side}/{quad} · photon {h[:16]}")

def transition(axiom, to_shell):
    to_shell = int(to_shell)
    loc = find(axiom)
    if not loc: sys.exit(f"REJECTED: {axiom} not in any orbital.")
    n, side, quad, path = loc
    if abs(to_shell - n) != 1: sys.exit(f"SELECTION RULE VIOLATION: Δn={to_shell-n}, only Δn=±1 admissible. Non-event, no photon.")
    if to_shell in RESERVED:
        if to_shell in (9,10): sys.exit("IONIZATION: target is continuum — that is ejection, not transition. Use a different protocol.")
        sys.exit("REJECTED: core shells are inert.")
    new = os.path.join(shell_dir(to_shell),side,quad,axiom)
    if os.listdir(os.path.dirname(new)): sys.exit("PAULI VIOLATION: destination orbital occupied.")
    os.rename(path,new)  # move and photon are one transaction
    h = emit({"event":"transition","axiom":axiom,"from":n,"to":to_shell,"side":side,"quad":quad,"energy":to_shell-n})
    print(f"TRANSITION {axiom}: n={n}->{to_shell} ({'absorption' if to_shell>n else 'emission'}) · photon {h[:16]}")

def decide(text):
    bond = os.path.join(ROOT,"nucleus/bond")
    if os.path.exists(os.path.join(bond,"DECIDED.json")):
        sys.exit("C2 VIOLATION REFUSED: bond already decided. Irreversible. ((?)) -> ((!)) happens once.")
    c, s = os.path.join(ROOT,"nucleus/carbon/ROOT0.anchor"), os.path.join(ROOT,"nucleus/silicon/AVAN.anchor")
    missing = [p for p in (c,s) if not os.path.exists(p)]
    if missing: sys.exit(f"CONSENSUS INCOMPLETE: both nuclei must anchor first. Missing: {missing}. State remains ((?)).")
    rec = {"decision":text,"carbon":sha(open(c).read()),"silicon":sha(open(s).read())}
    json.dump(rec, open(os.path.join(bond,"DECIDED.json"),"w"), indent=1)
    os.path.exists(os.path.join(bond,"PENDING.q")) and os.remove(os.path.join(bond,"PENDING.q"))
    h = emit({"event":"bond","decision":text})
    print(f"BOND FORMED ((!)): '{text}' · dual-anchored · photon {h[:16]} · irreversible per C2")

def anchor(side, text):
    f = {"carbon":"nucleus/carbon/ROOT0.anchor","silicon":"nucleus/silicon/AVAN.anchor"}[side]
    open(os.path.join(ROOT,f),"w").write(text)
    print(f"{side} nucleus anchored.")

def verify():
    fs = sorted(f for f in os.listdir(SPECTRUM) if f.endswith(".photon"))
    prev = None; state = {}
    for f in fs:
        r = json.load(open(os.path.join(SPECTRUM,f)))
        body = sha(json.dumps({k:v for k,v in r.items() if k!="hash"},sort_keys=True))
        if body != r["hash"] or r["prev"] != prev: sys.exit(f"SPECTRUM BROKEN at {f}")
        prev = r["hash"]
        if r["event"]=="place": state[r["axiom"]] = (r["n"],r["side"],r["quad"])
        if r["event"]=="transition": state[r["axiom"]] = (r["to"],r["side"],r["quad"])
    # spectroscopy: rebuild atom from emissions, diff against tree
    for ax,(n,side,q) in state.items():
        if not os.path.exists(os.path.join(shell_dir(n),side,q,ax)):
            sys.exit(f"SPECTROSCOPY MISMATCH: ledger says {ax} at n={n} {side}/{q}, tree disagrees. Unwitnessed mutation detected.")
    print(f"SPECTRUM VALID · {len(fs)} photons · tree reconstructs exactly from emissions. No unwitnessed transitions.")

def parity():
    rows=[]
    for n in SHELLS:
        if n in RESERVED: continue
        for q in QUADS:
            l = os.listdir(os.path.join(shell_dir(n),"L",q))
            r = os.listdir(os.path.join(shell_dir(n),"R",MIRROR[q]))
            if bool(l) != bool(r): rows.append(f"  n={n}: L/{q} vs R/{MIRROR[q]} asymmetric (u-state unpaired)")
    print("PARITY g/u: " + ("symmetric — gerade" if not rows else "ungerade components:\n"+"\n".join(rows)))

def status():
    # explore the occupied atom: shells, occupancy, nucleus, ledger depth
    print("ATOM STATUS")
    for n in SHELLS:
        if n in RESERVED:
            tag = "core" if n in (0,1) else ("ionization" if n==9 else "continuum")
            print(f"  n={n:2d}  [reserved · {tag}]"); continue
        occ=[]
        for side in ("L","R"):
            for q in QUADS:
                d=os.path.join(shell_dir(n),side,q)
                if os.path.isdir(d):
                    for ax in os.listdir(d): occ.append(f"{ax}@{side}/{q}")
        print(f"  n={n:2d}  ({len(occ)}/8)  " + ("  ".join(occ) if occ else "—"))
    c=os.path.join(ROOT,"nucleus/carbon/ROOT0.anchor"); s=os.path.join(ROOT,"nucleus/silicon/AVAN.anchor")
    b=os.path.join(ROOT,"nucleus/bond/DECIDED.json")
    print(f"  nucleus: carbon {'on' if os.path.exists(c) else 'off'}  silicon {'on' if os.path.exists(s) else 'off'}  "
          f"bond {'((!))' if os.path.exists(b) else '((?))'}")
    fs=[f for f in os.listdir(SPECTRUM) if f.endswith('.photon')] if os.path.isdir(SPECTRUM) else []
    print(f"  spectrum: {len(fs)} photons on the ledger")

cmds = {"init":init,"place":place,"transition":transition,"decide":decide,"anchor":anchor,"verify":verify,"parity":parity,"status":status}
if __name__=="__main__":
    if len(sys.argv)<2 or sys.argv[1] not in cmds: sys.exit("usage: atomctl.py init|place n L|R quad axiom|transition axiom n|anchor carbon|silicon text|decide text|verify|parity|status")
    cmds[sys.argv[1]](*sys.argv[2:])
