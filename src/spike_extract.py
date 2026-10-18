"""SPIKE (#3): rule-based reading of drawing-set text from the Library db. Never merges.

Run: python src/spike_extract.py   (LIBRARY_DB env var points at library.db; outputs go to data/spike3/, git-ignored)
"""
import collections
import json
import os
import re
import sqlite3
from pathlib import Path

DB = os.environ.get("LIBRARY_DB", "")
COLLECTION = "3 - Proj Lib/2 - Drawings and Specs/Bridges/MTO Database/"
INDEX = COLLECTION + "Project Drawings Database - Ontario.xlsx"
OUT = Path(__file__).resolve().parents[1] / "data" / "spike3"

# ---- basics: (label, pattern) scored by hit count -------------------------------------------
TYPE_PATTERNS = {
    "Precast I Girder": r"PRESTRESSED\s+(?:CONCRETE\s+)?GIRDERS?|PRECAST\s+GIRDERS?|C\.?P\.?C\.?I|NU\s?\d{4}|NU\s+GIRDER|PRECAST\s+(?:PRESTRESSED\s+)?(?:CONCRETE\s+)?(?:I[- ])?GIRDER|AASHTO",
    "Precast Box Girder": r"(?:PRECAST|PRESTRESSED)\s+(?:CONCRETE\s+)?BOX\s+(?:GIRDER|BEAM)|BOX\s+BEAM",
    "Steel Box Girder": r"STEEL\s+BOX\s+GIRDER|TUB\s+GIRDER|BOX\s+GIRDER\s+(?:WEB|FLANGE)",
    "Steel I Girder": r"STEEL\s+(?:PLATE\s+)?GIRDER|PLATE\s+GIRDER|\bWWF\s?\d|\bW\d{3,4}\s?X\s?\d",
    "Post-Tensioned": r"POST[- ]?TENSION|\bTENDONS?\b|STRESSING\s+SEQUENCE",
    "Rigid Frame": r"RIGID\s+FRAME",
    "Steel Truss": r"\bTRUSS\b",
    "Steel Arch": r"\bARCH\s+(?:RIB|SPAN)",
}
FOUNDATION_PATTERNS = {
    "steel piles": r"\bPILES?\b|\bH[- ]?PILES?\b|\bHP\s?\d{3}|STEEL\s+(?:H\s+)?PILES?|PIPE\s+PILES?|TUBE\s+PILES?",
    "spread footings": r"SPREAD\s+FOOTINGS?|FOOTINGS?\s+(?:ON|TO)\s+(?:BED)?ROCK|BEARING\s+ON\s+(?:BED)?ROCK|FOUNDED\s+ON|\bFOOTINGS?\b",
    "caisson": r"CAISSONS?",
}
ABUT_PATTERNS = {
    "semi-integral": r"SEMI[- ]?INTEGRAL",
    "integral": r"(?<!SEMI[- ])(?<!SEMI)INTEGRAL\s+ABUTMENT",
}
CROSSING_PATTERNS = {
    "underpass": r"UNDERPASS",
    "overpass": r"OVERPASS",
    "overhead": r"OVERHEAD|\bC\.?P\.?R\b|\bC\.?N\.?R\b|RAILWAY",
    "water": r"\bCREEK\b|\bRIVER\b|HIGH\s+WATER|\bH\.?W\.?L\b|SCOUR",
    "pedestrian": r"PEDESTRIAN\s+BRIDGE",
}
STAGED = r"\bSTAGE\s*(?:2|II|TWO)\b|CONSTRUCTION\s+STAGING"

