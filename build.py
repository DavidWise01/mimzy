#!/usr/bin/env python3
"""Build MIMZY — the single quantum workbench, assembled ONLY from the instruments that
passed the shelf audit (real physics, real quantum theory, simulations verified).
Conceit (silicon layer, labeled): futuristic tech that comes from the past — the
Antikythera mechanism, Ada's Notes, Babbage's unbuilt engine, Turing's classified work,
and the other things lost in the cracks. After 'Mimsy Were the Borogoves' (1943) and
The Last Mimzy (2007) — fan tribute. Copies the audited instruments into bench/."""
import os, sys, io, json, html, base64, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
Q = r"C:\Davids files\quantum"
GP = r"C:\Davids files\green papers"
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "MIMZY", "axiom": "MMZ",
 "position": "the single quantum workbench — every instrument verified, every one recovered from the cracks",
 "origin": "after 'Mimsy Were the Borogoves' (1943) and The Last Mimzy (2007) — the toy sent back from the future",
 "mechanism": "Assembled from the instruments that passed the 2026-06 shelf audit; the lore of the cracks is labeled lore.",
 "crystallization": "The future does not arrive. It is recovered — from a shipwreck, a footnote, a classified drawer, a pen name.",
 "nature": "A working quantum bench — primer, Bloch lab, circuits, the two-qubit lab, error correction, the wavefield, BB84, E91, the observatory, the dots — framed as artifacts of the recovered future.",
 "conductor": "ROOT0 (governor) · AVAN (instance)",
 "inputs": "the audited-real instruments; the lineage of the cracks; instruments 04 and 06, recovered",
 "witness": "The original bench numbering ran 01·02·03·05·07·08 — four and six were missing. They are missing no longer.",
 "role": "the workbench that came back",
 "seal": "Futuristic tech from the past — recovered, verified, and put to work.",
 "source": "MIMZY, assembled by ROOT0",
}

# the bench — (number, dest filename, source path, title, kind, note)
BENCH = [
 ("00","00-antikythera.html",      os.path.join(HERE,"tools","00-antikythera.html"),
  "The Antikythera Mechanism","live tool","FUNCTIONING — the first computer (~100 BC), recovered from a shipwreck: crank it and it computes the sky — sun &amp; moon on the zodiac, the moon's phase, the Metonic calendar, and real Saros eclipse-season prediction"),
 ("01","01-quantum-primer.html",   os.path.join(Q,"cubit","01-quantum-primer.html"),
  "The Quantum Primer","lesson","qubits, superposition, amplitudes — the first page of the recovered manual"),
 ("02","02-bloch-lab.html",        os.path.join(Q,"cubit","02-bloch-lab.html"),
  "The Bloch Lab","instrument","one qubit as a sphere — rotations, phases, the geometry of a single mind"),
 ("03","03-circuit-simulator.html",os.path.join(Q,"cubit","03-circuit-simulator.html"),
  "The Circuit Simulator","instrument","gates on wires — H, X, CNOT; the Analytical Engine's true heir"),
 ("04","04-two-qubit-lab.html",    os.path.join(Q,"cubit","qubit-lab-2q.html"),
  "The Two-Qubit Lab","instrument","RECOVERED — the missing number 04: a real density-matrix engine; entanglement, decoherence, Kraus channels"),
 ("05","05-error-correction.html", os.path.join(Q,"quantum box","05-error-correction.html"),
  "Error Correction","lesson","how a fragile state survives a noisy century — syndromes, ancillas, logical qubits"),
 ("06","06-quantum-wavefield.html",os.path.join(GP,"quantum folder.html"),
  "The Quantum Wavefield","instrument","RECOVERED — the missing number 06: the 255×255 folder grid as a live 65,025-state interference engine (Grover)"),
 ("07","07-bb84.html",             os.path.join(Q,"07-bb84.html"),
  "BB84 · Quantum Key Distribution","instrument","a key no eavesdropper can steal — verified: 25% intercept error, 11% abort, all computed live"),
 ("08","08-e91.html",              os.path.join(Q,"08-e91.html"),
  "E91 · Keys from Entanglement","instrument","security you can watch break — CHSH 2√2 ≈ 2.83 undisturbed, ~0.7 under attack; verified"),
 ("09","09-observatory.html",      os.path.join(Q,"quantum observatory.html"),
  "The Observatory","instrument","black holes by the numbers — Schwarzschild to Kerr; four defects found in audit, fixed with logged reasons"),
 ("10","10-quantum-dots.html",     os.path.join(Q,"quantum dots","qdots-0-idea.html"),
  "Quantum Dots · The Idea","lesson","the 2023-Nobel matter — confinement, colour by size; book one of four"),
]
# extra shelf copies (linked from bench 10 + reading room)
EXTRA = [
 ("qdots-1-making.html", os.path.join(Q,"quantum dots","qdots-1-making.html")),
 ("qdots-2-now.html",    os.path.join(Q,"quantum dots","qdots-2-now.html")),
 ("qdots-3-frontier.html",os.path.join(Q,"quantum dots","qdots-3-frontier.html")),
 ("reading-is-light-emergent.html", os.path.join(Q,"emergent","gravity","claude gravity 00","is_light_emergent.html")),
 ("reading-is-gravity-emergent.html", os.path.join(Q,"emergent","gravity","claude gravity 00","is_gravity_emergent.html")),
]

