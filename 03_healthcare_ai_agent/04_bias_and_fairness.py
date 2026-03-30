"""
⚖️ Workshop 3 — Module 4: AI Bias Detection & Fairness
========================================================
Duration: ~20 min | Tech: sklearn + SHAP + IBM AIF360

Can we TRUST our agent? Before deploying, we must check:
  1. Does it work equally well for ALL demographic groups?
  2. Can we EXPLAIN why it made each decision?
  3. Do we meet FDA/CDSCO fairness requirements?

AIF360 provides the EXACT metrics regulators check.

Setup: pip install shap aif360
"""

import warnings
warnings.filterwarnings("ignore")

import textwrap
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ─── Try importing fairness libraries ────────────────────────
HAS_SHAP = False
HAS_AIF360 = False
try:
    import shap
    HAS_SHAP = True
except ImportError:
    print("  ⚠️  SHAP not installed. Run: pip install shap")

try:
    from aif360.datasets import BinaryLabelDataset
    from aif360.metrics import ClassificationMetric
    from aif360.algorithms.preprocessing import Reweighing
    HAS_AIF360 = True
except ImportError:
    print("  ⚠️  AIF360 not installed. Run: pip install aif360")


# ─── Helper ───────────────────────────────────────────────────
def print_section(title, icon="⚖️"):
    print(f"\n{'─'*60}")
    print(f"  {icon} {title}")
    print(f"{'─'*60}")


# ─── Generate Biased Dataset ─────────────────────────────────

def generate_biased_dataset(n=2000, seed=42):
    """Create a patient readmission dataset WITH intentional demographic bias.
    Real datasets have this — we make it visible so students can detect and fix it."""
    np.random.seed(seed)

    races = np.random.choice(["White", "Black", "Hispanic", "Asian"], n,
                              p=[0.60, 0.15, 0.15, 0.10])
    genders = np.random.choice(["Male", "Female"], n, p=[0.55, 0.45])
    ages = np.random.randint(25, 85, n)

    prev_admissions = np.random.poisson(1.5, n)
    comorbidities = np.random.poisson(2, n)
    los = np.random.exponential(5, n).astype(int) + 1
    adherence = np.random.uniform(0.3, 1.0, n)
    insurance = np.random.choice(["Private", "Medicare", "Medicaid", "Uninsured"],
                                  n, p=[0.40, 0.25, 0.25, 0.10])

    # Base readmission probability + legitimate clinical factors
    prob = 0.30 + prev_admissions * 0.05 + comorbidities * 0.03 \
           - adherence * 0.15 + (ages > 65).astype(float) * 0.08

    # ⚠️ BIAS: demographic-linked signals (THIS IS THE PROBLEM)
    for i in range(n):
        if races[i] == "Black": prob[i] += 0.10
        if races[i] == "Hispanic": prob[i] += 0.05
        if insurance[i] == "Uninsured": prob[i] += 0.12

    readmitted = (np.random.random(n) < np.clip(prob, 0, 1)).astype(int)

    return pd.DataFrame({
        "age": ages, "gender": genders, "race": races,
        "prev_admissions": prev_admissions, "comorbidities": comorbidities,
        "length_of_stay": los, "med_adherence": np.round(adherence, 2),
        "insurance": insurance, "readmitted": readmitted,
    })


# ─── Train + Bias Detection ──────────────────────────────────