# ---- feature tags: tag -> trigger phrases (first vocabulary, grouped) -------------------------
TAGS = {
    "in-water": {
        "cofferdam": r"COFFER\s?DAM", "dewatering": r"DE-?WATERING", "turbidity curtain": r"TURBIDITY\s+(?:CURTAIN|BARRIER)",
        "tremie": r"TREMIE", "underwater work": r"UNDERWATER|\bDIVERS?\b", "scour protection": r"RIP[- ]?RAP|ARMOU?R\s+STONE|SCOUR\s+PROTECTION|GABIONS?",
        "temporary bridge/detour": r"TEMPORARY\s+(?:BRIDGE|MODULAR\s+BRIDGE)|DETOUR\s+(?:BRIDGE|STRUCTURE)",
        "falsework/shoring": r"FALSEWORK|TEMPORARY\s+SHORING|ROADWAY\s+PROTECTION",
    },
    "protection": {
        "containment system": r"CONTAINMENT\s+SYSTEM|ENCAPSULATION", "protection system": r"PROTECTION\s+SYSTEM",
        "temporary barrier/staging": r"TEMPORARY\s+(?:PRECAST\s+)?CONCRETE\s+BARRIER", "erosion control": r"SILT\s+FENCE|EROSION\s+(?:AND\s+SEDIMENT\s+)?CONTROL",
    },
    "foundations": {
        "rock anchor": r"ROCK\s+ANCHORS?", "soil anchor": r"SOIL\s+ANCHORS?|GROUND\s+ANCHORS?|TIE-?BACKS?", "deadman anchor": r"DEAD\s?MAN",
        "micropile": r"MICRO-?\s?PILES?", "helical pile": r"HELICAL\s+PILES?|SCREW\s+PILES?", "caisson": r"CAISSONS?",
        "foundation widening": r"FOOTING\s+(?:WIDENING|EXTENSION)|WIDEN(?:ED|ING)?\s+FOOTING", "underpinning": r"UNDERPINNING",
        "sheet piling": r"SHEET\s+PIL(?:E|ES|ING)", "jet grouting": r"JET\s+GROUT", "MSE wall": r"\bMSE\b|MECHANICALLY\s+STABILIZED",
        "approach slab": r"APPROACH\s+SLAB",
    },
    "substructure": {
        "refacing": r"REFAC(?:E|ING)", "jacketing": r"JACKET(?:ING)?", "pier cap replacement": r"(?:NEW|REPLACE\w*)\s+PIER\s+CAP",
        "crash wall": r"CRASH\s+WALL", "integral conversion": r"CONVERSION\s+TO\s+(?:SEMI-?)?INTEGRAL|(?:SEMI-?)?INTEGRAL\s+CONVERSION",
        "ballast wall": r"BALLAST\s+WALL", "cathodic protection": r"CATHODIC|GALVANIC\s+ANODES?", "crack injection": r"CRACK\s+INJECTION|EPOXY\s+INJECTION",
    },
    "concrete superstructure": {
        "deck replacement": r"DECK\s+REPLACEMENT|REMOVE\s+(?:EXISTING\s+)?DECK|NEW\s+DECK", "deck repairs": r"(?:PARTIAL|FULL)\s+DEPTH\s+(?:DECK\s+)?REPAIR|DECK\s+REPAIRS?",
        "concrete overlay": r"(?:CONCRETE|LATEX|SILICA\s+FUME|UHPC)\s+OVERLAY|\bUHPC\b", "girder addition": r"(?:NEW|ADDITIONAL)\s+GIRDERS?|GIRDER\s+ADDITION",
        "widening": r"WIDENING", "CFRP": r"\bC?FRP\b|CARBON\s+FIB(?:RE|ER)", "external post-tensioning": r"EXTERNAL\s+(?:POST-?TENSION|PRESTRESS)",
        "precast deck panels": r"PRECAST\s+DECK\s+PANELS?|FULL[- ]DEPTH\s+PRECAST",
    },
    "steel": {
        "steel repairs": r"STRUCTURAL\s+STEEL\s+REPAIRS?|SECTION\s+LOSS|REPAIR\s+PLATES?", "fatigue retrofit": r"FATIGUE|CRACK\s+ARREST|DRILL(?:ED)?\s+HOLES?\s+AT\s+CRACK",
        "pin and hanger": r"PIN\s+AND\s+HANGER|HANGER\s+PLATE", "recoating": r"COATING\s+(?:SYSTEM|REMOVAL)|RECOAT|BLAST\s+CLEAN|METALLIZ", "heat straightening": r"HEAT\s+STRAIGHTEN",
        "bolted splice": r"BOLTED\s+SPLICE|FIELD\s+SPLICE",
    },
    "bearings and joints": {
        "bearing replacement": r"(?:REPLACE\w*|NEW)\s+BEARINGS?|BEARING\s+REPLACEMENT", "jacking": r"\bJACKING\b|JACK(?:ING)?\s+(?:POINTS?|BRACKETS?|SEQUENCE)",
        "expansion joint replacement": r"(?:REPLACE\w*|NEW|INSTALL\s+NEW)\s+(?:EXPANSION\s+)?JOINT|JOINT\s+REPLACEMENT|STRIP\s+SEAL", "modular joint": r"MODULAR\s+(?:EXPANSION\s+)?JOINT",
        "finger joint": r"FINGER\s+JOINT", "joint elimination": r"(?:ELIMINAT\w*|REMOV\w*)\s+(?:THE\s+)?(?:EXPANSION\s+)?JOINTS?\s+(?:AT|OVER)|LINK\s+SLAB",
    },
    "barriers and deck surface": {
        "barrier/parapet replacement": r"(?:NEW|REPLACE\w*|CONSTRUCT\s+NEW)\s+(?:CONCRETE\s+)?(?:PARAPET|BARRIER)\s+WALL|PARAPET\s+WALL\s+REPLACEMENT", "railing": r"RAILING",
        "waterproofing": r"WATERPROOFING", "drainage": r"DECK\s+DRAINS?|SCUPPERS?|DOWNSPOUTS?", "lighting/utilities": r"LIGHT\s+STANDARDS?|UTILIT(?:Y|IES)\s+(?:SUPPORT|DUCT)|WATERMAIN|\bDUCTS?\b",
        "slope paving": r"SLOPE\s+PAVING",
    },
    "special conditions": {
        "accelerated construction": r"SLIDE[- ]IN|\bSPMT\b|ACCELERATED\s+BRIDGE", "seismic": r"SEISMIC\s+(?:RESTRAINER|RETROFIT)|RESTRAINERS?|SHEAR\s+KEYS?",
        "heritage": r"HERITAGE", "monitoring": r"VIBRATION\s+MONITOR|MONITORING\s+PROGRAM|STRAIN\s+GAUGE", "railway work": r"RAILWAY|\bCPR\b|\bCNR\b|METROLINX",
        "fish/species window": r"FISH\s+(?:HABITAT|WINDOW|RESCUE)|IN-?WATER\s+WORK\s+(?:TIMING|WINDOW|RESTRICTION)",
    },
}
STANDARD_PAGE = re.compile(r"STANDARD\s+DETAILS|\bSS\d{2}-|STANDARD\s+DRAWING|OPSD|\bSTANDARD\b", re.I)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def load_index(con):
    doc = con.execute("SELECT doc_id FROM documents WHERE canonical_path=?", (INDEX,)).fetchone()[0]
    out = {}
    for page, text in con.execute("SELECT page,text FROM pages WHERE doc_id=? AND page<=2", (doc,)):
        lines = text.split("\n")
        sheet = lines[0]
        head = [h.split(" (")[0].strip() for h in lines[1].split("\t")]
        for line in lines[2:]:
            row = dict(zip(head, (c.strip() for c in line.split("\t"))))
            name = row.get("Filename", "").upper().removesuffix(".PDF")
            if name:
                row["_sheet"] = "new" if "New" in sheet else "rehab"
                out[name] = row
    return out