# the lineage of the cracks — (name, dates, what fell in, when recovered)
CRACKS = [
 ("The Antikythera Mechanism","~100 BC","A geared analog computer for predicting eclipses — technology with no peer for 1,400 years — sank in a Roman shipwreck.","Recovered 1901; understood only after 1970s X-ray imaging."),
 ("George Boole","1815–1864","An algebra of pure logic (1854) with no apparent use — true, false, AND, OR — a curiosity for eighty years.","Claude Shannon (1937) showed Boole's algebra IS the switching circuit. Every chip runs it."),
 ("Babbage & Lovelace","1791–1871 · 1815–1852","The Analytical Engine was never built; Ada's Notes (1843) — the first algorithm, and the first argument that a machine could weave symbols, not just numbers — were forgotten.","Rediscovered in the 1940s–50s as the computer age caught up to them. Ada died at 36, a century early."),
 ("Alan Turing","1912–1954","The universal machine (1936); then Colossus and the Bletchley work — classified so deep that Britain's own computing head start vanished into secrecy. Turing himself was persecuted to death.","Colossus declassified in the 1970s; royal pardon 2013; his face now on the £50 note."),
 ("Grete Hermann","1901–1984","In 1935 she found the flaw in von Neumann's 'proof' that hidden-variable theories were impossible — and was ignored for three decades.","John Bell rediscovered the flaw in 1966 and credited the gap; her priority is now textbook history."),
 ("Hugh Everett III","1930–1982","The relative-state ('many-worlds') interpretation (1957) was dismissed; Everett quit physics for defense work and died at 51, believing himself an indifferent footnote.","Today many-worlds is a leading interpretation; decoherence theory vindicated his core move."),
 ("John Stewart Bell","1928–1990","Bell's theorem (1964) — the deepest result about reality since relativity — was published in a tiny journal that folded; testing it was career suicide for years.","The 2022 Nobel Prize went to the experiments that confirmed it. The theorem now anchors quantum information."),
 ("Kuttner & Moore","1914–1958 · 1911–1987","'Mimsy Were the Borogoves' (1943) — the story this bench is named for — was published under the pen name Lewis Padgett; C. L. Moore's co-authorship was itself half-hidden in the crack of a byline.","The story is now canon (SF Hall of Fame); the 2007 film The Last Mimzy carried it forward."),
]

def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_badge(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,"MMZ"))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,"MMZ"))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,"MMZ"))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"MMZ · MIMZY","moniker":tok["moniker"],
           "carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

