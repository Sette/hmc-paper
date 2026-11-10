# Cover letter — Knowledge-Based Systems

**Manuscript:** *Scalable R-Matrix Reconciliation, Sibling-Repulsive Ontology Graphs, and
Contrastive Learning for Hierarchical Multi-Label Classification*

**Authors:** Bruno Silva Sette, Diego Furtado Silva (Federal University of São Carlos, UFSCar, Brazil)
**Corresponding author:** Bruno Silva Sette — bruno.sette@ufscar.br

Dear Editor,

We submit the manuscript above for consideration in *Knowledge-Based Systems*. The paper
studies how explicit knowledge about a class hierarchy—a taxonomy or ontology—should be
injected into a multi-label classifier. This is a core knowledge-based systems question:
the hierarchy is the structured knowledge, and the R-matrix is the mechanism that enforces
consistency between an ancestor and its descendants.

**What the paper contributes.**
1. A **controlled $3 \times 2$ factorial decomposition of three training objectives** (BCE,
   hierarchical hinge, and the MCLoss of C-HMCNN) crossed with raw versus reconciled
   inference across **27 benchmarks** spanning four domain families (scientific/legal text,
   FunCat, Gene Ontology, and cross-domain ARFF) under a strict validation-only protocol.
2. A clear empirical answer to when hierarchical constraints help: **the gain comes from
   reconciliation at inference time (Wilcoxon $p = 2.1 \times 10^{-7}$ on Micro-AUPRC across
   26/27 datasets; $p = 1.3 \times 10^{-6}$ on Micro-F1 across 25/27 datasets), not from the
   consistency loss during training**. Unconstrained BCE with reconciliation matches MCLoss,
   whereas raw MCLoss scores collapse on internal nodes prior to reconciliation.
3. A **structural explanation of constraint utility**: reconciliation gain across the 27
   datasets is not predicted by static positive-label density on internal nodes (Spearman
   $\rho = -0.07$, $p = 0.721$), but correlates significantly with the average score raise
   induced on internal nodes during bottom-up propagation ($\rho = 0.49$, $p = 0.009$).
4. A **sparse $O(C+E)$ formulation of the R-matrix (`BlockDiagonalR`)** that enforces exact
   ancestor-closure consistency on large DAGs without materializing the dense $C \times C$
   matrix ($>1{,}400\times$ structural memory reduction), enabling batch sizes that exhaust
   GPU memory under the dense formulation (up to 4,134 classes in Gene Ontology).
5. An **independent reproducibility audit** showing that the reported Surj ontology
   autoencoder results cannot be verified from the published specification, deriving a
   Bessel-type bound explaining why standard ontology graph autoencoders collapse
   sibling classes (median cosine up to 0.9995), and introducing the **Sibling-Repulsive Graph
   Autoencoder (`SR-GAE`)**, **Hierarchical Multi-Label Contrastive Learning with $k$-NN
   retrieval (`H-MLCL+H-KNN`)**, and **Consistency-Preserving Depth Calibration (`DepthCal`)**.
   `SR-GAE`+`H-MLCL+H-KNN` reduces the median sibling cosine to $\le 0.038$ and strictly
   improves test Micro-AUPRC over the matched baseline on 27/27 benchmarks over 3 seeds
   (Wilcoxon $p = 1.5 \times 10^{-8}$; 26/27 strict wins in 3-seed controlled ablation,
   $p = 4.5 \times 10^{-8}$); the method matches C-HMCNN on Gene Ontology (0.421 vs. 0.420
   AUPRC, winning on 5/8 datasets) while 0.001 below HMCN-F (0.422), and improves cross-domain
   benchmarks (0.859 vs. 0.849 AUPRC). The full pipeline with `DepthCal` lifts deep-level F1
   by $+13.0\%$ on FunCat and $+24.1\%$ on Gene Ontology level 5 with zero hierarchy
   violations; `DepthCal` alone trades AUPRC for F1 (11/27 vs. 18/27), so it is a calibration
   choice for F1 rather than a uniform gain.

**Why KBS.** The work is about knowledge injection from taxonomies and ontologies into
learning systems, evaluated on text, genomic, and cross-domain hierarchies. It does not
propose a new application of an existing method; it isolates when the knowledge constraint
helps and when it does not, which is directly relevant to the journal's readership.

**Originality and ethics.** The manuscript is original, is not under consideration
elsewhere, and all authors have approved the submission. The R-matrix idea is credited to
Giunchiglia and Lukasiewicz (NeurIPS 2020); our contribution is the sparse formulation, the
systematic evaluation, and the reproducibility findings. Code and artifacts are available
at https://github.com/Sette/hmc-torch.

We suggest the following reviewers (no conflicts of interest): [TODO: 4--6 names].

Thank you for your consideration.

Sincerely,
Bruno Silva Sette
Federal University of São Carlos (UFSCar), Brazil
