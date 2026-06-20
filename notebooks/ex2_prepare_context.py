"""Exercise 2 step 1: conceptual scaling of the wine dataset.

Loads data/winequality-red.csv, draws a 200-row sample stratified by
quality tier, applies the scale definitions from the attribute inventory
(see report/ex2_toscana.md section 2), and writes:
  - data/wine_sample_200.csv  (raw sampled rows, for traceability)
  - data/wine_toscana.sql     (derived binary context as HSQLDB INSERTs)

Run with: .venv/bin/python3 notebooks/ex2_prepare_context.py
"""
import pandas as pd

DATA_PATH = "data/winequality-red.csv"
SAMPLE_PATH = "data/wine_sample_200.csv"
SQL_PATH = "data/wine_toscana.sql"
SAMPLE_SIZE = 200
RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH, sep=";")
    df.columns = [c.strip() for c in df.columns]
    return df


def quality_tier(q):
    if q <= 4:
        return "Low"
    if q <= 6:
        return "Medium"
    return "High"


def stratified_sample(df, n=SAMPLE_SIZE):
    df = df.copy()
    df["quality_tier"] = df["quality"].apply(quality_tier)
    frac = n / len(df)
    sample = (
        df.groupby("quality_tier", group_keys=False)
        .apply(lambda g: g.sample(frac=frac, random_state=RANDOM_STATE))
        .reset_index(drop=True)
    )
    # trim/pad to exactly n rows if rounding overshoots/undershoots
    if len(sample) > n:
        sample = sample.sample(n=n, random_state=RANDOM_STATE).reset_index(drop=True)
    if "quality_tier" not in sample.columns:
        sample["quality_tier"] = sample["quality"].apply(quality_tier)
    sample.insert(0, "wine_id", range(1, len(sample) + 1))
    return sample


# --- scale definitions ------------------------------------------------------
# Each function maps a raw value to the set of derived (ordinal/dichotomic/
# interordinal) attributes it satisfies, per the attribute inventory
# described in report/ex2_toscana.md section 2.

def scale_fixed_acidity(v):
    out = []
    if v >= 6:
        out.append("fixed_acidity>=low(6)")
    if v >= 8:
        out.append("fixed_acidity>=medium(8)")
    if v >= 10:
        out.append("fixed_acidity>=high(10)")
    return out


def scale_volatile_acidity(v):
    out = []
    if v >= 0.3:
        out.append("volatile_acidity>=low(0.3)")
    if v >= 0.5:
        out.append("volatile_acidity>=medium(0.5)")
    if v >= 0.7:
        out.append("volatile_acidity>=high(0.7)")
    return out


def scale_citric_acid(v):
    return ["citric_acid_present"] if v >= 0.25 else ["citric_acid_absent"]


def scale_residual_sugar(v):
    # dry < 4, off-dry 4-12, sweet > 12 (g/L) — wine industry convention
    if v < 4:
        return ["residual_sugar=dry"]
    if v <= 12:
        return ["residual_sugar=off_dry"]
    return ["residual_sugar=sweet"]


def scale_chlorides(v):
    return ["chlorides=high_salt"] if v >= 0.08 else ["chlorides=low_salt"]


def scale_free_so2(v):
    out = []
    if v >= 6:
        out.append("free_so2>=low(6)")
    if v >= 15:
        out.append("free_so2>=medium(15)")
    if v >= 30:
        out.append("free_so2>=high(30)")
    return out


def scale_total_so2(v):
    out = []
    if v >= 20:
        out.append("total_so2>=low(20)")
    if v >= 60:
        out.append("total_so2>=medium(60)")
    if v >= 100:
        out.append("total_so2>=high(100)")
    return out


def scale_density(v):
    return ["density=light"] if v < 0.997 else ["density=heavy"]


def scale_pH(v):
    # interordinal: acidic side and basic side, both increasing-include-bounds
    out = []
    if v <= 3.1:
        out.append("pH<=acidic(3.1)")
    if 3.1 < v < 3.4:
        out.append("pH=neutral_range")
    if v >= 3.4:
        out.append("pH>=basic(3.4)")
    return out


def scale_sulphates(v):
    out = []
    if v >= 0.4:
        out.append("sulphates>=low(0.4)")
    if v >= 0.6:
        out.append("sulphates>=medium(0.6)")
    if v >= 0.8:
        out.append("sulphates>=high(0.8)")
    return out


def scale_alcohol(v):
    out = []
    if v >= 9:
        out.append("alcohol>=9")
    if v >= 11:
        out.append("alcohol>=11")
    if v >= 13:
        out.append("alcohol>=13")
    return out


def scale_quality(v):
    out = []
    if v >= 5:
        out.append("quality>=acceptable(5)")
    if v >= 7:
        out.append("quality>=good(7)")
    if v >= 8:
        out.append("quality>=excellent(8)")
    return out


SCALES = {
    "fixed acidity": scale_fixed_acidity,
    "volatile acidity": scale_volatile_acidity,
    "citric acid": scale_citric_acid,
    "residual sugar": scale_residual_sugar,
    "chlorides": scale_chlorides,
    "free sulfur dioxide": scale_free_so2,
    "total sulfur dioxide": scale_total_so2,
    "density": scale_density,
    "pH": scale_pH,
    "sulphates": scale_sulphates,
    "alcohol": scale_alcohol,
    "quality": scale_quality,
}


def build_derived_context(sample):
    rows = {}
    for _, row in sample.iterrows():
        attrs = []
        for col, scale_fn in SCALES.items():
            attrs.extend(scale_fn(row[col]))
        rows[int(row["wine_id"])] = attrs
    return rows