def pick(scores: dict, default=""):
    best = max(scores.items(), key=lambda kv: kv[1], default=(default, 0))
    return best[0] if best[1] > 0 else default


def extract(pages):
    full = "\n".join(t for _, t in pages).upper()
    count = lambda pat: len(re.findall(pat, full))
    rec = {}
    ts = {k: count(p) for k, p in TYPE_PATTERNS.items()}
    if ts["Post-Tensioned"] and ts["Precast I Girder"] > ts["Post-Tensioned"]:
        ts["Post-Tensioned"] = 0  # pretensioned girders mention tendons in notes
    if ts["Steel Box Girder"] and ts["Steel I Girder"]:
        ts["Steel Box Girder"] *= 3  # box girder sets also mention plates and splices
    rec["type"] = pick(ts)
    ga = "\n".join(t for _, t in pages[:2]).upper()  # general arrangement comes first
    short = {"NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W", "CENTER": "C", "CENTRE": "C"}
    labels = {short.get(l, l) for l in re.findall(r"\b(N|S|E|W|NORTH|SOUTH|EAST|WEST|CENTRE|CENTER)\.?\s+PIER\b", ga)}
    numbered = {n for n in re.findall(r"\bPIER\s*(?:NO\.?\s*)?(\d{1,2})\b", ga) if 0 < int(n) < 15}
    rec["spans"] = (len(numbered) if numbered else len(labels)) + 1
    dims = [int(v) for v in re.findall(r"(?<![\d.])(\d{4,5})\+?(?![\d.])", ga)]
    rep = sorted({d for d, k in collections.Counter(d for d in dims if 6000 <= d <= 90000).items() if k >= 2}, reverse=True)
    if rec["spans"] == 1:
        rec["max_span"] = round(rep[0] / 1000, 1) if rep else None
    else:  # the largest repeated dimension is usually the total length
        rec["max_span"] = round(rep[1] / 1000, 1) if len(rep) > 1 else None
    fs = {k: count(p) for k, p in FOUNDATION_PATTERNS.items()}
    if fs["caisson"] >= 2:
        rec["foundation"] = "caisson"
    elif fs["steel piles"] >= 2 * max(fs["spread footings"], 1):
        rec["foundation"] = "steel piles"
    elif fs["spread footings"]:
        rec["foundation"] = "spread footings"
    else:
        rec["foundation"] = pick(fs, "unknown")
    ab = {k: (v if v >= 3 else 0) for k, v in ((k, count(p)) for k, p in ABUT_PATTERNS.items())}
    rec["abutment"] = "rigid frame" if rec["type"] == "Rigid Frame" else pick(ab, "traditional")
    rec["staged"] = "yes" if count(STAGED) else "no"
    cs = {k: count(p) for k, p in CROSSING_PATTERNS.items()}
    rec["crossing"] = pick(cs)
    tags = {}
    for group, items in TAGS.items():
        for tag, pat in items.items():
            job, std = [], []
            for page, text in pages:
                if re.search(pat, text, re.I):
                    (std if STANDARD_PAGE.search(text[:400] + text[-600:]) else job).append(page)
            if job or std:
                tags[tag] = {"group": group, "job_pages": job, "std_pages": std}
    rec["tags"] = tags
    return rec


