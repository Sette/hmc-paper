# Future Work vs. competitividade: diagnóstico e plano de experimentos

**Data:** 2026-11-09
**Escopo:** as três direções do parágrafo de Future Work (`main.tex:2253-2256`) e os datasets que elas citam.
**Status:** diagnóstico concluído; nenhum experimento novo foi executado.

---

## Resumo executivo

| Direção | Evidência | Veredito |
|---|---|---|
| **ESM-2** | Já rodado em `seq_FUN`/`seq_GO` com ESM congelado: AUPRC 0.5279 / 0.6011 vs 0.292 / 0.446 dos baselines publicados | **Sim**, ganho grande — mas é resultado de *feature* congelada, não end-to-end; reportar como cenário separado |
| **Texto nos rótulos GO** | Código implementado (`text`, `text+graph`, `pretrain_label_gae(features=...)`), mas **zero** execuções | **Talvez**; teste direto é barato (~1–2 h), mas exige preflight de cobertura do `go.obo` |
| **Tree ensembles diferenciáveis** | Só GBDT sklearn + reconcile pós-hoc; AUPRC 0.2256 vs 0.263 do neural | **Não**; sem evidência de ganho e custo de projeto à parte |

Recomendação: executar a Fase A (ESM + pipeline), depois a Fase B (texto GO com controles) e reenquadrar a Fase C como especulativa.

---

## 1. O trecho de Future Work

> "Future work will investigate coupling `SR-GAE` and `H-MLCL+KNN` with end-to-end biological sequence backbones (such as ESM-2), rich textual node definitions in the Rankin–Welch packing regime ($K_{\max} > D$), and differentiable tree ensembles with in-training reconciliation." (`main.tex:2253-2256`)

Mapeamento para datasets:

| Direção | Datasets-alvo | Por quê |
|---|---|---|
| ESM-2 | `seq_FUN`, `seq_GO` | únicos com ORFs recuperáveis (`data/yeast/*_ids.tsv`) |
| Texto nos rótulos | `cellcycle_GO`, `derisi_GO`, `pheno_GO` | regime $K_{\max} > D$ (dagger na Tabela 13) |
| Texto nos rótulos (secundário) | `gasch2_GO` | maior déficit verificado (0.418 vs HMCN-F 0.465), mas fora do regime de packing |
| Tree ensembles | FunCat, GO, cross-domain | onde o GBDT é o baseline tabular |

---

## 2. Posição competitiva atual (like-for-like)

| Família | Melhor baseline publicado | Nosso melhor | Δ | Status |
|---|---|---|---|---|
| FunCat (8 comuns) | C-HMCNN 0.264 | 0.263 | −0.001 | empatado |
| GO (8 comuns) | HMCN-F 0.422; C-HMCNN 0.420 | 0.421 | −0.001 / +0.001 | empatado |
| Cross-domain (4) | C-HMCNN 0.849 | 0.859 | +0.010 | à frente |
| WOS | HTC-CLIP 0.8786; HPT 0.8716 | 0.8704 | −0.0082 / −0.0012 | atrás, dentro do ruído |

ArXiv, AAPD, EUR-Lex e RCV1 não são like-for-like. O maior déficit verificado é `gasch2_GO`: 0.418 vs HMCN-F 0.465 (−0.047).

---

## 3. Diagnóstico por direção

### 3.1 ESM-2: ganho forte, mas não é o "end-to-end" prometido

O que existe:

- `src/hmc/features/protein.py`: `ProteinFeatureEncoder`, ESM-2 `facebook/esm2_t33_650M_UR50D` congelado, cache em disco.
- `experiments/run_protein_lm.py`: já rodou `seq_FUN` e `seq_GO`, 3 seeds × {`esm`, `esm+orig`} × {BCE, MCLoss}, protocolo validação-only.
- Saídas: `output/protein_lm/esm2_t33_650M_UR50D/{seq_FUN,seq_GO}.json`.

Resultados (ESM + MLP + R, 3 seeds):

| Dataset | ESM+BCE AUPRC | ESM+BCE F1 | Baseline publicado | Δ AUPRC |
|---|---:|---:|---:|---:|
| `seq_FUN` | **0.5279 ± 0.0029** | 0.5130 | C-HMCNN 0.292 / HMCN-F 0.291 | **+0.236 (+80.8%)** |
| `seq_GO` | **0.6011 ± 0.0031** | 0.5853 | C-HMCNN 0.446 / HMCN-F 0.447 | **+0.155 (+34.8%)** |

