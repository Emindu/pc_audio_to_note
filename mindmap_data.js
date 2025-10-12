// Auto-generated from mindmap_20251012_123023.json
const mindmapData = [
  {
    "id": "root",
    "text": "Autoregressive Process AR(p)",
    "parent": null,
    "level": 0,
    "position": { "x": 100, "y": 450 },
    "isCollapsed": false
  },
  {
    "id": "definition",
    "text": "Definition & Structure",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 100 },
    "isCollapsed": false
  },
  {
    "id": "char_poly",
    "text": "Characteristic Polynomial",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 200 },
    "isCollapsed": false
  },
  {
    "id": "stability",
    "text": "Stability & Stationarity",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 300 },
    "isCollapsed": false
  },
  {
    "id": "roots",
    "text": "Roots & Reciprocal Roots",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 400 },
    "isCollapsed": false
  },
  {
    "id": "state_space",
    "text": "State-Space Representation",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 500 },
    "isCollapsed": false
  },
  {
    "id": "forecast",
    "text": "Forecast Function",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 600 },
    "isCollapsed": false
  },
  {
    "id": "eigendecomp",
    "text": "Eigendecomposition",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 700 },
    "isCollapsed": false
  },
  {
    "id": "interpretation",
    "text": "Process Interpretation",
    "parent": "root",
    "level": 1,
    "position": { "x": 400, "y": 800 },
    "isCollapsed": false
  },
  {
    "id": "def_formula",
    "text": "Regress on past p values",
    "parent": "definition",
    "level": 2,
    "position": { "x": 700, "y": 50 },
    "isCollapsed": false
  },
  {
    "id": "order_p",
    "text": "Order p defines number of lags",
    "parent": "definition",
    "level": 2,
    "position": { "x": 700, "y": 100 },
    "isCollapsed": false
  },
  {
    "id": "epsilon_dist",
    "text": "ε_t ~ IID Normal(0, v)",
    "parent": "definition",
    "level": 2,
    "position": { "x": 700, "y": 150 },
    "isCollapsed": false
  },
  {
    "id": "parameters",
    "text": "p coefficients + variance",
    "parent": "definition",
    "level": 2,
    "position": { "x": 700, "y": 200 },
    "isCollapsed": false
  },
  {
    "id": "poly_def",
    "text": "Φ(u) polynomial of order p",
    "parent": "char_poly",
    "level": 2,
    "position": { "x": 700, "y": 225 },
    "isCollapsed": false
  },
  {
    "id": "poly_function",
    "text": "Function of φ coefficients",
    "parent": "char_poly",
    "level": 2,
    "position": { "x": 700, "y": 275 },
    "isCollapsed": false
  },
  {
    "id": "poly_purpose",
    "text": "Characterizes process properties",
    "parent": "char_poly",
    "level": 2,
    "position": { "x": 700, "y": 325 },
    "isCollapsed": false
  },
  {
    "id": "quasi_periodic",
    "text": "Identifies quasi-periodic behavior",
    "parent": "poly_purpose",
    "level": 3,
    "position": { "x": 1000, "y": 300 },
    "isCollapsed": false
  },
  {
    "id": "stationarity_check",
    "text": "Determines stationarity",
    "parent": "poly_purpose",
    "level": 3,
    "position": { "x": 1000, "y": 350 },
    "isCollapsed": false
  },
  {
    "id": "stability_cond",
    "text": "Stability Condition",
    "parent": "stability",
    "level": 2,
    "position": { "x": 700, "y": 375 },
    "isCollapsed": false
  },
  {
    "id": "unit_circle",
    "text": "All roots outside unit circle",
    "parent": "stability_cond",
    "level": 3,
    "position": { "x": 1000, "y": 375 },
    "isCollapsed": false
  },
  {
    "id": "modulus_gt_one",
    "text": "Modulus |u| > 1 for all roots",
    "parent": "stability_cond",
    "level": 3,
    "position": { "x": 1000, "y": 425 },
    "isCollapsed": false
  },
  {
    "id": "stable_stationary",
    "text": "Stable process is stationary",
    "parent": "stability",
    "level": 2,
    "position": { "x": 700, "y": 475 },
    "isCollapsed": false
  },
  {
    "id": "ma_representation",
    "text": "Can write as infinite MA process",
    "parent": "stability",
    "level": 2,
    "position": { "x": 700, "y": 525 },
    "isCollapsed": false
  },
  {
    "id": "backshift_op",
    "text": "Uses backshift operator B",
    "parent": "ma_representation",
    "level": 3,
    "position": { "x": 1000, "y": 500 },
    "isCollapsed": false
  },
  {
    "id": "psi_sum",
    "text": "Ψ(B) = Σ Ψ_j B^j, j=0 to ∞",
    "parent": "ma_representation",
    "level": 3,
    "position": { "x": 1000, "y": 550 },
    "isCollapsed": false
  },
  {
    "id": "reciprocal_roots",
    "text": "Reciprocal roots α_1, α_2, ..., α_p",
    "parent": "roots",
    "level": 2,
    "position": { "x": 700, "y": 600 },
    "isCollapsed": false
  },
  {
    "id": "root_properties",
    "text": "Determine process behavior",
    "parent": "roots",
    "level": 2,
    "position": { "x": 700, "y": 650 },
    "isCollapsed": false
  },
  {
    "id": "real_complex",
    "text": "Real vs complex valued roots",
    "parent": "root_properties",
    "level": 3,
    "position": { "x": 1000, "y": 625 },
    "isCollapsed": false
  },
  {
    "id": "modulus_impact",
    "text": "Modulus affects contribution",
    "parent": "root_properties",
    "level": 3,
    "position": { "x": 1000, "y": 675 },
    "isCollapsed": false
  },
  {
    "id": "ss_equations",
    "text": "State-Space Equations",
    "parent": "state_space",
    "level": 2,
    "position": { "x": 700, "y": 700 },
    "isCollapsed": false
  },
  {
    "id": "obs_equation",
    "text": "Observation: y_t = F^T x_t",
    "parent": "ss_equations",
    "level": 3,
    "position": { "x": 1000, "y": 675 },
    "isCollapsed": false
  },
  {
    "id": "state_equation",
    "text": "State: x_t = G x_{t-1} + w_t",
    "parent": "ss_equations",
    "level": 3,
    "position": { "x": 1000, "y": 725 },
    "isCollapsed": false
  },
  {
    "id": "markov_structure",
    "text": "Markovian structure",
    "parent": "ss_equations",
    "level": 3,
    "position": { "x": 1000, "y": 775 },
    "isCollapsed": false
  },
  {
    "id": "g_matrix",
    "text": "G Matrix Structure",
    "parent": "state_space",
    "level": 2,
    "position": { "x": 700, "y": 800 },
    "isCollapsed": false
  },
  {
    "id": "g_first_row",
    "text": "First row: AR coefficients",
    "parent": "g_matrix",
    "level": 3,
    "position": { "x": 1000, "y": 775 },
    "isCollapsed": false
  },
  {
    "id": "g_identity",
    "text": "Block: identity matrix",
    "parent": "g_matrix",
    "level": 3,
    "position": { "x": 1000, "y": 825 },
    "isCollapsed": false
  },
  {
    "id": "g_eigenvalues",
    "text": "Eigenvalues = reciprocal roots",
    "parent": "g_matrix",
    "level": 3,
    "position": { "x": 1000, "y": 875 },
    "isCollapsed": false
  },
  {
    "id": "vectors",
    "text": "Vector Definitions",
    "parent": "state_space",
    "level": 2,
    "position": { "x": 700, "y": 900 },
    "isCollapsed": false
  },
  {
    "id": "x_vector",
    "text": "x_t = [y_t, y_{t-1}, ..., y_{t-p+1}]",
    "parent": "vectors",
    "level": 3,
    "position": { "x": 1000, "y": 875 },
    "isCollapsed": false
  },
  {
    "id": "f_vector",
    "text": "F = [1, 0, 0, ..., 0]^T",
    "parent": "vectors",
    "level": 3,
    "position": { "x": 1000, "y": 925 },
    "isCollapsed": false
  },
  {
    "id": "w_vector",
    "text": "w_t = [ε_t, 0, 0, ..., 0]^T",
    "parent": "vectors",
    "level": 3,
    "position": { "x": 1000, "y": 975 },
    "isCollapsed": false
  },
  {
    "id": "forecast_def",
    "text": "Definition: f_t(h)",
    "parent": "forecast",
    "level": 2,
    "position": { "x": 700, "y": 1000 },
    "isCollapsed": false
  },
  {
    "id": "forecast_notation",
    "text": "E[y_{t+h} | y_1, ..., y_t]",
    "parent": "forecast_def",
    "level": 3,
    "position": { "x": 1000, "y": 975 },
    "isCollapsed": false
  },
  {
    "id": "h_steps",
    "text": "h = steps ahead forecast",
    "parent": "forecast_def",
    "level": 3,
    "position": { "x": 1000, "y": 1025 },
    "isCollapsed": false
  },
  {
    "id": "forecast_formula",
    "text": "Forecast Formula",
    "parent": "forecast",
    "level": 2,
    "position": { "x": 700, "y": 1075 },
    "isCollapsed": false
  },
  {
    "id": "f_g_power",
    "text": "F^T G^h x_t",
    "parent": "forecast_formula",
    "level": 3,
    "position": { "x": 1000, "y": 1050 },
    "isCollapsed": false
  },
  {
    "id": "g_power_h",
    "text": "G matrix raised to h power",
    "parent": "forecast_formula",
    "level": 3,
    "position": { "x": 1000, "y": 1100 },
    "isCollapsed": false
  },
  {
    "id": "eigen_formula",
    "text": "G = E Λ E^{-1}",
    "parent": "eigendecomp",
    "level": 2,
    "position": { "x": 700, "y": 1150 },
    "isCollapsed": false
  },
  {
    "id": "lambda_matrix",
    "text": "Λ diagonal with α_1, ..., α_p",
    "parent": "eigen_formula",
    "level": 3,
    "position": { "x": 1000, "y": 1125 },
    "isCollapsed": false
  },
  {
    "id": "e_eigenvectors",
    "text": "E matrix of eigenvectors",
    "parent": "eigen_formula",
    "level": 3,
    "position": { "x": 1000, "y": 1175 },
    "isCollapsed": false
  },
  {
    "id": "power_decomp",
    "text": "G^h decomposition",
    "parent": "eigendecomp",
    "level": 2,
    "position": { "x": 700, "y": 1225 },
    "isCollapsed": false
  },
  {
    "id": "alpha_power",
    "text": "α_j^h terms in forecast",
    "parent": "power_decomp",
    "level": 3,
    "position": { "x": 1000, "y": 1225 },
    "isCollapsed": false
  },
  {
    "id": "forecast_sum",
    "text": "Σ c_j α_j^h, j=1 to p",
    "parent": "power_decomp",
    "level": 3,
    "position": { "x": 1000, "y": 1275 },
    "isCollapsed": false
  },
  {
    "id": "exponential_decay",
    "text": "Exponential Decay",
    "parent": "interpretation",
    "level": 2,
    "position": { "x": 700, "y": 1325 },
    "isCollapsed": false
  },
  {
    "id": "stable_decay",
    "text": "Stable: |α_j| < 1, decays",
    "parent": "exponential_decay",
    "level": 3,
    "position": { "x": 1000, "y": 1300 },
    "isCollapsed": false
  },
  {
    "id": "decay_rate",
    "text": "Decay rate as function of h",
    "parent": "exponential_decay",
    "level": 3,
    "position": { "x": 1000, "y": 1350 },
    "isCollapsed": false
  },
  {
    "id": "behavior_types",
    "text": "Behavior Types",
    "parent": "interpretation",
    "level": 2,
    "position": { "x": 700, "y": 1425 },
    "isCollapsed": false
  },
  {
    "id": "complex_quasi",
    "text": "Complex roots: quasi-periodic",
    "parent": "behavior_types",
    "level": 3,
    "position": { "x": 1000, "y": 1400 },
    "isCollapsed": false
  },
  {
    "id": "real_non_quasi",
    "text": "Real roots: non-quasi-periodic",
    "parent": "behavior_types",
    "level": 3,
    "position": { "x": 1000, "y": 1450 },
    "isCollapsed": false
  },
  {
    "id": "contribution",
    "text": "Root Contribution",
    "parent": "interpretation",
    "level": 2,
    "position": { "x": 700, "y": 1525 },
    "isCollapsed": false
  },
  {
    "id": "large_modulus",
    "text": "Large modulus: more contribution",
    "parent": "contribution",
    "level": 3,
    "position": { "x": 1000, "y": 1500 },
    "isCollapsed": false
  },
  {
    "id": "close_to_one",
    "text": "Closer to ±1: stronger influence",
    "parent": "contribution",
    "level": 3,
    "position": { "x": 1000, "y": 1550 },
    "isCollapsed": false
  }
];