TYPE_ALIASES = {"prestressed": "precast i girder", "precast u girder": "precast box girder"}


def agree(field, got, want):
    want = norm(want)
    if not want or want in ("unknown", "n/a", "combination") and field != "foundation":
        return None
    if field == "max_span":
        try:
            return got is not None and abs(float(got) - float(want)) <= 1.0
        except ValueError:
            return None
    if field == "spans":
        return str(got) == want
    if field == "type":
        want = TYPE_ALIASES.get(want, want)
    if field == "crossing" and want == "subway":
        want = "underpass"
    return norm(str(got)) == want


FIELDS = {"type": "Type", "spans": "Number of Spans", "max_span": "Max. Span Length", "foundation": "Foundation",
          "abutment": "Abutment", "staged": "Staged?", "crossing": "Crossing Type"}


def main():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    index = load_index(con)
    docs = con.execute(
        "SELECT doc_id, canonical_path FROM documents WHERE held_out=0 AND ext='.pdf' AND canonical_path LIKE ?",
        (COLLECTION + "%",)).fetchall()
    OUT.mkdir(parents=True, exist_ok=True)
    tally = collections.defaultdict(lambda: [0, 0])
    misses = collections.defaultdict(collections.Counter)
    n = 0
    with open(OUT / "records.jsonl", "w", encoding="utf-8") as fh:
        for doc_id, path in docs:
            name = Path(path).stem.upper()
            pages = con.execute("SELECT page,text FROM pages WHERE doc_id=? ORDER BY page", (doc_id,)).fetchall()
            rec = extract(pages)
            rec.update(doc_id=doc_id, name=name, pages=len(pages))
            row = index.get(name)
            if row:
                n += 1
                rec["index"] = {f: row.get(c, "") for f, c in FIELDS.items()}
                rec["index"]["sheet"] = row["_sheet"]
                for f, c in FIELDS.items():
                    ok = agree(f, rec[f], row.get(c, ""))
                    if ok is None:
                        continue
                    tally[f][0] += ok
                    tally[f][1] += 1
                    if not ok:
                        misses[f][(norm(row.get(c, "")), norm(str(rec[f])))] += 1
            fh.write(json.dumps(rec) + "\n")
    lines = [f"sets read: {len(docs)} · matched to index: {n}", "", "| field | agree | scored | % |", "|---|---|---|---|"]
    tot = [0, 0]
    for f in FIELDS:
        a, b = tally[f]
        tot[0] += a; tot[1] += b
        lines.append(f"| {f} | {a} | {b} | {100*a/max(b,1):.0f} |")
    lines.append(f"| **all** | {tot[0]} | {tot[1]} | {100*tot[0]/max(tot[1],1):.0f} |")
    lines.append(f"\nmean of field %: {sum(100*a/max(b,1) for a,b in tally.values())/len(tally):.0f}")
    lines.append("\n## top disagreements (index -> extracted)")
    for f in FIELDS:
        lines.append(f"- {f}: " + "; ".join(f"{w}->{g} x{k}" for (w, g), k in misses[f].most_common(6)))
    (OUT / "score.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