`esm+orig` é pior (0.5070 / 0.5734); MCLoss é levemente pior que BCE (0.5235 / 0.5963).

O que isso **não** prova:

- É ESM **congelado**, não fine-tuning end-to-end.
- Não há `SR-GAE`/`H-MLCL+KNN` nesses runs.
- É uma mudança de modalidade de entrada; os baselines usam features pré-extraídas.
- O ganho dominante é o próprio ESM como feature. Com base nos resultados com features originais, o ganho esperado do acoplamento é pequeno (+0.001 a +0.003 AUPRC — no limite do desvio entre seeds de `seq_GO`, 0.0031).

**Veredito:** sim, melhora a competitividade em `seq_FUN`/`seq_GO`, mas deve ser reportado como cenário separado "sequence-based". O "end-to-end" continua sendo future work de verdade.

### 3.2 Texto nos rótulos GO: viável e barata, mas nunca testada

O que existe:

- `experiments/run_label_embeddings.py`: heads `text` e `text+graph` para GO, usando SPECTER2 congelado do nome + definição de cada termo no `go.obo`.
- `src/hmc/models/hierarchical/label_embedding.py`: `go_term_texts`, `load_go_obo`, `LabelEmbeddingHead`.
- `pretrain_label_gae(..., features=...)` já aceita features de nós $(n, K)$ em CPU; normaliza cada linha, concatena com a identidade e mantém `z_sr` com shape `(n, dim)`. O cosine head, o H-MLCL e o KNN não mudam.

Viabilidade verificada:

- `data["node_names"]` existe para GO; nomes são `GO0003674`, e `go_term_texts` mapeia para `GO:0003674`; `root` cai no fallback.
- SPECTER2 já está cacheado em `models/allenai__specter2_base`; o download do `go.obo` funciona (36,7 MB, CC BY 4.0, build 2026-08-05).
- **Pré-requisito crítico:** medir a cobertura de `node_names` no `go.obo` antes de rodar; exigir ~≥95%, porque os ARFFs são de uma release antiga e `go_term_texts` faz fallback silencioso para o ID cru.

Controles que faltam no desenho atual:

- varredura de dimensão ($D=128/256$) para testar o mecanismo de packing;
- uma condição com embeddings textuais embaralhados, para separar semântica de capacidade.

O caminho `LabelEmbeddingHead` é um head alternativo e **não** alimenta texto no GAE; serve como tela independente, mas não substitui o teste direto.

**Veredito:** plausível; o teste direto é barato (~1–2 h). Se funcionar, a integração é literalmente `pretrain_label_gae(..., features=text)`.

### 3.3 Tree ensembles diferenciáveis: sem evidência e caro

O que existe:

- Apenas GBDT OvR do scikit-learn + reconciliação pós-hoc (`src/hmc/models/tabular/gbdt_ovr.py`, `run_protocol.py`).
- FunCat-8: GBDT AUPRC **0.2256** vs neural 0.263 (−0.037); F1 0.3014 (8 comuns) / 0.2850 (10 datasets).
- `run_gbdt_calibrated.py` faz GBDT + Platt + reconcile, mas `output/experiments/` não existe (nunca salvou); Platt piora AUPRC para 0.2125.
- Não há árvore diferenciável, soft tree, nem treino através do R.

**Veredito:** nenhuma evidência de ganho competitivo; implementar é um projeto à parte. Não rodar agora; reenquadrar a frase como especulativa (não é necessário removê-la).

---

## 4. Plano de experimentos

### Fase A — ESM congelado + pipeline completo (prioridade máxima)

Objetivo: medir o ganho do acoplamento `SR-GAE + H-MLCL+KNN + DepthCal` sobre o baseline ESM que já existe.

Mudanças de código:

- Em `experiments/run_sr_gae_sota.py`:
  - `_load_protocol_runs(..., objective=None, baseline_path=None, feature_tag=None)`: filtrar `runs` por **features e objective** (o JSON tem 3 seeds × 2 variantes × 2 objetivos; filtrar só por objetivo pega a variante errada) e exigir `set(by_seed) == set(SEEDS)`.
  - `run_sota_one(..., features="orig", objective=None, align=True)`: se `features != "orig"`, substituir `data["x"]` pelos splits ESM (reutilizar `read_ids`, `esm_features`, `read_proteome` de `run_protein_lm.py`), setar `baseline_path=output/protein_lm/esm2_t33_650M_UR50D/<name>.json` e `feature_tag=features`.
  - `--no-align`: o bloco de alinhamento (linhas ~381–386) reescreve o resultado para pelo menos o baseline e pode esconder um efeito negativo do acoplamento. Guardar `sr_gae_mlcl_unadjusted` e reportar os dois.
  - Batch: `run_sota_one` usa batch 64 para `_GO`, mas o baseline ESM usou `hp["batch"] = 4`; treinar o trunk ESM com batch 4 ou reportar apenas o resultado não ajustado.
