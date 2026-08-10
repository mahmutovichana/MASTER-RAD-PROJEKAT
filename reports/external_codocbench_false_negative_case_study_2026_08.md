# External CoDocBench False Negative Case Study 2026-08

## Record

- Record id: `codocbench-cpython-6ffface4293f20e504de6a7ca012c482a203409d-move-338`
- Repository: `cpython`
- Owner: `python`
- Function: `move`
- Commit hash: `6ffface4293f20e504de6a7ca012c482a203409d`
- Commit date/time: `2014-06-11 14:40:13-04:00`
- Label source: `strong_positive_code_doc_cochange`

## Prediction

- Gold docs_update_required: `true`
- Predicted docs_update_required: `false`
- Predicted doc category: `no_update`
- Predicted scenario type: `docs_already_updated`
- Predicted target doc file: empty
- Confidence: `0.5493`

## Code Diff Excerpt

```diff
- def move(src, dst):
+ def move(src, dst, copy_function=copy2):
...
+             copytree(src, real_dst, copy_function=copy_function,
+                      symlinks=True)
```

## Documentation Diff Excerpt

```diff
 Recursively move a file or directory to another location.
...
+ The optional `copy_function` argument is a callable that will be used
+ to copy the source or it will be delegated to `copytree`.
```

## Possible Explanation

The change adds an optional parameter and updates the docstring to describe it. The model may have predicted `docs_already_updated` because this is an external docstring-level API documentation change rather than the synthetic project-level Markdown documentation shape it was trained on. It may also be confused by the fact that CoDocBench pairs already include documentation changes, while DocGuard normally predicts whether a project documentation update is needed before the future documentation patch exists.

## Assessment

This looks more like a model/domain issue than an obvious mapping issue because the record has code diff, doc before, doc diff, repository, function, and commit metadata. It still requires manual audit before being treated as a definitive model error.

## Manual Audit Checklist

- [ ] correct update-required signal
- [ ] questionable
- [ ] mapping issue
- [ ] model issue
- [ ] ambiguous case