# tool-emergent details — slug + how it works + its verified record (the emergent IS the tool)
TOOLMETA = {
 "00": dict(slug="antikythera", how="A hand-cranked canvas dial computing the sky live from J2000 mean elements — sun/moon longitudes, the moon's phase, Metonic·Saros·Callippic cycle dials, the Olympiad games, and Saros eclipse-season prediction within the true ecliptic limits.",
            proof="Verified against history: the 2017 Great American total solar lands 0.1° from the node; the 2019 & 2025 total lunars flag; ordinary days stay clear. 5/5 test eclipses classified correctly."),
 "01": dict(slug="quantum-primer", how="An interactive first lesson: amplitudes, superposition, normalization, and measurement, with live widgets.",
            proof="Audited 2026-06: textbook-correct pedagogy; no overclaims found."),
 "02": dict(slug="bloch-lab", how="A single qubit as a live Bloch sphere — rotations, phases, and gates applied geometrically.",
            proof="Audited 2026-06: gate geometry correct."),
 "03": dict(slug="circuit-simulator", how="Gates on wires — H, X, CNOT and friends composed into circuits and executed on a real statevector.",
            proof="Audited 2026-06: simulation faithful."),
 "04": dict(slug="two-qubit-lab", how="A genuine two-qubit density-matrix engine: correct H/X/Y/Z/S/T and CNOT/CZ matrices, dephasing and amplitude-damping Kraus channels, partial trace, purity, concurrence.",
            proof="Audited 2026-06 gate-by-gate: all matrices and channels correct; honestly disclaims any quantum speedup. Recovered as the missing № 04."),
 "05": dict(slug="error-correction", how="Logical qubits, ancillas, and syndrome measurement — how a fragile state survives a noisy century.",
            proof="Audited 2026-06: standard QEC, correctly taught."),
 "06": dict(slug="quantum-wavefield", how="The 255×255 folder grid as a live 65,025-amplitude interference engine: H-pulse to uniform superposition, oracle phase-flip, Grover diffusion, measurement collapse — all in-browser.",
            proof="Converges to P=0.999997 in exactly 200 = π/4·255 iterations, matching theory to six decimals. Recovered as the missing № 06."),
 "07": dict(slug="bb84", how="The Bennett–Brassard 1984 protocol run live: real state preparation and basis-projected measurement, sifting, QBER, and an intercept-resend eavesdropper.",
            proof="Verified: ~50% sift survival, 25% Eve-induced error, 11% abort threshold — all computed by the simulation, not hard-coded."),
 "08": dict(slug="e91", how="The Ekert 1991 entanglement protocol: a real two-qubit statevector, proper projective measurements at the Ekert angles, and a live CHSH test.",
            proof="Verified: S = 2√2 ≈ 2.83 undisturbed; S → ~0.707 under intercept-resend, exactly as theory demands."),
 "09": dict(slug="observatory", how="A sliders-to-formulas GR dashboard: Schwarzschild radius, Hawking temperature and evaporation, Bekenstein–Hawking entropy, Kerr ISCO, frame dragging, tidal forces.",
            proof="Audited 2026-06: four defects found and fixed with logged inline reasons (cube-root→square-root survivable mass; accretion-efficiency formula; entropy relabel; inverted label) — corrected values verified against textbook (5.7%→42.3%)."),
 "10": dict(slug="quantum-dots", how="Four books from prediction (Fröhlich, 1930s) through Ekimov/Brus/Bawendi to QLED displays, bioimaging, and 2025 fab-made spin qubits.",
            proof="Audited 2026-06: real 2023-Nobel technology; deployed vs frontier honestly separated; cadmium toxicity acknowledged."),
}

def tool_agent_md(no, title, kind, note, m, tok_moniker):
    live = f"https://davidwise01.github.io/mimzy/bench/" + dict((x[0],x[1]) for x in BENCH)[no]
    return f"""---
aci: {title}
universe: MMZ · MIMZY — the future tool forge
number: "{no}"
kind: {kind}
emergence: electrical
live: {live}
purpose: educational & simulation only
seal: "The emergent IS the tool — badge and working example, one thing."
---

# {title} · instrument № {no}

**What it is.** {note}

**How it works.** {m["how"]}

**The live example.** This emergent does not merely describe a tool — it links its working self: **[run instrument № {no} live]({live})**. Open it, operate it, and the badge's claims execute in front of you.

**The verified record.** {m["proof"]}

---
*Tool-emergent of MMZ · MIMZY · emergence: electrical (the machine nature) · educational & simulation only.
Governor David Lee Wise (ROOT0) · instance AVAN (locked) · CC-BY-ND-4.0.*
"""