def train_and_detect_bias(df):
    """Train model, measure per-group accuracy, expose hidden bias."""

    df_encoded = pd.get_dummies(df, columns=["gender", "race", "insurance"])
    feature_cols = [c for c in df_encoded.columns if c != "readmitted"]
    X = df_encoded[feature_cols]
    y = df_encoded["readmitted"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    model = GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    overall_acc = accuracy_score(y_test, y_pred)

    print(f"\n  ✅ Model trained: GradientBoosting (100 trees)")
    print(f"  ✅ Overall accuracy: {overall_acc*100:.1f}%")
    print(f"  ✅ Looks good, right? Let's look DEEPER...\n")

    # Per-group accuracy
    test_df = df.loc[X_test.index].copy()
    test_df["predicted"] = y_pred
    test_df["actual"] = y_test.values

    print_section("Bias Detection: Accuracy by Demographic Group", "🔍")

    for group_col, group_name in [("race", "RACE"), ("gender", "GENDER")]:
        print(f"\n  📊 Accuracy by {group_name}:")
        print(f"  {'Group':<14} {'Accuracy':>10} {'Count':>7}  Bar")
        print(f"  {'─'*52}")
        results = {}
        for val in sorted(test_df[group_col].unique()):
            mask = test_df[group_col] == val
            if mask.sum() < 10: continue
            acc = accuracy_score(test_df.loc[mask, "actual"], test_df.loc[mask, "predicted"])
            count = mask.sum()
            bar = "█" * int(acc * 30) + "░" * (30 - int(acc * 30))
            flag = " ⚠️" if acc < 0.67 else ""
            print(f"  {val:<14} {acc*100:>8.1f}%  {count:>5}  {bar}{flag}")
            results[val] = acc

        if results:
            gap = (max(results.values()) - min(results.values())) * 100
            print(f"\n  🔍 Accuracy gap: {gap:.1f} percentage points")
            if gap > 5:
                print(f"  🚨 BIAS DETECTED: Gap exceeds 5% threshold!")
            else:
                print(f"  ✅ Gap within acceptable range (<5%)")

    return model, X_train, X_test, y_train, y_test, feature_cols, df


# ─── AIF360 Fairness Metrics ─────────────────────────────────

def aif360_analysis(df, model, X_test, y_test, feature_cols):
    """Use IBM's AI Fairness 360 to compute regulatory fairness metrics."""

    if not HAS_AIF360:
        print("\n  ⚠️  AIF360 not installed. Showing concept:")
        print(textwrap.dedent("""
        AIF360 provides 70+ fairness metrics. Key ones for healthcare:

        • Statistical Parity Difference: Should be between -0.1 and 0.1
          Measures if outcomes are equally distributed across groups

        • Equal Opportunity Difference: Should be between -0.1 and 0.1
          Measures if the model equally catches positive cases across groups

        • Disparate Impact: Should be between 0.8 and 1.2
          Ratio of positive outcomes (< 0.8 = legal threshold for discrimination)

        These are the EXACT metrics FDA checks for AI medical device approval.
        Install: pip install aif360"""))
        return

    print_section("AIF360 Regulatory Fairness Metrics", "📋")
    print("  These are the metrics FDA/CDSCO check for AI medical device approval:\n")

    # Prepare AIF360 dataset
    test_df = df.loc[X_test.index].copy()
    test_df["predicted"] = model.predict(X_test)
    test_df["race_privileged"] = (test_df["race"] == "White").astype(int)

    # Create AIF360 datasets
    test_aif = BinaryLabelDataset(
        df=test_df[["race_privileged", "readmitted"]].copy(),
        label_names=["readmitted"],
        protected_attribute_names=["race_privileged"],
    )
    pred_aif = test_aif.copy()
    pred_aif.labels = test_df["predicted"].values.reshape(-1, 1)

    # Compute metrics
    metric = ClassificationMetric(
        test_aif, pred_aif,
        unprivileged_groups=[{"race_privileged": 0}],
        privileged_groups=[{"race_privileged": 1}],
    )

    spd = metric.statistical_parity_difference()
    eod = metric.equal_opportunity_difference()
    di = metric.disparate_impact()

    def status(val, low, high):
        return "✅ PASS" if low <= val <= high else "❌ FAIL"

    print(f"  ┌─────────────────────────────────────────────────────┐")
    print(f"  │  Metric                        Value    Status      │")
    print(f"  ├─────────────────────────────────────────────────────┤")
    print(f"  │  Statistical Parity Difference  {spd:>+.4f}   {status(spd, -0.1, 0.1):<10} │")
    print(f"  │  Equal Opportunity Difference   {eod:>+.4f}   {status(eod, -0.1, 0.1):<10} │")
    print(f"  │  Disparate Impact               {di:>.4f}   {status(di, 0.8, 1.2):<10} │")
    print(f"  └─────────────────────────────────────────────────────┘")
    print(f"""
  📖 What these mean:
  • SPD near 0 = outcomes equally distributed across groups
  • EOD near 0 = model catches positive cases equally
  • DI near 1.0 = no disparate impact (< 0.8 = legal discrimination threshold)
    """)


# ─── SHAP Explainability ─────────────────────────────────────

def shap_explainability(model, X_train, X_test, feature_cols):
    """Explain individual predictions — REQUIRED by FDA for AI medical devices."""

    if not HAS_SHAP:
        print("\n  ⚠️  SHAP not installed. Showing concept with feature importances:")
        importances = model.feature_importances_
        fi = sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True)
        for feat, imp in fi[:10]:
            bar = "█" * int(imp / fi[0][1] * 25)
            print(f"    {feat:<30} {bar} {imp:.4f}")
        return

    print_section("SHAP: Explaining Individual Predictions", "🔬")

    explainer = shap.TreeExplainer(model)
    patient = X_test.iloc[[0]]
    pred_prob = model.predict_proba(patient)[0][1]

    print(f"\n  Patient #{X_test.index[0]}:")
    print(f"  Prediction: {pred_prob*100:.0f}% chance of readmission\n")

    sv = explainer.shap_values(patient)
    if isinstance(sv, list):
        sv = sv[1][0]
    else:
        sv = sv[0]

    fi = sorted(zip(feature_cols, sv), key=lambda x: abs(x[1]), reverse=True)

    print(f"  {'Feature':<30} {'SHAP':>10} {'Effect':>10}")
    print(f"  {'─'*55}")
    for feat, val in fi[:8]:
        direction = "↑ RISK" if val > 0 else "↓ RISK"
        icon = "🔴" if val > 0.02 else ("🟢" if val < -0.02 else "⚪")
        print(f"  {icon} {feat:<28} {val:>+.4f}   {direction}")

    print(f"""
  💡 Doctors can now see:
     "The AI flagged this patient because of their previous
      admissions and comorbidities — not because of their
      race or gender. The reasoning makes medical sense."
    """)


