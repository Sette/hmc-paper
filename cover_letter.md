# Cover letter — Knowledge-Based Systems

**Manuscript:** *When Do Hierarchical Constraints Help? A Systematic Study of R-Matrix
Consistency and Reconciliation in Hierarchical Multi-Label Classification*

**Authors:** Bruno Sette, [Orientador] (Federal University of São Carlos, UFSCar, Brazil)
**Corresponding author:** Bruno Sette — brunosilvasette@gmail.com

Dear Editor,

We submit the manuscript above for consideration in *Knowledge-Based Systems*. The paper
studies how explicit knowledge about a class hierarchy—a taxonomy or ontology—should be
injected into a multi-label classifier. This is a core knowledge-based systems question:
the hierarchy is the structured knowledge, and the R-matrix is the mechanism that enforces
consistency between an ancestor and its descendants.

**What the paper contributes.**
1. A **sparse O(C+E) formulation of the R-matrix** that preserves the hierarchical
   consistency constraint on large DAGs without materializing the dense C×C matrix,
   enabling batch sizes that do not fit in GPU memory with the dense form (up to 4,134
   classes in Gene Ontology).
2. A **controlled study of three training objectives** (BCE, hinge, and the MCLoss of
   C-HMCNN) with and without inference-time reconciliation, on 27 datasets spanning text,
   FunCat, Gene Ontology, and cross-domain ARFF benchmarks, under a validation-only
   protocol.
3. A clear empirical answer: **the gain comes from reconciliation at inference time, not
   from the consistency loss during training**. BCE with reconciliation is competitive with
   MCLoss, and MCLoss raw scores can collapse before reconciliation. The paper is therefore
   as useful for what it rules out as for what it recommends.
4. A **reproducibility study** showing that the reported Surj results cannot be reproduced
   from the published description, with the reimplementation, recipes, and per-seed scores
   released.
5. An open-source, modular implementation (`hmc-torch`) that makes the study reproducible
   and extensible.

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
Bruno Sette
Federal University of São Carlos (UFSCar), Brazil
