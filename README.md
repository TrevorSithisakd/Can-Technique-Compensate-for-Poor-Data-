# Can-Technique-Compensate-for-Poor-Data-
Controlled study of forecast skill on efficient large-cap US equities. The question is not "can I build a profitable model?" but instead 
"on a low signal to noise target, does model and feature sophistication buy you anything or is the limitation the data itself whether in quantity or quality?" 
The headline finding is a rigoursly supported negative where across 11 model/feature configurations, 
cross-sectional forecaast skill never clears the signifiicance bar. As a result sphistication is dominated by signal.

## Research question & hypotheses
Research question & hypotheses

On 5-day-ahead returns for large-cap US equities (2018–2024), how does forecast skill measured by the Information Coefficient (IC) scale with model
complexity, feature richness, and data quantity?
- **H1.** Mean cross-sectional IC is statistically indistinguishable from 0 across
every configuration.

- **H2.** No configuration significantly beats a momentum-only ridge baseline.

- **H3.** IC does not improve monotonically with more data the ceiling is
signal, not sample size.

### Metrics
Primary metric is mean per-date cross sectional IC with a Newey-West t-stat, significance bar is |t| > 2 on a hold-out.

### Why use Newey-West
Overlap-induced autocorrelation. Each 5-day return window shares four days
with the next, so consecutive daily ICs share inputs and are mechanically
autocorrelated even under zero skill. This shrinks the effective sample size
below the number of dates, so the naive std/sqrt(N) standard error is too
small and the t-stat is inflated — a false-positive trap. Newey-West adds the
lagged covariance terms out to lag 5 (beyond which windows no longer overlap),
restoring an honest standard error.
Heteroskedasticity. IC noise is far larger in turbulent regimes (e.g. March
2020) than in calm periods. A single pooled variance misstates the uncertainty;
the HAC estimator builds the SE from each date's own deviation, so it is robust
to the time-varying variance.

(placeholder)