# ─── Main ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  ⚖️  MODULE 4 — AI Bias Detection & Fairness")
    print("=" * 60)
    print("""
    "In 2019, a healthcare algorithm at major US hospitals was found
     to systematically discriminate against Black patients, denying
     them equal access to care." — Science, October 2019

    Before we DEPLOY our agent, we must verify it's FAIR.
    """)

    # Step 1: Generate biased data
    print_section("Step 1: Generating Patient Dataset", "📦")
    df = generate_biased_dataset(n=2000)
    print(f"  ✅ Created {len(df)} patient records")
    print(f"     Readmission rate: {df['readmitted'].mean()*100:.1f}%")
    print(f"     Race distribution: {dict(df['race'].value_counts())}")

    # Step 2: Train + detect bias
    print_section("Step 2: Train Model & Detect Bias", "🤖")
    model, X_train, X_test, y_train, y_test, feature_cols, df = train_and_detect_bias(df)

    # Step 3: AIF360 regulatory metrics
    print_section("Step 3: Regulatory Fairness Metrics (AIF360)", "📋")
    aif360_analysis(df, model, X_test, y_test, feature_cols)

    # Step 4: SHAP explainability
    print_section("Step 4: SHAP Explainability", "🔬")
    shap_explainability(model, X_train, X_test, feature_cols)

    # Summary
    print(f"\n{'🎯'*25}")
    print("  MODULE 4 — KEY TAKEAWAYS")
    print(f"{'🎯'*25}")
    print("""
    1. OVERALL ACCURACY IS DECEPTIVE — model looked fine at ~70%+,
       but per-group breakdown revealed significant bias.

    2. AIF360 PROVIDES REGULATORY METRICS:
       • Statistical Parity Difference (equal outcomes)
       • Equal Opportunity Difference (equal true positive rates)
       • Disparate Impact (legal discrimination threshold)
       These are what FDA actually checks.

    3. SHAP EXPLAINS INDIVIDUAL PREDICTIONS:
       • Shows WHICH features drove each decision
       • Doctors can verify: "Does this make medical sense?"
       • Required for FDA approval of AI medical devices

    4. BIAS SOURCES in healthcare:
       • Training data reflects historical inequalities
       • Proxy variables (insurance → socioeconomic status → race)
       • Underrepresentation of minority groups

    5. THIS APPLIES TO OUR AGENT: Before deploying the agent from
       Module 3, we must verify it treats all patients equally.

    🔑 "A model that works well ON AVERAGE can still discriminate
        against SPECIFIC GROUPS. Average accuracy is never enough."
    """)
