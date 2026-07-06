#!/usr/bin/env bash
# trim_skills.sh — trim duplicate/cluttered skills from a skill directory
#
# Default mode: ARCHIVE (move to _deprecated_skills/ — fully reversible)
# Add --hard     to permanently delete (only after you've reviewed the archive)
# Add --dry-run  to preview changes without modifying anything
#
# Usage:
#   chmod +x trim_skills.sh
#   ./trim_skills.sh                                    # archive mode in cwd
#   ./trim_skills.sh --target-dir ~/my-skills           # archive mode in another dir
#   ./trim_skills.sh --dry-run                          # preview only
#   ./trim_skills.sh --hard                             # DESTRUCTIVE — type 'DELETE' to confirm
#
# Safe by default. Hard-delete requires explicit opt-in.

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TARGET_DIR="."
DRY_RUN=false
HARD_DELETE=false

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --target-dir) TARGET_DIR="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=true; shift ;;
    --hard)       HARD_DELETE=true; shift ;;
    -h|--help)
      sed -n '2,15p' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: target directory does not exist: $TARGET_DIR"
  exit 1
fi

cd "$TARGET_DIR"
echo "Working directory: $(pwd)"
echo ""

# ---------------------------------------------------------------------------
# Skill list — edit this section if you want to add/remove entries
# ---------------------------------------------------------------------------

SKILLS_TO_REMOVE=(
  # ── Architecture duplicates (7) ──────────────────────────────────────────
  solution-architect
  saas-architect
  integration-architect
  infrastructure-architect
  system-design
  engineering-architecture-review
  engineering-leadership            # parent folder; removes 3 sub-skills inside

  # ── Backend duplicates (14) ──────────────────────────────────────────────
  backend-architect
  backend-django
  backend-express
  backend-nestjs
  backend-graphql
  backend-grpc
  backend-websocket
  backend-microservices
  backend-authorization
  backend-caching
  backend-background-jobs
  backend-performance
  api-engineer
  backend-engineers                # plural — will be replaced by singular

  # ── Frontend / UI / UX duplicates (10) ───────────────────────────────────
  ui-ux-pro-max
  design-ui
  design-ux
  frontend-ui-engineering
  frontend-nextjs
  frontend-javascript
  frontend-tailwindcss
  frontend-state-management
  frontend-seo
  frontend-engineers               # plural — will be replaced by singular

  # ── Database / data duplicates (13) ──────────────────────────────────────
  database-mongodb
  database-elasticsearch
  database-prisma
  database-migrations
  database-indexing
  database-query-optimization
  database-replication
  data-engineering-airflow
  data-engineering-dbt
  data-engineering-kafka
  data-engineering-spark
  data-science-analytics
  data-science-statistics

  # ── Cloud / DevOps duplicates (11) ───────────────────────────────────────
  cloud-aws
  cloud-serverless
  cloud-networking
  cloud-iam
  cloud-cost-optimization
  dev-ops-engineer                 # typo variant — use devops-engineer
  devops-github-actions
  devops-jenkins
  devops-nginx
  devops-monitoring
  devops-logging

  # ── Security duplicates (3) ──────────────────────────────────────────────
  security-api-security
  security-owasp
  security-zero-trust

  # ── Leadership / process duplicates (6) ──────────────────────────────────
  vp-engineering
  engineering-best-practices
  engineering-performance
  product-management
  project-management
  operations

  # ── ML / AI duplicates (6) ───────────────────────────────────────────────
  ml-pytorch
  ml-tensorflow
  ml-sklearn
  mlops-mlflow
  mlops-ci-cd
  mlops-monitoring

  # ── LLM foundational (2) ────────────────────────────────────────────────
  llm-serving
  llm-transformers

  # ── Orchestrators that don't add value (8) ───────────────────────────────
  phase-2-orchestrator
  phase-3-orchestrator
  phase-4-orchestrator
  phase-6-orchestrator
  phase-7-orchestrator
  phase-8-orchestrator
  phase-10-orchestrator
  phase-11-orchestrator

  # ── Typos and specials (1) ───────────────────────────────────────────────
  business-aalyst                  # typo of business-analyst (keep the latter)
)

# ---------------------------------------------------------------------------
# Hard-delete confirmation gate
# ---------------------------------------------------------------------------

if [ "$HARD_DELETE" = true ] && [ "$DRY_RUN" = false ]; then
  echo "⚠️  HARD DELETE MODE — files will be PERMANENTLY removed."
  echo "    Target: $TARGET_DIR"
  echo ""
  read -rp "Type 'DELETE' (in caps) to confirm: " confirm
  if [ "$confirm" != "DELETE" ]; then
    echo "Aborted — no changes made."
    exit 1
  fi
  echo ""
fi

# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

MODE=$([ "$HARD_DELETE" = true ] && echo "HARD DELETE" || ([ "$DRY_RUN" = true ] && echo "DRY RUN" || echo "ARCHIVE"))

echo "============================================================"
echo "  SKILL ROSTER TRIM"
echo "  Mode:    $MODE"
echo "  Target:  $TARGET_DIR"
echo "  Entries: ${#SKILLS_TO_REMOVE[@]}"
echo "============================================================"
echo ""

if [ "$HARD_DELETE" = false ] && [ "$DRY_RUN" = false ]; then
  mkdir -p _deprecated_skills
fi

found=0
missing=0
acted=0

for skill in "${SKILLS_TO_REMOVE[@]}"; do
  if [ -d "$skill" ]; then
    found=$((found+1))
    if [ "$DRY_RUN" = true ]; then
      echo "  [DRY] would remove: $skill"
      acted=$((acted+1))
    elif [ "$HARD_DELETE" = true ]; then
      rm -rf "$skill"
      echo "  [DELETED] $skill"
      acted=$((acted+1))
    else
      mv "$skill" _deprecated_skills/
      echo "  [ARCHIVED] $skill -> _deprecated_skills/"
      acted=$((acted+1))
    fi
  else
    missing=$((missing+1))
    echo "  [SKIP] not found: $skill"
  fi
done

echo ""
echo "============================================================"
echo "  Summary: found=$found  acted=$acted  missing=$missing"
echo "============================================================"
echo ""

# ---------------------------------------------------------------------------
# Post-run guidance
# ---------------------------------------------------------------------------

if [ "$DRY_RUN" = true ]; then
  echo "Dry run complete. No changes made."
  echo "Run without --dry-run to actually archive."
elif [ "$HARD_DELETE" = true ]; then
  echo "Hard delete complete. Cannot be undone."
else
  echo "Archive complete."
  echo ""
  echo "Next steps:"
  echo "  1. cd $TARGET_DIR && ls _deprecated_skills/        # verify the archive"
  echo "  2. Spot-check that any content you needed was already merged into the kept skills."
  echo "  3. After a grace period (recommend: 1 sprint), run with --hard to delete."
  echo "     Example: ./trim_skills.sh --target-dir $TARGET_DIR --hard"
fi