def verify_scale_closure(derived):
    """Sanity check: ordinal scales must be downward-closed in the bound order
    (e.g. alcohol>=13 present => alcohol>=11 and alcohol>=9 also present)."""
    chains = [
        ["alcohol>=9", "alcohol>=11", "alcohol>=13"],
        ["fixed_acidity>=low(6)", "fixed_acidity>=medium(8)", "fixed_acidity>=high(10)"],
        ["volatile_acidity>=low(0.3)", "volatile_acidity>=medium(0.5)", "volatile_acidity>=high(0.7)"],
        ["free_so2>=low(6)", "free_so2>=medium(15)", "free_so2>=high(30)"],
        ["total_so2>=low(20)", "total_so2>=medium(60)", "total_so2>=high(100)"],
        ["sulphates>=low(0.4)", "sulphates>=medium(0.6)", "sulphates>=high(0.8)"],
        ["quality>=acceptable(5)", "quality>=good(7)", "quality>=excellent(8)"],
    ]
    errors = []
    for wine_id, attrs in derived.items():
        attr_set = set(attrs)
        for chain in chains:
            seen_true = False
            for a in reversed(chain):  # highest bound first
                present = a in attr_set
                if present:
                    seen_true = True
                elif seen_true:
                    errors.append((wine_id, chain, a))
    if errors:
        raise AssertionError(f"Scale closure violated: {errors[:5]} (+{len(errors)-5} more)")
    print(f"Scale closure verified for {len(derived)} wines across {len(chains)} ordinal chains.")


def all_attributes():
    attrs = []
    seen = set()
    for col, fn in SCALES.items():
        # probe a representative spread of values to enumerate possible labels
        for probe in [0, 1, 5, 10, 20, 50, 100, 0.1, 0.3, 0.5, 0.7, 0.9, 3.0, 3.2, 3.5, 9, 11, 13]:
            for a in fn(probe):
                if a not in seen:
                    seen.add(a)
                    attrs.append(a)
    return attrs


def sql_identifier(name):
    return name.replace(" ", "_").replace(">", "ge").replace("<", "le").replace(
        "=", "_").replace("(", "_").replace(")", "_").replace(".", "_").replace("-", "_")


def write_sql(sample, derived, attrs, path=SQL_PATH):
    attr_cols = [sql_identifier(a) for a in attrs]
    with open(path, "w") as f:
        f.write("-- Derived binary context for ToscanaJ/Elba (HSQLDB)\n")
        f.write("-- Generated by notebooks/ex2_prepare_context.py\n\n")
        f.write("DROP TABLE wine_context IF EXISTS;\n\n")
        f.write("CREATE TABLE wine_context (\n")
        f.write("  wine_id INTEGER PRIMARY KEY,\n")
        col_defs = ",\n".join(f"  {c} VARCHAR(1)" for c in attr_cols)
        f.write(col_defs + "\n);\n\n")

        for wine_id, attr_list in derived.items():
            present = set(attr_list)
            values = ["'X'" if a in present else "''" for a in attrs]
            cols = ", ".join(["wine_id"] + attr_cols)
            vals = ", ".join([str(wine_id)] + values)
            f.write(f"INSERT INTO wine_context ({cols}) VALUES ({vals});\n")
    print(f"Wrote {len(derived)} rows x {len(attrs)} attributes to {path}")


RAW_COLUMNS = [
    "fixed acidity", "volatile acidity", "citric acid", "residual sugar",
    "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density",
    "pH", "sulphates", "alcohol", "quality",
]


def write_raw_sql(sample, path=SQL_PATH):
    """Raw many-valued context for Elba: Elba derives the scales itself
    (Ordinal/Interordinal scale dialogs with thresholds), so the SQL must
    carry the original numeric values, not pre-binarized columns."""
    col_map = {c: sql_identifier(c) for c in RAW_COLUMNS}
    with open(path, "w") as f:
        f.write("-- Raw many-valued context for Elba (HSQLDB)\n")
        f.write("-- Generated by notebooks/ex2_prepare_context.py\n")
        f.write("-- Elba builds the conceptual scales from these raw columns.\n\n")
        f.write("DROP TABLE wine_context IF EXISTS;\n\n")
        f.write("CREATE TABLE wine_context (\n")
        f.write("  wine_id INTEGER PRIMARY KEY,\n")
        col_defs = ",\n".join(
            f"  {col_map[c]} {'INTEGER' if c == 'quality' else 'DOUBLE'}" for c in RAW_COLUMNS
        )
        f.write(col_defs + "\n);\n\n")

        cols = ", ".join(["wine_id"] + [col_map[c] for c in RAW_COLUMNS])
        for _, row in sample.iterrows():
            vals = [str(int(row["wine_id"]))] + [str(row[c]) for c in RAW_COLUMNS]
            f.write(f"INSERT INTO wine_context ({cols}) VALUES ({', '.join(vals)});\n")
    print(f"Wrote {len(sample)} rows x {len(RAW_COLUMNS)} raw attributes to {path}")


def main():
    df = load_data()
    sample = stratified_sample(df)
    sample.to_csv(SAMPLE_PATH, index=False)
    print(f"Wrote {len(sample)}-row stratified sample to {SAMPLE_PATH}")
    print(sample["quality_tier"].value_counts(), "\n")

    derived = build_derived_context(sample)
    verify_scale_closure(derived)

    attrs = all_attributes()
    print(f"\nDerived context has {len(attrs)} binary attributes (computed in Python for the implications notebook):")
    for a in attrs:
        print(f"  - {a}")

    write_raw_sql(sample)


if __name__ == "__main__":
    main()
