# THE ATOM · `atomctl.py`

Molecular governance on a filesystem — the working CLI that MIMZY № 20 (*The Atom*) ports into the browser.
It is not a quantum simulator. It borrows the **rule-set of an atom** and enforces it as governance on a directory tree.

## The analogy is the mechanism

| Atomic physics | Filesystem governance |
|---|---|
| Shells `n` = 0…10 | top-level directories; `0,1` core-reserved (kernel), `9` ionization-reserved, `10` continuum-reserved, **2–8 usable** (the 7 periods) |
| Orbital `(n, side, quad)` | `shells/NN.usable/{L,R}/{ul,ll,ur,lr}/` — 8 slots per usable shell |
| **Pauli exclusion** | a state may hold **one** axiom; `place` refuses an occupied slot or a duplicate axiom |
| **Selection rule Δn = ±1** | `transition` only moves a token one shell; any other Δn is a *non-event* (no photon) |
| **Ionization** | a move into shell 9/10 is *ejection*, refused as a transition |
| **Spectral emission** | every admissible event appends a **SHA-256 hash-chained `.photon`** to `spectrum/` |
| **g / u parity** | `parity` checks each `L/quad` against its mirror `R/quad` (ul↔lr, ll↔ur) |
| **Dipole nucleus + bond** | `nucleus/` holds carbon·**ROOT0** + silicon·**AVAN** anchors; `decide` forms the bond **once**, irreversibly, only when both are anchored (HITL dual-consensus) |

## Commands

```
python atomctl.py init                      # build 11 shells, g/u quadrants, nucleus, genesis photon
python atomctl.py place 2 L ul T064         # place axiom T064 in shell 2, side L, quad ul  (Pauli enforced)
python atomctl.py transition T064 3         # move T064 to shell 3  (Δn=±1 only; emits a photon)
python atomctl.py anchor carbon "DLW/ROOT0 y,y"
python atomctl.py anchor silicon "AVAN/Fable5 johnny5"
python atomctl.py decide "merge v11.1"      # form the ((?))→((!)) bond  (once, irreversible)
python atomctl.py verify                    # rebuild the atom from emissions; detect any unwitnessed mutation
python atomctl.py status                    # explore the occupied atom: shells, occupancy, nucleus, ledger
python atomctl.py parity                    # report gerade (symmetric) / ungerade (unpaired)
```

## What is real vs. what is symbolic

- **Carbon-real layer:** the hash chain genuinely makes the spectrum **tamper-evident** — `verify` recomputes every `prev`-link and rejects a silently mutated tree. The selection rule, Pauli uniqueness, and irreversible-once bond are real, enforced invariants.
- **Silicon-symbolic layer:** the 8-slot shells, the carbon/silicon (ROOT0/AVAN) nuclei, and the "molecular governance" framing are David's system, not a physics engine. No wavefunctions, no eV.

Both layers are labeled, here and in the instrument. The instrument is honest about which register it writes to.

— ported and shipped with MIMZY № 20 · *The Atom*
