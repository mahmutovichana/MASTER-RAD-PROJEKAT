# Evolution Log

Baseline purpose: Billing and invoice service with REST-style routes and background invoice jobs.

## PR Sequence

### 1. Add invoice payment endpoint

- Case: `BEACON-BILLING-SERVICE-PR-01`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `docs/api.md`
- Change: Document invoice payment endpoint.
- DocGuard prediction: pending runner execution

### 2. Add invoice reviewer field

- Case: `BEACON-BILLING-SERVICE-PR-02`
- Difficulty: `easy`
- Docs update required: `True`
- Expected target doc: `docs/models.md`
- Change: Document invoice reviewerId.
- DocGuard prediction: pending runner execution

### 3. Change billing page size default

- Case: `BEACON-BILLING-SERVICE-PR-03`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `docs/configuration.md`
- Change: Update default page size docs.
- DocGuard prediction: pending runner execution

### 4. Require billing role on invoice routes

- Case: `BEACON-BILLING-SERVICE-PR-04`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `docs/architecture.md`
- Change: Document billing role middleware behavior.
- DocGuard prediction: pending runner execution

### 5. Add invoice export seed command

- Case: `BEACON-BILLING-SERVICE-PR-05`
- Difficulty: `easy`
- Docs update required: `True`
- Expected target doc: `docs/developer-setup.md`
- Change: Document invoice seed flow.
- DocGuard prediction: pending runner execution

### 6. Refactor invoice formatting helper

- Case: `BEACON-BILLING-SERVICE-PR-06`
- Difficulty: `medium`
- Docs update required: `False`
- Expected target doc: `none`
- Change: Private helper extraction only.
- DocGuard prediction: pending runner execution

### 7. Notify customers about invoice review window

- Case: `BEACON-BILLING-SERVICE-PR-07`
- Difficulty: `medium`
- Docs update required: `True`
- Expected target doc: `CHANGELOG.md`
- Change: Mention customer notification behavior in changelog.
- DocGuard prediction: pending runner execution

### 8. Clean up log message

- Case: `BEACON-BILLING-SERVICE-PR-08`
- Difficulty: `easy`
- Docs update required: `False`
- Expected target doc: `none`
- Change: Logging message wording only.
- DocGuard prediction: pending runner execution