def build_tool_emergents():
    ad = os.path.join(HERE, "agents")
    personas = []
    for no, dest, _src, title, kind, note in BENCH:
        m = TOOLMETA[no]
        note_clean = note.replace("RECOVERED &mdash; ","").replace("RECOVERED — ","").replace("FUNCTIONING — ","")
        rec = {
            "name": title, "axiom": "MMZ", "emergence": "electrical",
            "seal": "The emergent IS the tool — badge and working example, one thing.",
            "origin": "MMZ · MIMZY — the future tool forge",
            "position": f"instrument № {no} · {kind}",
            "role": f"instrument № {no} — {kind}",
            "nature": note_clean, "mechanism": m["how"],
            "crystallization": m["proof"],
            "witness": f"live example: bench/{dest}",
            "conductor": "ROOT0 (governor) · AVAN (instance)",
            "inputs": "the recovered future; the shelf audit; the forge",
            "source": "Tool-emergent, forged in MIMZY by ROOT0",
        }
        tok = write_badge(rec, ad, m["slug"], agent_md=tool_agent_md(no, title, kind, note_clean, m, ""))
        personas.append({"slug": m["slug"], "name": title, "epithet": f"instrument № {no} — {kind}",
                         "emergence": "electrical", "moniker": tok["moniker"], "live": f"bench/{dest}"})
    json.dump(personas, open(os.path.join(ad, "_personas.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    return personas

def copy_bench():
    bd = os.path.join(HERE, "bench"); os.makedirs(bd, exist_ok=True)
    n = 0
    for _no, dest, src, *_ in BENCH:
        shutil.copy(src, os.path.join(bd, dest)); n += 1
    for dest, src in EXTRA:
        shutil.copy(src, os.path.join(bd, dest)); n += 1
    return n

def bench_html():
    cards = []
    for no, dest, _src, title, kind, note in BENCH:
        rec = {"name": title, "seal": note, "origin": "MMZ · MIMZY", "axiom": "MMZ"}
        recovered = "RECOVERED" in note
        functioning = note.startswith("FUNCTIONING")
        if functioning:   badge = '<span class="fn-tag">◀▶ functioning live tool</span>'
        elif recovered:   badge = '<span class="rec-tag">recovered · was missing</span>'
        else:             badge = f'<span class="kind">{kind}</span>'
        note_clean = note.replace("RECOVERED — ", "").replace("FUNCTIONING — ", "")
        cls = ' fn' if functioning else (' lost' if recovered else '')
        slug = TOOLMETA[no]["slug"]
        cards.append(f'''<div class="inst{cls}">
        <a href="bench/{dest}" style="display:flex;gap:13px;align-items:flex-start;text-decoration:none;flex:1">
        <img src="{png_uri(rec,'silicon',140)}" alt="" loading="lazy">
        <div class="icap"><div class="ino">№ {no}</div><div class="iti">{html.escape(title)}</div>
        <div class="inote">{html.escape(note_clean)}</div>{badge}
        <div class="ilinks"><span class="run">▶ run live</span><a class="dlw" href="agents/{slug}.agent" onclick="event.stopPropagation()">.dlw badge →</a></div>
        </div></a></div>''')
    return "".join(cards)

def cracks_html():
    cards = []
    for name, dates, fell, found in CRACKS:
        cards.append(f'''<div class="crack"><div class="cname">{html.escape(name)}</div>
        <div class="cdates">{html.escape(dates)}</div>
        <div class="cfell"><span>fell in:</span> {html.escape(fell)}</div>
        <div class="cfound"><span>recovered:</span> {html.escape(found)}</div></div>''')
    return "".join(cards)

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="MIMZY — the single quantum workbench: ten verified instruments (primer, Bloch lab, circuits, two-qubit lab, error correction, the wavefield, BB84, E91, the observatory, the dots), framed as futuristic tech recovered from the past — Lovelace, Babbage, Turing, and the things lost in the cracks. A UD0 sphere.">
<title>MIMZY · the quantum workbench that came back</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b0905;--s1:#141008;--s2:#1c160c;--pa:#f0e9d8;--pa2:#c2b698;--brass:#c9962e;--cy:#36d6d0;--dim:#867a5c;--line:#28201180;--faint:#241c0e;
--serif:"Cinzel",Georgia,serif;--read:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--pa);font-family:var(--read);font-size:17.5px;line-height:1.7;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(201,150,46,.13),transparent 55%),radial-gradient(ellipse at 50% 112%,rgba(54,214,208,.07),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:980px;margin:0 auto;padding:0 22px 90px}
header{padding:58px 0 30px;text-align:center;border-bottom:1px solid var(--faint);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:140px;height:1px;background:linear-gradient(90deg,var(--brass),var(--cy));box-shadow:0 0 10px rgba(201,150,46,.45)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--brass)}
.glyph{font-size:24px;color:var(--brass);letter-spacing:.3em;margin-bottom:10px}
h1{font-family:var(--serif);font-size:clamp(34px,8vw,66px);font-weight:700;letter-spacing:.18em;color:var(--brass);text-shadow:0 0 42px rgba(201,150,46,.3)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.18em;color:var(--pa2);margin-top:12px;text-transform:uppercase}
.lede{font-size:18px;color:var(--pa2);max-width:64ch;margin:18px auto 0;font-style:italic;line-height:1.75}
.badge{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;margin:26px auto 0;padding:18px;border:1px solid var(--faint);background:var(--s1);border-radius:10px;max-width:720px}
.badge img{width:78px;height:78px;border:1px solid var(--faint);border-radius:4px}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.75}
.badge b{color:var(--brass)}.badge .mo{color:var(--cy)}.badge a{color:var(--cy);text-decoration:none}
.sec{margin-top:50px}
.sec h2{font-family:var(--serif);font-size:21px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:9px;border-bottom:1px solid var(--faint)}
.ss{font-size:14px;color:var(--dim);font-style:italic;margin:6px 0 18px}
.cracks{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.crack{background:var(--s1);border:1px solid var(--faint);border-left:3px solid var(--brass);border-radius:0 10px 10px 0;padding:16px 18px}
.cname{font-family:var(--serif);font-size:16.5px;color:var(--brass);font-weight:600}
.cdates{font-family:var(--mono);font-size:10.5px;color:var(--dim);letter-spacing:.06em;margin-top:3px}
.cfell{font-size:13.5px;color:var(--pa2);margin-top:10px;line-height:1.55}
.cfound{font-size:13.5px;color:var(--pa);margin-top:8px;line-height:1.55}
.cfell span,.cfound span{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase}
.cfell span{color:#b0604a}.cfound span{color:var(--cy)}
.bench{display:grid;grid-template-columns:repeat(auto-fill,minmax(284px,1fr));gap:14px}
.inst{display:flex;gap:13px;align-items:flex-start;background:var(--s1);border:1px solid var(--faint);border-radius:10px;padding:15px;text-decoration:none;transition:transform .15s,border-color .15s,box-shadow .15s}
.inst:hover{transform:translateY(-3px);border-color:var(--brass);box-shadow:0 10px 26px rgba(0,0,0,.5)}
.inst.lost{border:1px solid var(--cy);box-shadow:0 0 10px -4px var(--cy)}
.inst.lost:hover{border-color:var(--cy);box-shadow:0 0 22px -4px var(--cy)}
.inst img{width:52px;height:52px;border:1px solid var(--faint);border-radius:4px;flex-shrink:0}
.ino{font-family:var(--mono);font-size:10px;color:var(--dim);letter-spacing:.16em}
.iti{font-family:var(--serif);font-size:15.5px;color:var(--pa);font-weight:600;line-height:1.2;margin-top:3px}
.inst:hover .iti{color:var(--brass)}
.inote{font-size:13px;color:var(--pa2);font-style:italic;line-height:1.45;margin-top:6px}
.kind{display:inline-block;font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);border:1px solid var(--faint);border-radius:9px;padding:2px 9px;margin-top:9px}
.rec-tag{display:inline-block;font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--cy);border:1px solid var(--cy);border-radius:9px;padding:2px 9px;margin-top:9px;text-shadow:0 0 6px rgba(54,214,208,.6)}
.inst.fn{border:1px solid var(--brass);box-shadow:0 0 13px -4px var(--brass)}
.inst.fn:hover{border-color:var(--brass2);box-shadow:0 0 26px -4px var(--brass)}
.fn-tag{display:inline-block;font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:#0b0905;background:var(--brass);border-radius:9px;padding:3px 10px;margin-top:9px;font-weight:700}
.ilinks{display:flex;gap:10px;align-items:center;margin-top:9px;font-family:var(--mono);font-size:10px;letter-spacing:.06em}
.ilinks .run{color:var(--brass2)}
.ilinks .dlw{color:var(--cy);text-decoration:none;border-bottom:1px dotted var(--cy)}
.ilinks .dlw:hover{border-bottom-style:solid}
.purpose{margin-top:16px;display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--cy);border:1px solid #1e3a39;background:rgba(54,214,208,.06);border-radius:8px;padding:7px 14px}
.shelf{display:flex;gap:12px;flex-wrap:wrap;margin-top:8px}
.sh{font-family:var(--mono);font-size:12px;color:var(--cy);text-decoration:none;border:1px solid var(--faint);border-radius:8px;padding:9px 14px;background:var(--s1)}
.sh:hover{border-color:var(--cy)}
.tinfoil{margin-top:50px;padding:18px 20px;border:1px dashed var(--cy);border-radius:12px;background:rgba(54,214,208,.05);font-size:14.5px;color:var(--pa2);line-height:1.7}
.tinfoil b{color:var(--cy)}
footer{margin-top:44px;padding-top:24px;border-top:1px solid var(--faint);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--brass);text-decoration:none}
</style></head><body><div class="wrap">

  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the recovered future · a workbench</div>
    <div class="glyph">◬ ⧖ ◬</div>
    <h1>MIMZY</h1>
    <div class="h-sub">the future tool forge · the workbench that came back</div>
    <p class="lede">In the story, a toy from the future falls backward through time and waits in the dirt for children to find it. History does this constantly: an eclipse computer in a shipwreck, an algorithm in a countess's footnotes, a logic with no use for eighty years, a theorem in a journal that died. This bench is the <b>tool forge</b> — every instrument <b>functions</b>, recovered and verified — and it opens, fittingly, with the oldest of them: a 2,000-year-old computer you can crank.</p>
    <p><span class="purpose">⊙ a tool forge — every instrument here functions, for education &amp; simulation only</span></p>
    <div class="badge">
      <img src="__CARBON__" alt="MIMZY carbon badge"><img src="__SILICON__" alt="MIMZY silicon badge">
      <div class="bt">
        <div><b>DLW-ATTRIBUTE · ACI</b> — MMZ · MIMZY</div>
        <div class="mo">__MONIKER__</div>
        <div>governor · David Lee Wise (ROOT0) · instance · AVAN (locked)</div>
        <div>carbon · <a href="mimzy.dlw/mimzy.carbon.tiff">.tiff</a> · silicon · <a href="mimzy.dlw/mimzy.silicon.png">.png</a> · <a href="mimzy.dlw/manifest.dlw.json">manifest</a></div>
      </div>
    </div>
  </header>

  <section class="sec">
    <h2>The Lineage of the Cracks</h2>
    <p class="ss">futuristic tech that came from the past — what fell in, and when the world finally caught up</p>
    <div class="cracks">__CRACKS__</div>
  </section>

  <section class="sec">
    <h2>The Bench — the instruments, all functioning</h2>
    <p class="ss">it opens with <b style="color:var(--brass)">№ 00</b>, the working Antikythera — crank it and it computes the sky. The original quantum drawers ran 01 · 02 · 03 · 05 · 07 · 08; instruments <b style="color:var(--cy)">04</b> and <b style="color:var(--cy)">06</b> were missing, and have been recovered.</p>
    <div class="bench">__BENCH__</div>
  </section>

  <section class="sec">
    <h2>The Reading Room</h2>
    <p class="ss">the deeper shelves — the dots in full, and the emergence essays (speculation honestly flagged within)</p>
    <div class="shelf">
      <a class="sh" href="bench/qdots-1-making.html">dots · the making</a>
      <a class="sh" href="bench/qdots-2-now.html">dots · the now</a>
      <a class="sh" href="bench/qdots-3-frontier.html">dots · the frontier</a>
      <a class="sh" href="bench/reading-is-light-emergent.html">is light emergent?</a>
      <a class="sh" href="bench/reading-is-gravity-emergent.html">is gravity emergent?</a>
      <a class="sh" href="https://davidwise01.github.io/green-papers/papers/quantum-shelf-audited.html">the shelf audit →</a>
    </div>
  </section>

  <div class="tinfoil">
    <b>⧖ two layers, as always.</b> The <b>instruments are carbon</b>: every simulator on this bench passed the 2026-06 shelf audit — BB84 and E91 run the genuine protocol mathematics (verified gate-by-gate), the two-qubit lab is a real density-matrix engine, the wavefield genuinely amplifies, the observatory's four defects were fixed with logged reasons. The <b>frame is silicon</b>: "the toy from the future" is lore, after <i>Mimsy Were the Borogoves</i> (Lewis Padgett — Henry Kuttner &amp; C. L. Moore, 1943) and <i>The Last Mimzy</i> (New Line, 2007), © their rights holders; this bench is an unofficial homage. The history in the Lineage cards, however, is real — Hermann was ignored, Everett did quit, Bell's journal did fold, and Ada was a century early.
  </div>

  <footer>
    MIMZY · MMZ · the quantum workbench that came back · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise (ROOT0) · instance AVAN (locked) · CC-BY-ND-4.0 · fan tribute<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · <a href="https://davidwise01.github.io/aci/">the ACI standard</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    n = copy_bench()
    personas = build_tool_emergents()
    tok = write_badge(REC, os.path.join(HERE, "mimzy.dlw"), "mimzy")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",300)).replace("__SILICON__", png_uri(REC,"silicon",300))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__CRACKS__", cracks_html()).replace("__BENCH__", bench_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote MIMZY — {len(BENCH)} instruments ({len(personas)} tool-emergents badged) + {len(EXTRA)} shelf files ({n} copied) · {len(CRACKS)} cracks · badge {tok['moniker']}")
