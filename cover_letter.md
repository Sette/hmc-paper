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
3. A **structural analysis of constraint utility**: the reconciliation gain across the 27
   datasets is not predicted by static positive-label density on internal nodes (Spearman
   $\rho = -0.07$, $p = 0.721$); it follows the average score raise that bottom-up
   propagation induces on internal nodes ($\rho = 0.49$, $p = 0.009$), a quantity known
   only after training.
4. A **sparse $O(C+E)$ formulation of the R-matrix (`BlockDiagonalR`)** that enforces exact
   ancestor-closure consistency on large DAGs without materializing the dense $C \times C$
   matrix ($>1{,}400\times$ structural memory reduction), enabling batch sizes that exhaust
   GPU memory under the dense formulation (up to 4,134 classes in Gene Ontology).
5. An **independent reproducibility audit** of the Surj ontology autoencoder, whose reported
   gains we could not reproduce from the published specification, together with a
   **negative result on ontology embeddings**. Standard ontology graph autoencoders place
   sibling classes on nearly parallel directions (median cosine up to 0.9995); a
   sibling-repulsive variant (`SR-GAE`) removes this collapse (median $\le 0.038$), but in a
   paired three-seed evaluation with a random-prototype control the repaired prototypes add
   nothing to a reconciled classifier. The small gain we measure ($+0.0022$ Micro-AUPRC,
   higher on 25/27 datasets) comes from $k$-NN retrieval in a contrastive embedding, and
   per-depth logit offsets raise global Micro-F1 slightly while lowering F1 on the deepest
   levels of FunCat and Gene Ontology.

**Why KBS.** The work is about knowledge injection from taxonomies and ontologies into
learning systems, evaluated on text, genomic, and cross-domain hierarchies. It does not
propose a new application of an existing method; it isolates when the knowledge constraint
helps and when it does not, which is directly relevant to the journal's readership.

**Originality and ethics.** The manuscript is original and all authors have approved the
submission. [TODO before submitting: a shorter conference paper covering the factorial
study and the sparse operator was prepared for IJCNN; state its status here (under review,
accepted, or withdrawn) and how this manuscript extends it. Do not keep the sentence "not
under consideration elsewhere" unless that is true on the submission date.] The R-matrix idea is credited to
Giunchiglia and Lukasiewicz (NeurIPS 2020); our contribution is the sparse formulation, the
systematic evaluation, and the reproducibility findings. Code and artifacts are available
at https://github.com/Sette/hmc-torch.

We suggest the following reviewers (no conflicts of interest): [TODO: 4--6 names].

Thank you for your consideration.

Sincerely,
Bruno Silva Sette
Federal University of São Carlos (UFSCar), Brazil
