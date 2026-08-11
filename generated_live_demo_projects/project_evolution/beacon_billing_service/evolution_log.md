# Evolution Log

Baseline purpose: Billing and invoice service with REST-style routes and background invoice jobs.

## PR Sequence

### 1. Add invoice payment endpoint

- Case: `BEACON-BILLING-SERVICE-PR-01`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `docs/api.md`
- Change: Document invoice payment endpoint.
- DocGuard prediction: see generated results below

### 2. Add invoice reviewer field

- Case: `BEACON-BILLING-SERVICE-PR-02`
- Difficulty: `easy`
- Docs update required: `True`
- Expected target doc: `docs/models.md`
- Change: Document invoice reviewerId.
- DocGuard prediction: see generated results below

### 3. Change billing page size default

- Case: `BEACON-BILLING-SERVICE-PR-03`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `docs/configuration.md`
- Change: Update default page size docs.
- DocGuard prediction: see generated results below

### 4. Require billing role on invoice routes

- Case: `BEACON-BILLING-SERVICE-PR-04`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `docs/architecture.md`
- Change: Document billing role middleware behavior.
- DocGuard prediction: see generated results below

### 5. Add invoice export seed command

- Case: `BEACON-BILLING-SERVICE-PR-05`
- Difficulty: `easy`
- Docs update required: `True`
- Expected target doc: `docs/developer-setup.md`
- Change: Document invoice seed flow.
- DocGuard prediction: see generated results below

### 6. Refactor invoice formatting helper

- Case: `BEACON-BILLING-SERVICE-PR-06`
- Difficulty: `medium`
- Docs update required: `False`
- Expected target doc: `none`
- Change: Private helper extraction only.
- DocGuard prediction: see generated results below

### 7. Notify customers about invoice review window

- Case: `BEACON-BILLING-SERVICE-PR-07`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `CHANGELOG.md`
- Change: Mention customer notification behavior in changelog.
- DocGuard prediction: see generated results below

### 8. Clean up log message

- Case: `BEACON-BILLING-SERVICE-PR-08`
- Difficulty: `easy`
- Docs update required: `False`
- Expected target doc: `none`
- Change: Logging message wording only.
- DocGuard prediction: see generated results below

## DocGuard Runner Results

- `BEACON-BILLING-SERVICE-PR-01`: docs `True`, category `api_reference`, target `docs/api.md`.
- `BEACON-BILLING-SERVICE-PR-02`: docs `True`, category `model_contract`, target `docs/models.md`.
- `BEACON-BILLING-SERVICE-PR-03`: docs `True`, category `configuration`, target `docs/configuration.md`.
- `BEACON-BILLING-SERVICE-PR-04`: docs `True`, category `architecture_flow`, target `docs/architecture.md`.
- `BEACON-BILLING-SERVICE-PR-05`: docs `True`, category `developer_setup`, target `docs/developer-setup.md`.
- `BEACON-BILLING-SERVICE-PR-06`: docs `False`, category `no_update`, target `none`.
- `BEACON-BILLING-SERVICE-PR-07`: docs `True`, category `changelog`, target `CHANGELOG.md`.
- `BEACON-BILLING-SERVICE-PR-08`: docs `False`, category `no_update`, target `none`.