- Saídas em subdiretórios por objetivo/feature (`output/sr_gae_protein/mc_esm/`, `.../bce_esm/`), para não colidir no cache por nome de dataset.

Execução:

```bash
cd /home/brunos/git/hmc-torch
# após o patch
.venv/bin/python experiments/run_sr_gae_sota.py \
  --datasets seq_FUN,seq_GO --features esm --objective mc \
  --out_dir output/sr_gae_protein/mc_esm --no-align
.venv/bin/python experiments/run_sr_gae_sota.py \
  --datasets seq_FUN,seq_GO --features esm --objective bce \
  --out_dir output/sr_gae_protein/bce_esm --no-align
```

Custo: ~0,5–1 h para MC, ~1–2 h incluindo BCE (embeddings ESM já cacheados; sem retreinar baseline).

Critério de sucesso (pré-registrado): ΔAUPRC pareado de `ESM+SR-GAE+H-MLCL+KNN+DepthCal` menos o baseline MLP ESM, MC, 3 seeds, **não ajustado**. Esperado realista: +0,001 a +0,003; exigir sinal consistente entre seeds e não alegar significância com n=3. Reportar também ΔF1, Δdeep F1 e os `gamma_proto`/`beta` escolhidos.

Enquadramento no paper: tabela separada "sequence-based", com a ressalva de modalidade; o resultado dominante é o ESM congelado, não o acoplamento.

### Fase B — texto nos rótulos GO (prioridade média)

Objetivo: testar se definições textuais ajudam exatamente onde o `SR-GAE` estrutural perde no regime $K_{\max} > D$.

1. **Preflight** — baixar e verificar o `go.obo`, medir cobertura por dataset:

```bash
cd /home/brunos/git/hmc-torch
mkdir -p data/ontologies
curl -fL -o data/ontologies/go.obo https://current.geneontology.org/ontology/go.obo
sha256sum data/ontologies/go.obo
PYTHONPATH=src:experiments .venv/bin/python - <<'PY'
import sys; sys.path.insert(0, "src"); sys.path.insert(0, "experiments")
from hmc.models.hierarchical.label_embedding import load_go_obo
from run_protocol import load_dataset
texts = load_go_obo("data/ontologies/go.obo")
for n in ["cellcycle_GO","derisi_GO","pheno_GO","gasch2_GO"]:
    d = load_dataset(n)
    names = [x for x, e in zip(d["node_names"], d["eval_mask"]) if e]
    miss = [x for x in names if f"GO:{x[2:]}" not in texts]
    print(n, len(names), len(miss), miss[:5])
PY
```

Exigir ≥95% de cobertura; registrar release, SHA-256 e licença (CC BY 4.0) no JSON de resultados.

2. **Teste direto** — `pretrain_label_gae(..., features=text)` vs sem features em `cellcycle_GO,derisi_GO,pheno_GO` (+`gasch2_GO` secundário), medindo similaridade sibling e AUPRC do cosine head; depois o pipeline completo. Reutilizar `go_text_embeddings` de `run_label_embeddings.py`; manter numpy em CPU, assert de `features.shape[0] == n`; incluir modelo/release na chave do cache.

```bash
# após o patch (--label_features)
.venv/bin/python experiments/run_sr_gae_sota.py \
  --datasets cellcycle_GO,derisi_GO,pheno_GO,gasch2_GO \
  --label_features text --out_dir output/sr_gae_text/text --force
```

3. **Controles** — `--dim 128/256` e uma condição com embeddings textuais embaralhados:

```bash
.venv/bin/python experiments/run_sr_gae_sota.py \
  --datasets cellcycle_GO,derisi_GO,pheno_GO --dim 128 \
  --out_dir output/sr_gae_text/dim128
.venv/bin/python experiments/run_sr_gae_sota.py \
  --datasets cellcycle_GO,derisi_GO,pheno_GO --dim 256 \
  --out_dir output/sr_gae_text/dim256
```

4. **Opcional** — tela com `LabelEmbeddingHead` (`--objective mc`, 3 seeds) como evidência suplementar; não é gate:

```bash
.venv/bin/python experiments/run_label_embeddings.py \
  --datasets cellcycle_GO,derisi_GO,pheno_GO,gasch2_GO \
  --objective mc --modes free,graph,text,text+graph --seeds 0 \
  --out_dir output/label_embeddings_go_screen
```

Custo: teste direto ~1–2 h; tela opcional 6–18 h.

Critério de sucesso: melhora de geometria (cosine sibling) e do cosine head nos três datasets de packing; AUPRC/F1 global é secundário. `cellcycle_GO` está a −0,001 do C-HMCNN (dentro do ruído); `pheno_GO` não tem baseline publicado; `gasch2_GO` (−0,047 vs HMCN-F) é um alvo diferente e mais difícil — não usar como critério do mecanismo.

### Fase C — tree ensembles diferenciáveis

Não rodar. Reenquadrar a frase do Future Work como especulativa/longo prazo, sem promessa de ganho competitivo. Se o usuário insistir num piloto: soft/differentiable tree em 4 datasets FunCat com R no treino; custo de semanas, retorno incerto.

### Fora do escopo do Future Work (quick wins opcionais)

- `gasch2_GO`: investigar o outlier do HMCN-F (0.465) e se o head textual ajuda.
- WOS: encoder de nomes de rótulos + retrieval poderia fechar 0,002–0,008 vs HTC-CLIP/HILL/MLCL-KNN.
- AAPD no split oficial SGM: converte o +0,100 não comparável em resultado verificado.

---

## 5. Arquivos e funções críticos

- `experiments/run_sr_gae_sota.py` — `_load_protocol_runs` (~270–301), `run_sota_one` (~304–444, especialmente 309–314, 327, 337–347, 381–386), `main` (~447–470).
- `experiments/run_protein_lm.py` — reutilizar `read_ids`, `esm_features`, `read_proteome`.
- `experiments/run_label_embeddings.py` — `go_text_embeddings` (~70–80), `OBO_PATH` (~66); adicionar `--obo_path`, cobertura e chave de cache com modelo/release.
- `src/hmc/models/hierarchical/graph_autoencoder.py` — `pretrain_label_gae` (~80–178); assert opcional de shape para `features`.
- `src/hmc/models/hierarchical/label_embedding.py` — `load_go_obo`/`go_term_texts` (~267–317).
- `docs/hmc-paper/main.tex:2253-2256` — só se for reenquadrar a Fase C.

---

## 6. Riscos e notas

- **ESM é mudança de modalidade:** os baselines C-HMCNN/HMCN-F usam features pré-extraídas; não comparar diretamente. Reportar como cenário "sequence-based".
- **Cobertura do `go.obo`:** ARFFs antigos podem não casar com a release atual; medir antes de gastar GPU.
- **Licença do GO:** CC BY 4.0; registrar release e SHA-256.
- **Ambiente:** usar `.venv/bin/python` ou `uv run`; o python do sistema não tem torch/numpy.
- **Não misturar** `output/sr_gae_sota/` (headline, protocolo SOTA) com `output/sr_gae_depth/` (ablation controlado, batch 32).
- **WOS corrigido (2026-11-09):** a lista per-seed do texto (0.8732/0.8667/0.8712) misturava valores do HPT (seed 123 `rec/thr0` = 0.8732; média `rec/val` = 0.8712) com o raw do globalE2E seed 0 (0.8667). Corrigida para os valores reconciliados dos JSONs, **0.8671/0.8693/0.8749**, em `main.tex` e na tese. O `0.8684 ± 0.0014` do HPT continua sem fonte nos artefatos salvos (summary: `raw/val` 0.8697 ± 0.0023; `rec/val` 0.8712 ± 0.0029) — re-verificar.

---

## 7. Sugestão de redação para o Future Work (não aplicada)

Se a Fase A confirmar o ganho e a Fase B for positiva, o parágrafo pode passar a distinguir o que já foi testado do que continua em aberto:

> "Future work will investigate end-to-end fine-tuning of biological sequence backbones (such as ESM-2), building on the frozen-ESM pilot that already improves `seq_FUN`/`seq_GO`; textual node definitions for GO labels in the Rankin–Welch regime; and differentiable tree ensembles with in-training reconciliation, which remain untested."

Não alterar `main.tex` antes dos resultados.
