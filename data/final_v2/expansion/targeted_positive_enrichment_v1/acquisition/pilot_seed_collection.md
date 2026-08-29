# DocGuard Real PR Seed Collector Report

This report summarizes neutral repo-based sampling of merged public GitHub PRs.

The collector does not assign gold labels and does not decide whether documentation should be updated.
It only creates seed PR URLs for the later candidate builder and manual validation workflow.

- Repositories scanned: `11`
- Seeds accepted: `1200`
- Rejected/skipped PRs: `865`
- Acquisition status: `complete`
- Requirements satisfied: `True`
- Target observed/requested: `1200` / `1200`
- Target deficit: `0`
- Minimum language deficits: `{}`
- Collector bucket counts: `{'code_only': 938, 'code_and_docs': 156, 'code_only_tests_or_fixtures': 106}`
- Language hint counts: `{'': 1200}`
- Repository counts per language: `{'': 11}`
- Candidate bucket counts per language: `{'': {'code_only': 938, 'code_and_docs': 156, 'code_only_tests_or_fixtures': 106}}`
- Reject reason counts: `{'not_merged': 541, 'other_or_binary_only_excluded': 252, 'docs_only_excluded': 47, 'fetch_pr_files_failed': 3, 'too_many_changed_files': 21, 'too_large_patch': 1}`

## Methodological Boundary

- This is real public GitHub PR sampling.
- No synthetic examples are generated.
- No final labels are assigned here.
- `collector_bucket` is audit metadata for balancing and review planning, not a model label.
- Final evaluation must use only the safe fields produced later by the candidate builder.

## Accepted Seeds

| PR | Repository | Bucket | Language hint | Title |
| --- | --- | --- | --- | --- |
| https://github.com/godotengine/godot/pull/117999 | `godotengine/godot` | `code_only` | `` | DDS: Fix loading 3D textures with mipmaps |
| https://github.com/godotengine/godot/pull/122963 | `godotengine/godot` | `code_only` | `` | [3.x] Fix some UB / uninitialized vars |
| https://github.com/godotengine/godot/pull/122945 | `godotengine/godot` | `code_only` | `` | Fix duplicate Toggle Comment context option |
| https://github.com/godotengine/godot/pull/122931 | `godotengine/godot` | `code_only` | `` | Add shader uniform hints `no_storage` and `no_editor` |
| https://github.com/godotengine/godot/pull/121940 | `godotengine/godot` | `code_only` | `` | Fix crash when setting the root Viewport's World3D to null |
| https://github.com/godotengine/godot/pull/122950 | `godotengine/godot` | `code_only` | `` | Fix deprecated build after dock changes |
| https://github.com/godotengine/godot/pull/122919 | `godotengine/godot` | `code_only` | `` | Fix GroupsEditor localization problems |
| https://github.com/godotengine/godot/pull/122863 | `godotengine/godot` | `code_only` | `` | Further improve resource load errors by using more specific macros |
| https://github.com/godotengine/godot/pull/122947 | `godotengine/godot` | `code_only` | `` | Make dock color and spacing closer to 4.7 |
| https://github.com/godotengine/godot/pull/121920 | `godotengine/godot` | `code_only` | `` | Add support for metadata in text scenes |
| https://github.com/godotengine/godot/pull/121999 | `godotengine/godot` | `code_only` | `` | FIX: RichTextLabel - Maintain proportional scroll position on resize |
| https://github.com/godotengine/godot/pull/122739 | `godotengine/godot` | `code_only` | `` | Improve various dynamic method usages |
| https://github.com/godotengine/godot/pull/122895 | `godotengine/godot` | `code_only` | `` | Fix 3D editor visibility problems |
| https://github.com/godotengine/godot/pull/122893 | `godotengine/godot` | `code_only` | `` | Fix AssetStore crash in Project Manager |
| https://github.com/godotengine/godot/pull/122878 | `godotengine/godot` | `code_only` | `` | Improve dock tab focus |
| https://github.com/godotengine/godot/pull/118236 | `godotengine/godot` | `code_only` | `` | Make `JoltContactListener3D` lockless |
| https://github.com/godotengine/godot/pull/122903 | `godotengine/godot` | `code_only` | `` | Make main screen dock colors more readable |
| https://github.com/godotengine/godot/pull/122851 | `godotengine/godot` | `code_only` | `` | Rename `GDType::Property` to `Member`, and `SETGET` to `PROPERTY`. |
| https://github.com/godotengine/godot/pull/122924 | `godotengine/godot` | `code_only` | `` | Suppress item selection events when updating script outline. |
| https://github.com/godotengine/godot/pull/122403 | `godotengine/godot` | `code_only` | `` | Update Android distribution identifiers |
| https://github.com/godotengine/godot/pull/121937 | `godotengine/godot` | `code_only` | `` | Add ClassDB binding for `TEXTURE_SLICE_2D_ARRAY` |
| https://github.com/godotengine/godot/pull/122935 | `godotengine/godot` | `code_only` | `` | Fix editor hanging when a GDExtension library is missing for the platform |
| https://github.com/godotengine/godot/pull/115426 | `godotengine/godot` | `code_only` | `` | Implement multi-bounce ambient occlusion approximation |
| https://github.com/godotengine/godot/pull/120610 | `godotengine/godot` | `code_only` | `` | Add global option to Copy/ConvertTransformModifier for reference bone |
| https://github.com/godotengine/godot/pull/120812 | `godotengine/godot` | `code_only` | `` | [3.x] Replace `LocalVector.operator Vector` with `Vector(Span)` constructor. |
| https://github.com/godotengine/godot/pull/105791 | `godotengine/godot` | `code_only` | `` | Add the ability to cancel pan/zoom/orbit navigation |
| https://github.com/godotengine/godot/pull/122736 | `godotengine/godot` | `code_only` | `` | Clear translation domains when switching to English |
| https://github.com/godotengine/godot/pull/122879 | `godotengine/godot` | `code_only` | `` | Fix local scale application in AnimationMixer |
| https://github.com/godotengine/godot/pull/113429 | `godotengine/godot` | `code_only` | `` | Implement texture mip-level streaming |
| https://github.com/godotengine/godot/pull/104456 | `godotengine/godot` | `code_only` | `` | Make "Show Node in Tree" button more user friendly |
| https://github.com/godotengine/godot/pull/122884 | `godotengine/godot` | `code_only` | `` | Fix main screen container index on Android |
| https://github.com/godotengine/godot/pull/122883 | `godotengine/godot` | `code_only` | `` | NoisePreview: Fix preview not updaing after "3D" toggle change |
| https://github.com/godotengine/godot/pull/122825 | `godotengine/godot` | `code_only` | `` | [Windows] Process all `WM_(NC)MOUSEMOVE` messages when touch screen/pen input is detected. |
| https://github.com/godotengine/godot/pull/121080 | `godotengine/godot` | `code_only` | `` | Clean and simplify `2D` toolbar |
| https://github.com/godotengine/godot/pull/122782 | `godotengine/godot` | `code_only` | `` | visionOS: Implement additional visionOS 26+ features |
| https://github.com/godotengine/godot/pull/122786 | `godotengine/godot` | `code_only` | `` | Fix issue where certain types could not be edited from remote or multi-node edit. |
| https://github.com/godotengine/godot/pull/122848 | `godotengine/godot` | `code_only` | `` | Add Information and Frame Time panels to the 2D editor |
| https://github.com/godotengine/godot/pull/121833 | `godotengine/godot` | `code_only` | `` | GDScript: Disallow strings as comments |
| https://github.com/godotengine/godot/pull/120942 | `godotengine/godot` | `code_only` | `` | Speed up removing many child nodes |
| https://github.com/godotengine/godot/pull/121629 | `godotengine/godot` | `code_only` | `` | `LocalVector::push_back` by const ref for complex types where no resize |
| https://github.com/godotengine/godot/pull/122784 | `godotengine/godot` | `code_only` | `` | Resource format text: Replace all instances of `_printerr` with `ERR_PRINT` directly |
| https://github.com/godotengine/godot/pull/47054 | `godotengine/godot` | `code_only` | `` | Allow disabling 2D when compiling export templates |
| https://github.com/godotengine/godot/pull/122831 | `godotengine/godot` | `code_only` | `` | Fix uninitialized `DockLayout` in `EditorDock` |
| https://github.com/godotengine/godot/pull/122802 | `godotengine/godot` | `code_only` | `` | Add EditorDock property for switching main screen |
| https://github.com/godotengine/godot/pull/115039 | `godotengine/godot` | `code_only` | `` | Add cursor overrides for 2D shape editor |
| https://github.com/godotengine/godot/pull/122656 | `godotengine/godot` | `code_only` | `` | Move compatibility methods maps from `ClassDB` to `GDType` |
| https://github.com/godotengine/godot/pull/119638 | `godotengine/godot` | `code_only` | `` | Fix missing "Clear Inheritance" and "Open in Editor" context menu buttons in unsaved inherited scene root |
| https://github.com/godotengine/godot/pull/122618 | `godotengine/godot` | `code_only` | `` | Lazy Editor Setting Saving |
| https://github.com/godotengine/godot/pull/122829 | `godotengine/godot` | `code_only` | `` | Fix memory leak of a `ScannedDirectory` instance in `EditorFileSystem` |
| https://github.com/godotengine/godot/pull/122841 | `godotengine/godot` | `code_only` | `` | Fix divide by zero in scale check in RenderGeometryInstanceBase |
| https://github.com/godotengine/godot/pull/117938 | `godotengine/godot` | `code_and_docs` | `` | Implement Feral GameMode integration on Linux |
| https://github.com/godotengine/godot/pull/122751 | `godotengine/godot` | `code_only` | `` | Simplify `GDType` by storing all properties in a single unified map. Save ~12mb runtime RAM |
| https://github.com/godotengine/godot/pull/120009 | `godotengine/godot` | `code_only` | `` | Don't force power-of-2 resolution for VRAM-compressed layered textures |
| https://github.com/godotengine/godot/pull/119668 | `godotengine/godot` | `code_only` | `` | Remove alignment check during astc decompression |
| https://github.com/godotengine/godot/pull/120400 | `godotengine/godot` | `code_only` | `` | Remove dead `RA to RG` conversion code from TextureStorage |
| https://github.com/godotengine/godot/pull/122703 | `godotengine/godot` | `code_only` | `` | Betsy: Optimize and improve for certain source image formats |
| https://github.com/godotengine/godot/pull/121147 | `godotengine/godot` | `code_only` | `` | Do not warn about unsupported RGB texture formats |
| https://github.com/godotengine/godot/pull/63345 | `godotengine/godot` | `code_only` | `` | Cleanup RendererSceneRender::GeometryInstance |
| https://github.com/godotengine/godot/pull/118789 | `godotengine/godot` | `code_only` | `` | Add AnimationNodeObservers for signaling animation events |
| https://github.com/godotengine/godot/pull/122613 | `godotengine/godot` | `code_only` | `` | CI: Pass GitHub Action prek diffs via `--from-ref` |
| https://github.com/godotengine/godot/pull/122248 | `godotengine/godot` | `code_only` | `` | Metal,XR: Fix extension texture creation and API usage |
| https://github.com/godotengine/godot/pull/113051 | `godotengine/godot` | `code_only` | `` | Change main screen plugins into docks |
| https://github.com/godotengine/godot/pull/122773 | `godotengine/godot` | `code_only` | `` | Add missing `_printerr()`s in error handlers |
| https://github.com/godotengine/godot/pull/122279 | `godotengine/godot` | `code_only` | `` | Move `ScriptLanguage::validate` to `EditorLanguage` |
| https://github.com/godotengine/godot/pull/117438 | `godotengine/godot` | `code_only` | `` | GDScript: Reduce memory overhead from hot reloading |
| https://github.com/godotengine/godot/pull/122806 | `godotengine/godot` | `code_only` | `` | Add missing `<memory>` includes in SVG module |
| https://github.com/godotengine/godot/pull/122725 | `godotengine/godot` | `code_only` | `` | [Linux] Don't send an octet-stream MIME type for the "All Files" filter |
| https://github.com/godotengine/godot/pull/122667 | `godotengine/godot` | `code_only` | `` | Fix handle mode being dropped for bezier curves in track editor |
| https://github.com/godotengine/godot/pull/122767 | `godotengine/godot` | `code_only` | `` | Fix selected bezier track renders black when filtered out |
| https://github.com/godotengine/godot/pull/122809 | `godotengine/godot` | `code_only` | `` | List monitor resolutions and refresh rates in editor Copy System Info |
| https://github.com/godotengine/godot/pull/99404 | `godotengine/godot` | `code_only` | `` | Implement VisualShader Node Groups/Subgraphs |
| https://github.com/godotengine/godot/pull/122785 | `godotengine/godot` | `code_only` | `` | Send Nodes instead of NodePaths in SceneTreeDock signals |
| https://github.com/godotengine/godot/pull/120609 | `godotengine/godot` | `code_only` | `` | Add `BoneSpreader3D` & `skin_scale` property to Bone in Skeleton3D |
| https://github.com/godotengine/godot/pull/122559 | `godotengine/godot` | `code_only` | `` | Editor: Add visionOS templates to download manager |
| https://github.com/godotengine/godot/pull/122675 | `godotengine/godot` | `code_only` | `` | renderer: texture is used for atomic operations, so set atomic bit |
| https://github.com/godotengine/godot/pull/122646 | `godotengine/godot` | `code_only` | `` | GDScript: Fix reflection for `_init()` and `_static_init()` |
| https://github.com/godotengine/godot/pull/121063 | `godotengine/godot` | `code_only` | `` | Add search to animations menu in AnimationNodeStateMachineEditor |
| https://github.com/godotengine/godot/pull/121849 | `godotengine/godot` | `code_only` | `` | Automate Android & Java SDK setup |
| https://github.com/godotengine/godot/pull/122574 | `godotengine/godot` | `code_only` | `` | Fix and add more scroll hints in the editor |
| https://github.com/godotengine/godot/pull/122719 | `godotengine/godot` | `code_only` | `` | Reduce `Search Help` update threshold |
| https://github.com/godotengine/godot/pull/122768 | `godotengine/godot` | `code_only` | `` | Use `SIZE_SHRINK_BEGIN` instead of `0` in `set_*_size_flags` calls |
| https://github.com/godotengine/godot/pull/122760 | `godotengine/godot` | `code_only` | `` | Fix empty click context options for file list |
| https://github.com/godotengine/godot/pull/118309 | `godotengine/godot` | `code_only` | `` | Add `SIZE_MAXIMIZE` size flag |
| https://github.com/godotengine/godot/pull/122402 | `godotengine/godot` | `code_only` | `` | [TextServer] Shape adjacent spans with same font/language properties as one |
| https://github.com/godotengine/godot/pull/118383 | `godotengine/godot` | `code_only` | `` | Optimize performance when selecting and dragging multiple keys |
| https://github.com/godotengine/godot/pull/122776 | `godotengine/godot` | `code_only` | `` | CI: Bump SCons version [4.10.1 → 4.11.0] |
| https://github.com/godotengine/godot/pull/122756 | `godotengine/godot` | `code_only` | `` | LSP: Display warning code in diagnostic "code" field instead of message |
| https://github.com/godotengine/godot/pull/121532 | `godotengine/godot` | `code_only` | `` | Fix error when creating new scene |
| https://github.com/godotengine/godot/pull/107154 | `godotengine/godot` | `code_only` | `` | Always use a dark background for 3D editor overlays even with light theme |
| https://github.com/godotengine/godot/pull/122634 | `godotengine/godot` | `code_only_tests_or_fixtures` | `` | Update `argument_options.tscn` to load `AnimationPlayer` libraries in the most recent format |
| https://github.com/godotengine/godot/pull/122759 | `godotengine/godot` | `code_only` | `` | Remove unused `AcceptDialog` in `ScriptEditorDebugger` |
| https://github.com/godotengine/godot/pull/122012 | `godotengine/godot` | `code_only` | `` | Remove unnecessary include in `gdscript_function.h` |
| https://github.com/godotengine/godot/pull/122669 | `godotengine/godot` | `code_only` | `` | Fix Cinematic Preview and Lock View Rotation labels on light theme in the 3D editor |
| https://github.com/godotengine/godot/pull/118073 | `godotengine/godot` | `code_only` | `` | Add buffer device address support to D3D12 driver. |
| https://github.com/godotengine/godot/pull/120891 | `godotengine/godot` | `code_only` | `` | GDScript: Fix attribute access falsely counting as local usage |
| https://github.com/godotengine/godot/pull/122639 | `godotengine/godot` | `code_only` | `` | [3.x] [iOS] Fix x86_64 simulator build. |
| https://github.com/godotengine/godot/pull/121923 | `godotengine/godot` | `code_only` | `` | Core: Remove assignment in Variant Object destructor |
| https://github.com/godotengine/godot/pull/119306 | `godotengine/godot` | `code_only` | `` | Fix `BlendSpace2D` editor toolbar overflow |
| https://github.com/godotengine/godot/pull/122465 | `godotengine/godot` | `code_only` | `` | Replace `Vector` with `LocalVector` in GDScript AST |
| https://github.com/godotengine/godot/pull/105701 | `godotengine/godot` | `code_only` | `` | Implement DrawableTextures |
| https://github.com/godotengine/godot/pull/122676 | `godotengine/godot` | `code_only` | `` | Add Windows Arm64 COFF headers to `ResourceImporterOBJ` |
| https://github.com/godotengine/godot/pull/122596 | `godotengine/godot` | `code_only` | `` | Move property maps from `ClassDB` to `GDType`. Accelerate `Object` property access 1.6x |
| https://github.com/godotengine/godot/pull/122700 | `godotengine/godot` | `code_and_docs` | `` | [3.6] Cherry-picks for the 3.6 branch (future 3.6.3) - 3rd batch |
| https://github.com/godotengine/godot/pull/122647 | `godotengine/godot` | `code_only` | `` | [3.x] Add internal `get_entropy()` javascript function for web build |
| https://github.com/godotengine/godot/pull/122624 | `godotengine/godot` | `code_only` | `` | Show a proper error when there is invalid input in `EditorPropertyNodePath` |
| https://github.com/godotengine/godot/pull/122107 | `godotengine/godot` | `code_only` | `` | Fix wrong common class logic for inspected remote nodes |
| https://github.com/godotengine/godot/pull/122693 | `godotengine/godot` | `code_only` | `` | Make `LightmapData` smaller and manually pack `uses_lightmap_specular` into element info. |
| https://github.com/godotengine/godot/pull/122690 | `godotengine/godot` | `code_only` | `` | [Core]: Make `get_object_class_name_or_empty` return reference for use in typed containers |
| https://github.com/godotengine/godot/pull/122659 | `godotengine/godot` | `code_only` | `` | Add replace preview to Find in Files |
| https://github.com/godotengine/godot/pull/122579 | `godotengine/godot` | `code_only` | `` | Fix: Scene importer does not correctly load custom global classes from its Root Type property |
| https://github.com/ethereum/go-ethereum/pull/35589 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/eth: avoid announcing sparse blob txs to legacy peers |
| https://github.com/ethereum/go-ethereum/pull/35389 | `ethereum/go-ethereum` | `code_only` | `` | cmd/devp2p/internal/ethtest: add eth/71 (EIP-8159) tests |
| https://github.com/ethereum/go-ethereum/pull/35554 | `ethereum/go-ethereum` | `code_only` | `` | eth: return iterator errors from debug_storageRangeAt |
| https://github.com/ethereum/go-ethereum/pull/35592 | `ethereum/go-ethereum` | `code_only` | `` | eth/gasestimator: return used gas for plain transfer estimates |
| https://github.com/ethereum/go-ethereum/pull/35583 | `ethereum/go-ethereum` | `code_only` | `` | eth/tracers: make debug_traceCall block parameter optional |
| https://github.com/ethereum/go-ethereum/pull/35574 | `ethereum/go-ethereum` | `code_only_tests_or_fixtures` | `` | tests: compare baseFeePerGas with nil-safe Cmp |
| https://github.com/ethereum/go-ethereum/pull/33740 | `ethereum/go-ethereum` | `code_only` | `` | cmd/geth: add subcommand for offline binary tree conversion |
| https://github.com/ethereum/go-ethereum/pull/35591 | `ethereum/go-ethereum` | `code_and_docs` | `` | beacon, cmd, core, params: remove the holesky testnet |
| https://github.com/ethereum/go-ethereum/pull/35367 | `ethereum/go-ethereum` | `code_only` | `` | core/txpool: add blocked transaction size cap |
| https://github.com/ethereum/go-ethereum/pull/35593 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/eth, eth/downloader: reject empty partial receipt responses |
| https://github.com/ethereum/go-ethereum/pull/35581 | `ethereum/go-ethereum` | `code_only` | `` | core/vm, cmd/geth, tests: remove EIP-7610 implementation |
| https://github.com/ethereum/go-ethereum/pull/35421 | `ethereum/go-ethereum` | `code_only` | `` | version: release v1.17.5 |
| https://github.com/ethereum/go-ethereum/pull/35575 | `ethereum/go-ethereum` | `code_only` | `` | core: enforce block gas limit in parallel block execution |
| https://github.com/ethereum/go-ethereum/pull/35580 | `ethereum/go-ethereum` | `code_only` | `` | beacon/engine, eth/catalyst: fix hive failure |
| https://github.com/ethereum/go-ethereum/pull/35070 | `ethereum/go-ethereum` | `code_only` | `` | eth/filters: reject GetLogs range with begin > 0 and end == 0 |
| https://github.com/ethereum/go-ethereum/pull/35429 | `ethereum/go-ethereum` | `code_only` | `` | core/txpool/blobpool: lock lookup when logging corrupt tx blobs |
| https://github.com/ethereum/go-ethereum/pull/35573 | `ethereum/go-ethereum` | `code_only` | `` | .gitea, cmd: deprecate golang 1.24 |
| https://github.com/ethereum/go-ethereum/pull/35512 | `ethereum/go-ethereum` | `code_only` | `` | core: honor ExecuteConfig.EnableTracer for the EVM-level tracing hooks |
| https://github.com/ethereum/go-ethereum/pull/35537 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/eth: fix deadlock when re-requesting partial receipts |
| https://github.com/ethereum/go-ethereum/pull/35578 | `ethereum/go-ethereum` | `code_only` | `` | common/lru, core/vm: count entry overhead in the precompile cache budget |
| https://github.com/ethereum/go-ethereum/pull/35572 | `ethereum/go-ethereum` | `code_only` | `` | core, eth: improve the blob fetcher |
| https://github.com/ethereum/go-ethereum/pull/35576 | `ethereum/go-ethereum` | `code_only` | `` | rpc: reject null for required arguments |
| https://github.com/ethereum/go-ethereum/pull/35518 | `ethereum/go-ethereum` | `code_only` | `` | rpc, eth/catalyst: optimize json decode |
| https://github.com/ethereum/go-ethereum/pull/33719 | `ethereum/go-ethereum` | `code_only` | `` | common/lru: add metered lru cache variant |
| https://github.com/ethereum/go-ethereum/pull/34770 | `ethereum/go-ethereum` | `code_only` | `` | cmd/devp2p: add more hive discv5 coverage |
| https://github.com/ethereum/go-ethereum/pull/35551 | `ethereum/go-ethereum` | `code_only` | `` | core/rawdb: fix head truncation below a diverged tail group |
| https://github.com/ethereum/go-ethereum/pull/35553 | `ethereum/go-ethereum` | `code_only` | `` | internal/ethapi: skip unconfigured forks when computing next fork in eth_config |
| https://github.com/ethereum/go-ethereum/pull/35552 | `ethereum/go-ethereum` | `code_only` | `` | core/txpool/blobpool: do not warn when a blob tx is swapped out by its signer |
| https://github.com/ethereum/go-ethereum/pull/35564 | `ethereum/go-ethereum` | `code_only` | `` | core/txpool/locals: check close error before replacing journal |
| https://github.com/ethereum/go-ethereum/pull/35533 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/snap: parallelize the state response processing |
| https://github.com/ethereum/go-ethereum/pull/35543 | `ethereum/go-ethereum` | `code_only` | `` | core/txpool/blobpool: speed up serving pre eth/72 peers |
| https://github.com/ethereum/go-ethereum/pull/35261 | `ethereum/go-ethereum` | `code_only` | `` | core/vm: add access cost check |
| https://github.com/ethereum/go-ethereum/pull/33773 | `ethereum/go-ethereum` | `code_only` | `` | miner: add OpenTelemetry spans for block building path |
| https://github.com/ethereum/go-ethereum/pull/35542 | `ethereum/go-ethereum` | `code_only_tests_or_fixtures` | `` | p2p/discover: try to fix TestUDPv5_lookupE2E by using SetFallbackUDP |
| https://github.com/ethereum/go-ethereum/pull/35529 | `ethereum/go-ethereum` | `code_only` | `` | crypto/kzg4844: add RecoverCells with systematic fast path |
| https://github.com/ethereum/go-ethereum/pull/35514 | `ethereum/go-ethereum` | `code_only` | `` | core, eth/catalyst, beacon/engine: update for glam8 |
| https://github.com/ethereum/go-ethereum/pull/35528 | `ethereum/go-ethereum` | `code_only` | `` | crypto/kzg4844: add BlobsFromDataCells for zero-KZG blob reconstruction |
| https://github.com/ethereum/go-ethereum/pull/35544 | `ethereum/go-ethereum` | `code_only` | `` | eth: return error instead of panicking on debug_executionWitness |
| https://github.com/ethereum/go-ethereum/pull/35526 | `ethereum/go-ethereum` | `code_only` | `` | common/lru, core/vm: count key bytes against the precompile cache budget |
| https://github.com/ethereum/go-ethereum/pull/35473 | `ethereum/go-ethereum` | `code_only` | `` | core/vm: key the precompile cache on the input instead of its hash |
| https://github.com/ethereum/go-ethereum/pull/35524 | `ethereum/go-ethereum` | `code_only` | `` | eth/fetcher: validate announced blob tx size against announcer's protocol version |
| https://github.com/ethereum/go-ethereum/pull/35509 | `ethereum/go-ethereum` | `code_only` | `` | eth: don't read a blob pool that is still initialising |
| https://github.com/ethereum/go-ethereum/pull/35498 | `ethereum/go-ethereum` | `code_only` | `` | core/state: unset the block-level accessList in Finalise  |
| https://github.com/ethereum/go-ethereum/pull/35510 | `ethereum/go-ethereum` | `code_only` | `` | build, internal: add retry mechanism in package uploading |
| https://github.com/ethereum/go-ethereum/pull/35433 | `ethereum/go-ethereum` | `code_only` | `` | eth/syncer: only synthesize finalized/safe markers with an explicit sync target |
| https://github.com/ethereum/go-ethereum/pull/35520 | `ethereum/go-ethereum` | `code_only` | `` | cmd, core, eth, internal: deprecate state sizer |
| https://github.com/ethereum/go-ethereum/pull/35519 | `ethereum/go-ethereum` | `code_only` | `` | eth/catalyst: make `headBlock` reorging to `finalized` possible |
| https://github.com/ethereum/go-ethereum/pull/35515 | `ethereum/go-ethereum` | `code_only` | `` | eth/downloader: don't signal sync startup before fetchers register for cancellation |
| https://github.com/ethereum/go-ethereum/pull/33943 | `ethereum/go-ethereum` | `code_only` | `` | miner: avoid unnecessary work after payload resolution |
| https://github.com/ethereum/go-ethereum/pull/33869 | `ethereum/go-ethereum` | `code_only` | `` | core/vm: Switch to branchless normalization and extend EXCHANGE |
| https://github.com/ethereum/go-ethereum/pull/33521 | `ethereum/go-ethereum` | `code_only` | `` | eth/catalyst: add initial OpenTelemetry tracing for newPayload |
| https://github.com/ethereum/go-ethereum/pull/33780 | `ethereum/go-ethereum` | `code_only` | `` | internal/telemetry: don't create internal spans without parents |
| https://github.com/ethereum/go-ethereum/pull/33787 | `ethereum/go-ethereum` | `code_only_tests_or_fixtures` | `` | core/vm: 8024 tests should enforce explicit errors |
| https://github.com/ethereum/go-ethereum/pull/33614 | `ethereum/go-ethereum` | `code_only` | `` | core/vm: update EIP-8024 - Missing immediate byte is now treated as 0x00 |
| https://github.com/ethereum/go-ethereum/pull/33599 | `ethereum/go-ethereum` | `code_only` | `` | rpc: extract OpenTelemetry trace context from request headers |
| https://github.com/ethereum/go-ethereum/pull/33573 | `ethereum/go-ethereum` | `code_only` | `` | core/rawdb: skip missing block bodies during tx unindexing |
| https://github.com/ethereum/go-ethereum/pull/33452 | `ethereum/go-ethereum` | `code_only` | `` | rpc: add OpenTelemetry tracing for JSON-RPC calls |
| https://github.com/ethereum/go-ethereum/pull/33095 | `ethereum/go-ethereum` | `code_only` | `` | core/vm: implement EIP-8024 |
| https://github.com/ethereum/go-ethereum/pull/34626 | `ethereum/go-ethereum` | `code_only` | `` | core, eth/protocols/snap, eth/downloader: snap/2 sync logic |
| https://github.com/ethereum/go-ethereum/pull/35501 | `ethereum/go-ethereum` | `code_only_tests_or_fixtures` | `` | eth/catalyst: pass targetGasLimit through in testing_buildBlockV1 |
| https://github.com/ethereum/go-ethereum/pull/35423 | `ethereum/go-ethereum` | `code_only` | `` | core/rawdb: retain BAL in bad blocks |
| https://github.com/ethereum/go-ethereum/pull/35477 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/snap: add tests and comments |
| https://github.com/ethereum/go-ethereum/pull/35490 | `ethereum/go-ethereum` | `code_only` | `` | core: revert block validation optimization |
| https://github.com/ethereum/go-ethereum/pull/35497 | `ethereum/go-ethereum` | `code_only` | `` | core/vm, params, tests: update gas price parameters |
| https://github.com/ethereum/go-ethereum/pull/35493 | `ethereum/go-ethereum` | `code_only` | `` | eth/downloader: don't log stale access list reservations as errors |
| https://github.com/ethereum/go-ethereum/pull/35469 | `ethereum/go-ethereum` | `code_only` | `` | graphql: add slotNumber to block schema |
| https://github.com/ethereum/go-ethereum/pull/35486 | `ethereum/go-ethereum` | `code_only` | `` | core, params: rename RegularPerAuthBaseCost to ExecutionPerAuthBaseCost |
| https://github.com/ethereum/go-ethereum/pull/35167 | `ethereum/go-ethereum` | `code_only` | `` | accounts/external: forward blob fee cap to external signer |
| https://github.com/ethereum/go-ethereum/pull/35471 | `ethereum/go-ethereum` | `code_only` | `` | core/rawdb: verify canonical hash before reading ancient BAL |
| https://github.com/ethereum/go-ethereum/pull/35463 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/snap: advance catch-up pivot after batch commit |
| https://github.com/ethereum/go-ethereum/pull/35386 | `ethereum/go-ethereum` | `code_only` | `` | eth/downloader: implement BAL downloading |
| https://github.com/ethereum/go-ethereum/pull/35392 | `ethereum/go-ethereum` | `code_only` | `` | eth/catalyst: use IsAmsterdam when sealing simulated beacon blocks |
| https://github.com/ethereum/go-ethereum/pull/35376 | `ethereum/go-ethereum` | `code_only` | `` | cmd/geth: release iterator in checkStateContent |
| https://github.com/ethereum/go-ethereum/pull/35465 | `ethereum/go-ethereum` | `code_only` | `` | core: fail fast on transaction error in parallel block execution |
| https://github.com/ethereum/go-ethereum/pull/35345 | `ethereum/go-ethereum` | `code_only` | `` | accounts/abi: set stringKind for contract-typed arguments |
| https://github.com/ethereum/go-ethereum/pull/35302 | `ethereum/go-ethereum` | `code_only` | `` | cmd/geth: return storage slot count from traverseStorage |
| https://github.com/ethereum/go-ethereum/pull/35461 | `ethereum/go-ethereum` | `code_only` | `` | core: surface database errors in parallel block execution |
| https://github.com/ethereum/go-ethereum/pull/35462 | `ethereum/go-ethereum` | `code_only` | `` | eth/downloader: hold pivotLock when reading pivot header in progress report |
| https://github.com/ethereum/go-ethereum/pull/35464 | `ethereum/go-ethereum` | `code_only` | `` | core: genesis slot number parsing |
| https://github.com/ethereum/go-ethereum/pull/35460 | `ethereum/go-ethereum` | `code_only` | `` | common/mclock: rename symbol to remove conflicts with other languages |
| https://github.com/ethereum/go-ethereum/pull/35442 | `ethereum/go-ethereum` | `code_only` | `` | eth/syncer: fix nil deref when the target block is missing |
| https://github.com/ethereum/go-ethereum/pull/35459 | `ethereum/go-ethereum` | `code_only` | `` | core, core/state: fix preimage recording in parallel block execution |
| https://github.com/ethereum/go-ethereum/pull/35443 | `ethereum/go-ethereum` | `code_only` | `` | core: attach the precompile cache in parallel block execution |
| https://github.com/ethereum/go-ethereum/pull/35457 | `ethereum/go-ethereum` | `code_only` | `` | core, eth: rename regular gas to execution gas |
| https://github.com/ethereum/go-ethereum/pull/35454 | `ethereum/go-ethereum` | `code_only` | `` | core: update 2780 and 8038 parameters |
| https://github.com/ethereum/go-ethereum/pull/35458 | `ethereum/go-ethereum` | `code_only` | `` | cmd, consensus, core, miner: update 7997 |
| https://github.com/ethereum/go-ethereum/pull/35441 | `ethereum/go-ethereum` | `code_only` | `` | core: fix data race on the BLOCKHASH cache in parallel block execution |
| https://github.com/ethereum/go-ethereum/pull/35439 | `ethereum/go-ethereum` | `code_only` | `` | core/txpool/blobpool: fall back to pool in GetCells for blob-mode cache entries |
| https://github.com/ethereum/go-ethereum/pull/35316 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols/snap: purge stale sync state when snap sync v2 is re-enabled |
| https://github.com/ethereum/go-ethereum/pull/35388 | `ethereum/go-ethereum` | `code_only` | `` | core, core/vm: precompile result caching  |
| https://github.com/ethereum/go-ethereum/pull/35400 | `ethereum/go-ethereum` | `code_only` | `` | triedb/pathdb: report nothing recoverable during state sync |
| https://github.com/ethereum/go-ethereum/pull/35404 | `ethereum/go-ethereum` | `code_only` | `` | core: coordinate the state prefetcher with block processing |
| https://github.com/ethereum/go-ethereum/pull/35264 | `ethereum/go-ethereum` | `code_only` | `` | core: implement parallel block execution with BAL |
| https://github.com/ethereum/go-ethereum/pull/35428 | `ethereum/go-ethereum` | `code_only` | `` | eth/protocols: fix Cells/GetCells RLP encoding |
| https://github.com/ethereum/go-ethereum/pull/35427 | `ethereum/go-ethereum` | `code_only` | `` | miner: don't seal block if a db error occurred |
| https://github.com/ethereum/go-ethereum/pull/35425 | `ethereum/go-ethereum` | `code_only` | `` | version: start v1.17.6 release cycle |
| https://github.com/ethereum/go-ethereum/pull/35406 | `ethereum/go-ethereum` | `code_only` | `` | core: fix tx size calculation |
| https://github.com/ethereum/go-ethereum/pull/35405 | `ethereum/go-ethereum` | `code_only` | `` | eth/downloader: hold pivotLock when marking pivot committed |
| https://github.com/ethereum/go-ethereum/pull/35408 | `ethereum/go-ethereum` | `code_only` | `` | node: check authorization header case-insensitivity |
| https://github.com/ethereum/go-ethereum/pull/35407 | `ethereum/go-ethereum` | `code_only` | `` | cmd/utils: skip memory-limit sanitize when total memory is unknown |
| https://github.com/ethereum/go-ethereum/pull/35396 | `ethereum/go-ethereum` | `code_only` | `` | core: emit the tracing frames with EIP-2780 manner |
| https://github.com/ethereum/go-ethereum/pull/35391 | `ethereum/go-ethereum` | `code_only` | `` | eth/catalyst: allow reorg depth equal to maxReorgDepth |
| https://github.com/ethereum/go-ethereum/pull/35403 | `ethereum/go-ethereum` | `code_only` | `` | core: optimize block validation |
| https://github.com/ethereum/go-ethereum/pull/35399 | `ethereum/go-ethereum` | `code_only` | `` | eth/fetcher: clear partial map when dropping last waitlist peer |
| https://github.com/ethereum/go-ethereum/pull/35402 | `ethereum/go-ethereum` | `code_only` | `` | eth/downloader: disable snap mode after committing pivot block |
| https://github.com/ethereum/go-ethereum/pull/35212 | `ethereum/go-ethereum` | `code_only` | `` | core: implement EIP-2780 |
| https://github.com/ethereum/go-ethereum/pull/35216 | `ethereum/go-ethereum` | `code_only` | `` | core: implement EIP-8038 |
| https://github.com/ethereum/go-ethereum/pull/35363 | `ethereum/go-ethereum` | `code_only` | `` | cmd: add gogc flag |
| https://github.com/ethereum/go-ethereum/pull/35393 | `ethereum/go-ethereum` | `code_only` | `` | eth/fetcher: count unique hashes in blob queueing metric |
| https://github.com/ethereum/go-ethereum/pull/35364 | `ethereum/go-ethereum` | `code_only_tests_or_fixtures` | `` | core: improve amsterdam fork test coverage |
| https://github.com/dapr/dapr/pull/10431 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] workflow: allow meta watch on stalled workflow |
| https://github.com/dapr/dapr/pull/10424 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | [Backport release-1.18] Integration: fix retention-job test race |
| https://github.com/dapr/dapr/pull/10428 | `dapr/dapr` | `code_and_docs` | `` | workflow: allow meta watch on stalled workflow |
| https://github.com/dapr/dapr/pull/10307 | `dapr/dapr` | `code_only` | `` | workflows: fix lost completion rendezvous |
| https://github.com/dapr/dapr/pull/10380 | `dapr/dapr` | `code_only` | `` | actors: delete timers on ownership loss |
| https://github.com/dapr/dapr/pull/10407 | `dapr/dapr` | `code_only` | `` | workflow: prevent activity double-execution across placement handoff |
| https://github.com/dapr/dapr/pull/10405 | `dapr/dapr` | `code_only` | `` | workflow: suppress stale reminder escalations for completed instances |
| https://github.com/dapr/dapr/pull/10420 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | Integration: fix retention-job test race |
| https://github.com/dapr/dapr/pull/10422 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | Integration: move CRD generation into build step |
| https://github.com/dapr/dapr/pull/10421 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | [Backport release-1.18] Integration: workflow: pin recreate-collision |
| https://github.com/dapr/dapr/pull/10419 | `dapr/dapr` | `code_only` | `` | [1.18] workflow: fix spurious failures under history signing (#10403) |
| https://github.com/dapr/dapr/pull/10349 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | Integration: workflow: pin recreate-collision |
| https://github.com/dapr/dapr/pull/10354 | `dapr/dapr` | `code_and_docs` | `` | workflow: fix mid-batch terminate |
| https://github.com/dapr/dapr/pull/10408 | `dapr/dapr` | `code_only` | `` | workflow: cancel pending work-item completions when the last worker disconnects |
| https://github.com/dapr/dapr/pull/10403 | `dapr/dapr` | `code_and_docs` | `` | workflow: fix spurious failures under history signing |
| https://github.com/dapr/dapr/pull/10415 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] Drop binary gRPC metadata from output binding component metadata |
| https://github.com/dapr/dapr/pull/10406 | `dapr/dapr` | `code_only` | `` | workflow: disable fast path when scheduler concurrency limits are configured |
| https://github.com/dapr/dapr/pull/10395 | `dapr/dapr` | `code_and_docs` | `` | Drop binary gRPC metadata from output binding component metadata |
| https://github.com/dapr/dapr/pull/10404 | `dapr/dapr` | `code_only` | `` | workflow: close fastpath fold gaps |
| https://github.com/dapr/dapr/pull/10402 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] workflow: fix parent deadlock on child instance ID collision after ContinueAsNew |
| https://github.com/dapr/dapr/pull/10400 | `dapr/dapr` | `code_and_docs` | `` | workflow: fix parent deadlock on child instance ID collision after ContinueAsNew |
| https://github.com/dapr/dapr/pull/10401 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] Retry workflow reminder creates on all transient scheduler errors |
| https://github.com/dapr/dapr/pull/10399 | `dapr/dapr` | `code_and_docs` | `` | Retry workflow reminder creates on all transient scheduler errors |
| https://github.com/dapr/dapr/pull/10396 | `dapr/dapr` | `code_only` | `` | workflow: actors: drop blocking completion-waiter paths |
| https://github.com/dapr/dapr/pull/10391 | `dapr/dapr` | `code_only` | `` | [release-1.17] fix(deps): bump x/mod to v0.40.0, etcd to v3.5.33, fasthttp to v1.70.0 |
| https://github.com/dapr/dapr/pull/10397 | `dapr/dapr` | `code_only` | `` | make k8s ns creation idempotent for the scheduler placement run |
| https://github.com/dapr/dapr/pull/10394 | `dapr/dapr` | `code_only` | `` | healthz: honour --healthz-listen-address in the healthz server |
| https://github.com/dapr/dapr/pull/10381 | `dapr/dapr` | `code_only` | `` | perf(workflow): elide no-op start trigger |
| https://github.com/dapr/dapr/pull/10384 | `dapr/dapr` | `code_only` | `` | add scheduler-placement comparison to perf tests |
| https://github.com/dapr/dapr/pull/10382 | `dapr/dapr` | `code_and_docs` | `` | integration: add clustered workflow CI job |
| https://github.com/dapr/dapr/pull/10374 | `dapr/dapr` | `code_only` | `` | feat(sentry): support jwt typing via optional typ header |
| https://github.com/dapr/dapr/pull/10379 | `dapr/dapr` | `code_only` | `` | perf(workflow): event-driven work item completion |
| https://github.com/dapr/dapr/pull/10372 | `dapr/dapr` | `code_only` | `` | perf(workflow): bounded actor residency, janitor hysteresis, scoped activity lock |
| https://github.com/dapr/dapr/pull/10370 | `dapr/dapr` | `code_and_docs` | `` | [1.16] placement table lock wedging after a slow dissemination round |
| https://github.com/dapr/dapr/pull/10365 | `dapr/dapr` | `code_only` | `` | perf(diagnostics): cache tag maps for hot-path metric records |
| https://github.com/dapr/dapr/pull/10369 | `dapr/dapr` | `code_and_docs` | `` | [1.16] Fix daprd placement reconnect after failed actor deactivation |
| https://github.com/dapr/dapr/pull/10366 | `dapr/dapr` | `code_only` | `` | perf(workflow): drop per-turn state snapshot clone, slab event marshals |
| https://github.com/dapr/dapr/pull/10348 | `dapr/dapr` | `code_only` | `` | scheduler: honor invoke cancellation, tolerate unknown job acks |
| https://github.com/dapr/dapr/pull/10294 | `dapr/dapr` | `code_only` | `` | Fix streaming service invocation connections closed mid-stream by idle-purge |
| https://github.com/dapr/dapr/pull/10345 | `dapr/dapr` | `code_only` | `` | scheduler: retry client creation instead of fatal exit |
| https://github.com/dapr/dapr/pull/10359 | `dapr/dapr` | `code_and_docs` | `` | [1.16] add in azure auth spiffee cred contrib fix |
| https://github.com/dapr/dapr/pull/10358 | `dapr/dapr` | `code_and_docs` | `` | [1.17] add in azure auth spiffee cred contrib fix |
| https://github.com/dapr/dapr/pull/10118 | `dapr/dapr` | `code_and_docs` | `` | Add spiffe source to context for all component operations |
| https://github.com/dapr/dapr/pull/10356 | `dapr/dapr` | `code_and_docs` | `` | Update Go 1.26.5 -> 1.26.6 |
| https://github.com/dapr/dapr/pull/10355 | `dapr/dapr` | `code_and_docs` | `` | workflow: fix mid-batch terminate |
| https://github.com/dapr/dapr/pull/10347 | `dapr/dapr` | `code_only` | `` | scheduler: preserve delivery seniority in the pool pending drain |
| https://github.com/dapr/dapr/pull/10344 | `dapr/dapr` | `code_only` | `` | perf: workflow: jittered exponential reminder backoff |
| https://github.com/dapr/dapr/pull/10343 | `dapr/dapr` | `code_only` | `` | scheduler: reject jobs with invalid target metadata instead of panic |
| https://github.com/dapr/dapr/pull/10342 | `dapr/dapr` | `code_only` | `` | perf: grpc: raise the pooled connection stream cap to 2048 |
| https://github.com/dapr/dapr/pull/10328 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | Integration: stale workflow reminder delivered with no actor state store |
| https://github.com/dapr/dapr/pull/10341 | `dapr/dapr` | `code_only` | `` | perf: resiliency: cache default policy template expansion |
| https://github.com/dapr/dapr/pull/10293 | `dapr/dapr` | `code_only` | `` | Workflow: cross-app operations |
| https://github.com/dapr/dapr/pull/10339 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] grpc: give the app connection realistic connect budget |
| https://github.com/dapr/dapr/pull/10336 | `dapr/dapr` | `code_and_docs` | `` | grpc: give the app connection realistic connect budget |
| https://github.com/dapr/dapr/pull/10333 | `dapr/dapr` | `code_only` | `` | Attach SVID context when doing secret resolution |
| https://github.com/dapr/dapr/pull/10334 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] workflow: ack activity-result reminders for purged instances |
| https://github.com/dapr/dapr/pull/10332 | `dapr/dapr` | `code_and_docs` | `` | workflow: ack activity-result reminders for purged instances |
| https://github.com/dapr/dapr/pull/10330 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] workflow: fix stalled workflows left unrecoverable |
| https://github.com/dapr/dapr/pull/10329 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.17] workflow: fix stalled workflows left unrecoverable |
| https://github.com/dapr/dapr/pull/10331 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] placement: report stream closure exactly once |
| https://github.com/dapr/dapr/pull/10327 | `dapr/dapr` | `code_and_docs` | `` | placement: report stream closure exactly once |
| https://github.com/dapr/dapr/pull/10326 | `dapr/dapr` | `code_and_docs` | `` | workflow: fix stalled workflows left unrecoverable |
| https://github.com/dapr/dapr/pull/10325 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] actors: allow hot reloading the actor state store |
| https://github.com/dapr/dapr/pull/10309 | `dapr/dapr` | `code_and_docs` | `` | actors: allow hot reloading the actor state store |
| https://github.com/dapr/dapr/pull/10324 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] workflows: fresh trace roots on ContinueAsNew |
| https://github.com/dapr/dapr/pull/10321 | `dapr/dapr` | `code_and_docs` | `` | workflows: fresh trace roots on ContinueAsNew |
| https://github.com/dapr/dapr/pull/10320 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] PubSub: Fix panic in HTTP delivery on non-string trace field |
| https://github.com/dapr/dapr/pull/10319 | `dapr/dapr` | `code_and_docs` | `` | PubSub: Fix panic in HTTP delivery on non-string trace field |
| https://github.com/dapr/dapr/pull/10318 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] mcpserver retry registration on failure |
| https://github.com/dapr/dapr/pull/10308 | `dapr/dapr` | `code_and_docs` | `` | mcpserver retry registration on failure |
| https://github.com/dapr/dapr/pull/10220 | `dapr/dapr` | `code_and_docs` | `` | fix(runtime): make binding OPTIONS probe timeout configurable |
| https://github.com/dapr/dapr/pull/9050 | `dapr/dapr` | `code_only` | `` | Added support for binary cloudevent |
| https://github.com/dapr/dapr/pull/10142 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | Add integration tests for stateful-history workflow delivery |
| https://github.com/dapr/dapr/pull/10303 | `dapr/dapr` | `code_and_docs` | `` | [1.16] fix(runtime): make binding OPTIONS probe timeout configurable (#10220) |
| https://github.com/dapr/dapr/pull/10301 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | e2e: drain pubsub redelivery backlog before reset |
| https://github.com/dapr/dapr/pull/10304 | `dapr/dapr` | `code_and_docs` | `` | [1.17] fix(runtime): make binding OPTIONS probe timeout configurable (#10220) |
| https://github.com/dapr/dapr/pull/10300 | `dapr/dapr` | `code_and_docs` | `` | [1.18] cherrypick fix(runtime): make binding OPTIONS probe timeout configurable (#10220) |
| https://github.com/dapr/dapr/pull/10283 | `dapr/dapr` | `code_only` | `` | workflows: remove the clustered-deployment completion rendezvous hops |
| https://github.com/dapr/dapr/pull/10232 | `dapr/dapr` | `code_only` | `` | Add appProtocol to all Dapr K8s Services |
| https://github.com/dapr/dapr/pull/10292 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] Fix jobs scheduled over HTTP without `data` failing to deliver + timezone tests |
| https://github.com/dapr/dapr/pull/10281 | `dapr/dapr` | `code_only` | `` | version-skew: fix integration tests |
| https://github.com/dapr/dapr/pull/10289 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] Workflow: Fix transient GetInstance failure |
| https://github.com/dapr/dapr/pull/10286 | `dapr/dapr` | `code_only` | `` | [Backport release-1.18] sec: bump grpc etc |
| https://github.com/dapr/dapr/pull/10251 | `dapr/dapr` | `code_and_docs` | `` | Fix jobs scheduled over HTTP without `data` failing to deliver + timezone tests |
| https://github.com/dapr/dapr/pull/10287 | `dapr/dapr` | `code_only` | `` | Remove components-contrib workflows abstraction |
| https://github.com/dapr/dapr/pull/10187 | `dapr/dapr` | `code_only` | `` | feat(metrics): add workflow execution buckets configuration |
| https://github.com/dapr/dapr/pull/10288 | `dapr/dapr` | `code_and_docs` | `` | Workflow: Fix transient GetInstance failure |
| https://github.com/dapr/dapr/pull/10282 | `dapr/dapr` | `code_only` | `` | sentry: stamp container image references into SVIDs |
| https://github.com/dapr/dapr/pull/10280 | `dapr/dapr` | `code_only` | `` | sec: bump grpc etc |
| https://github.com/dapr/dapr/pull/10276 | `dapr/dapr` | `code_only` | `` | [Backport release-1.17] GH workflow: adds merge group to all workflows |
| https://github.com/dapr/dapr/pull/10278 | `dapr/dapr` | `code_only` | `` | [Backport release-1.18] GH workflow: adds merge group to all workflows |
| https://github.com/dapr/dapr/pull/10275 | `dapr/dapr` | `code_only` | `` | GH workflow: adds merge group to all workflows |
| https://github.com/dapr/dapr/pull/10263 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | fix: use tick-local CollectT in subscriptions hot-reload test to stop hard-failing on transient errors |
| https://github.com/dapr/dapr/pull/10225 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] fix: preserve sub-millisecond latency precision |
| https://github.com/dapr/dapr/pull/10262 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] scheduler: bound shutdown drain, survive dead WatchJobs streams |
| https://github.com/dapr/dapr/pull/10260 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] Metrics: Restore etcd metrics on the scheduler |
| https://github.com/dapr/dapr/pull/10261 | `dapr/dapr` | `code_and_docs` | `` | scheduler: bound shutdown drain, survive dead WatchJobs streams |
| https://github.com/dapr/dapr/pull/10254 | `dapr/dapr` | `code_and_docs` | `` | Metrics: Restore etcd metrics on the scheduler |
| https://github.com/dapr/dapr/pull/10257 | `dapr/dapr` | `code_only` | `` | fix(tests): declare an fsgroup for aks environments |
| https://github.com/dapr/dapr/pull/10256 | `dapr/dapr` | `code_and_docs` | `` | Update go to 1.26.5 (#10171) |
| https://github.com/dapr/dapr/pull/10198 | `dapr/dapr` | `code_only` | `` | fix(release): only tag the highest semver release as `latest` |
| https://github.com/dapr/dapr/pull/10250 | `dapr/dapr` | `code_only` | `` | version-skew: Fix master |
| https://github.com/dapr/dapr/pull/10171 | `dapr/dapr` | `code_and_docs` | `` | Update go to 1.26.5 |
| https://github.com/dapr/dapr/pull/10249 | `dapr/dapr` | `code_and_docs` | `` | [Backport release-1.18] workflow: persist terminal state before recursive terminate cascade |
| https://github.com/dapr/dapr/pull/10156 | `dapr/dapr` | `code_only` | `` | scheduler: make cron storage backend pluggable |
| https://github.com/dapr/dapr/pull/10157 | `dapr/dapr` | `code_and_docs` | `` | workflow: persist terminal state before recursive terminate cascade |
| https://github.com/dapr/dapr/pull/10104 | `dapr/dapr` | `code_and_docs` | `` | Fix Configuration chart CRD drift |
| https://github.com/dapr/dapr/pull/10215 | `dapr/dapr` | `code_and_docs` | `` | fix: preserve sub-millisecond latency precision |
| https://github.com/dapr/dapr/pull/10164 | `dapr/dapr` | `code_only_tests_or_fixtures` | `` | Test hot-reload when kubernetes secret references update their value |
| https://github.com/dapr/dapr/pull/10169 | `dapr/dapr` | `code_only` | `` | fix: remove duplicate resource init |
| https://github.com/rust-lang/rust/pull/161979 | `rust-lang/rust` | `code_only` | `` | Rollup of 3 pull requests |
| https://github.com/rust-lang/rust/pull/160851 | `rust-lang/rust` | `code_only` | `` | Add MSA and `f16` inline ASM support for MIPS |
| https://github.com/rust-lang/rust/pull/161960 | `rust-lang/rust` | `code_only` | `` | std::sys::sgx::tls: fix TLS destructor pointer provenance |
| https://github.com/rust-lang/rust/pull/161976 | `rust-lang/rust` | `code_only` | `` | Improve rustdoc macro expansion code |
| https://github.com/rust-lang/rust/pull/161970 | `rust-lang/rust` | `code_only` | `` | Rollup of 3 pull requests |
| https://github.com/rust-lang/rust/pull/161794 | `rust-lang/rust` | `code_only` | `` | Fix handling of weak keyword `pin` |
| https://github.com/rust-lang/rust/pull/161928 | `rust-lang/rust` | `code_only` | `` | Improve to_int_checked performance |
| https://github.com/rust-lang/rust/pull/159988 | `rust-lang/rust` | `code_only` | `` | On arm, only require fpregs instead of vfp2 to allow s0-s15, s0-s31, and d0-15 register classes |
| https://github.com/rust-lang/rust/pull/159098 | `rust-lang/rust` | `code_only` | `` | Add Arc/Rc::strong_count_from_raw |
| https://github.com/rust-lang/rust/pull/161910 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | Add rustdoc-html regression test for generated macro |
| https://github.com/rust-lang/rust/pull/161965 | `rust-lang/rust` | `code_only` | `` | Rollup of 2 pull requests |
| https://github.com/rust-lang/rust/pull/161692 | `rust-lang/rust` | `code_only` | `` | Allow Unpin impls for local extern type |
| https://github.com/rust-lang/rust/pull/161886 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | compiler: Make +fix-cortex-a53-835769 a default feature for aarch64 fuchsia |
| https://github.com/rust-lang/rust/pull/161877 | `rust-lang/rust` | `code_only` | `` | Do not load macro metadata for local definitions in rustdoc |
| https://github.com/rust-lang/rust/pull/161876 | `rust-lang/rust` | `code_only` | `` | rustdoc: Correctly handle when a macro generates multiple items in `--generate-macro-expansion` |
| https://github.com/rust-lang/rust/pull/161959 | `rust-lang/rust` | `code_and_docs` | `` | Rollup of 17 pull requests |
| https://github.com/rust-lang/rust/pull/161858 | `rust-lang/rust` | `code_only` | `` | fix ICE in generic_const_parameter_types with inherents |
| https://github.com/rust-lang/rust/pull/161927 | `rust-lang/rust` | `code_only` | `` | Change `rustc_middle/src/hooks/mod.rs` to `hooks.rs` |
| https://github.com/rust-lang/rust/pull/161924 | `rust-lang/rust` | `code_only` | `` | Windows: document that `normalize_lexically` converts `/` to `\` |
| https://github.com/rust-lang/rust/pull/161897 | `rust-lang/rust` | `code_only` | `` | Reject contract attributes without arguments |
| https://github.com/rust-lang/rust/pull/161377 | `rust-lang/rust` | `code_only` | `` | [bootstrap] Don't reverse the order of dylib search path entries |
| https://github.com/rust-lang/rust/pull/161945 | `rust-lang/rust` | `code_only` | `` | std: optimise IO error formatting |
| https://github.com/rust-lang/rust/pull/161888 | `rust-lang/rust` | `code_only` | `` | compiler: Allow safestack to be togglable via #[sanitize(safestack = "...")] |
| https://github.com/rust-lang/rust/pull/161887 | `rust-lang/rust` | `code_only` | `` | std: uefi: fix File::seek returning the EOF sentinel |
| https://github.com/rust-lang/rust/pull/161883 | `rust-lang/rust` | `code_only` | `` | better deal with internal features being injected into doctests |
| https://github.com/rust-lang/rust/pull/161880 | `rust-lang/rust` | `code_only` | `` | fix rustc_lint_defs doctest issues |
| https://github.com/rust-lang/rust/pull/161865 | `rust-lang/rust` | `code_and_docs` | `` | loongarch: support passing `u128`/`i128` to inline assembly |
| https://github.com/rust-lang/rust/pull/161804 | `rust-lang/rust` | `code_only` | `` | Document PartialOrd behavior for Option<T> where T: PartialOrd |
| https://github.com/rust-lang/rust/pull/161577 | `rust-lang/rust` | `code_only` | `` | implement [u8]::split_ascii_whitespace |
| https://github.com/rust-lang/rust/pull/160594 | `rust-lang/rust` | `code_only` | `` | attach global target features to module-level assembly |
| https://github.com/rust-lang/rust/pull/158913 | `rust-lang/rust` | `code_only` | `` | Update `browser-ui-test` version to `0.24.1` |
| https://github.com/rust-lang/rust/pull/161859 | `rust-lang/rust` | `code_only` | `` | Do not optimize MIR for comptime ConstFns |
| https://github.com/rust-lang/rust/pull/161853 | `rust-lang/rust` | `code_only` | `` | Consolidate LLVM skip in check builds in bootstrap |
| https://github.com/rust-lang/rust/pull/158522 | `rust-lang/rust` | `code_only` | `` | Lint against invalid POSIX symbol definitions |
| https://github.com/rust-lang/rust/pull/161860 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | atomicptr.rs test: remove unused import |
| https://github.com/rust-lang/rust/pull/161666 | `rust-lang/rust` | `code_only` | `` | Print vendor instructions in `x vendor` |
| https://github.com/rust-lang/rust/pull/161862 | `rust-lang/rust` | `code_only` | `` | Put data segment in specified section with link_section on wasm |
| https://github.com/rust-lang/rust/pull/161870 | `rust-lang/rust` | `code_only` | `` | bind to [::1] instead of 127.0.0.1 in documentation examples for v6 UDP methods |
| https://github.com/rust-lang/rust/pull/161828 | `rust-lang/rust` | `code_only` | `` | Never type after-stabilization cleanup |
| https://github.com/rust-lang/rust/pull/161730 | `rust-lang/rust` | `code_only` | `` | Improve type mismatch annotation for lets with block-wrapped initializers |
| https://github.com/rust-lang/rust/pull/161528 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | Add regression test to ensure optimal compilation |
| https://github.com/rust-lang/rust/pull/161456 | `rust-lang/rust` | `code_only` | `` | reduce perf impact of scalar size checks |
| https://github.com/rust-lang/rust/pull/161421 | `rust-lang/rust` | `code_only` | `` | Include startup crt objects on WASI for more outputs |
| https://github.com/rust-lang/rust/pull/160848 | `rust-lang/rust` | `code_only` | `` | std: avoid aliasing violations when wrapping opaque C types |
| https://github.com/rust-lang/rust/pull/160562 | `rust-lang/rust` | `code_only` | `` | add target feature ABI checks for SPARC |
| https://github.com/rust-lang/rust/pull/157218 | `rust-lang/rust` | `code_only` | `` | Track items behind `cfg_select` in the same way we do for `cfg` |
| https://github.com/rust-lang/rust/pull/161891 | `rust-lang/rust` | `code_only` | `` | Mark `extern_item_impls` feature as incomplete |
| https://github.com/rust-lang/rust/pull/161890 | `rust-lang/rust` | `code_only` | `` | rustdoc: some clarifying comments |
| https://github.com/rust-lang/rust/pull/161889 | `rust-lang/rust` | `code_only` | `` | Add link to ownership section in ptr::read docs |
| https://github.com/rust-lang/rust/pull/161866 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | delegation: add tests fixating behavior of delegating to default trait implementations |
| https://github.com/rust-lang/rust/pull/161805 | `rust-lang/rust` | `code_only` | `` | Prefer ambiguous candidates when deduplicating traits in scope, so `ambiguous_glob_imported_traits` doesn't depend on import order |
| https://github.com/rust-lang/rust/pull/150075 | `rust-lang/rust` | `code_only` | `` | Implement clamp_to |
| https://github.com/rust-lang/rust/pull/161571 | `rust-lang/rust` | `code_only` | `` | Refactor the `#[allow(dead_code)]` propagation for impl items of traits |
| https://github.com/rust-lang/rust/pull/158854 | `rust-lang/rust` | `code_only` | `` | Add `#[rustc_test_entrypoint_marker]` |
| https://github.com/rust-lang/rust/pull/161012 | `rust-lang/rust` | `code_only` | `` | borrowck: Normalize non-rigid aliases in NLL type relating |
| https://github.com/rust-lang/rust/pull/159099 | `rust-lang/rust` | `code_only` | `` | Stabilize String::from_utf8_lossy_owned |
| https://github.com/rust-lang/rust/pull/161003 | `rust-lang/rust` | `code_only` | `` | Also warn if an invalid `doc` attribute is used on a macro invocation |
| https://github.com/rust-lang/rust/pull/134021 | `rust-lang/rust` | `code_only` | `` | Implement `IntoIterator` for `[&[mut]] Box<[T; N], A>` |
| https://github.com/rust-lang/rust/pull/151379 | `rust-lang/rust` | `code_only` | `` | Stabilize `VecDeque::retain_back` from `truncate_front` |
| https://github.com/rust-lang/rust/pull/161562 | `rust-lang/rust` | `code_only` | `` | More EC2 instance usage |
| https://github.com/rust-lang/rust/pull/156225 | `rust-lang/rust` | `code_only` | `` | feat(num): improve error messages for `TryFromIntError` |
| https://github.com/rust-lang/rust/pull/161422 | `rust-lang/rust` | `code_only` | `` | [beta] bump stage0, plus backports |
| https://github.com/rust-lang/rust/pull/161681 | `rust-lang/rust` | `code_only` | `` | Cross-compile i686-pc-windows-gnu std from x86_64 |
| https://github.com/rust-lang/rust/pull/96010 | `rust-lang/rust` | `code_only` | `` | Implement `core::ptr::Unique` on top of `NonNull` |
| https://github.com/rust-lang/rust/pull/149125 | `rust-lang/rust` | `code_only` | `` | In `BTreeMap::eq`, do not compare the elements if the sizes are different. |
| https://github.com/rust-lang/rust/pull/121533 | `rust-lang/rust` | `code_only` | `` | Handle .init_array link_section specially on wasm |
| https://github.com/rust-lang/rust/pull/161818 | `rust-lang/rust` | `code_only` | `` | Fix long type on diagnostics for conditionally implemented traits |
| https://github.com/rust-lang/rust/pull/161052 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | Add regression test for generic inference |
| https://github.com/rust-lang/rust/pull/161839 | `rust-lang/rust` | `code_only` | `` | Fix doc link to pointer::addr |
| https://github.com/rust-lang/rust/pull/161849 | `rust-lang/rust` | `code_only` | `` | Rollup of 7 pull requests |
| https://github.com/rust-lang/rust/pull/161691 | `rust-lang/rust` | `code_only` | `` | Assorted bootstrap config refactors (part 1/N) |
| https://github.com/rust-lang/rust/pull/161813 | `rust-lang/rust` | `code_only` | `` | Change `is_eligible_for_coverage` from a hook to a query |
| https://github.com/rust-lang/rust/pull/161034 | `rust-lang/rust` | `code_only` | `` | Add SVE-accelerated Vec::retain_mut for aarch64 |
| https://github.com/rust-lang/rust/pull/161843 | `rust-lang/rust` | `code_only` | `` | rustdoc: fix lint `cargo::non_kebab_case_bins` |
| https://github.com/rust-lang/rust/pull/161842 | `rust-lang/rust` | `code_only` | `` | chore: fix cargo lints |
| https://github.com/rust-lang/rust/pull/161628 | `rust-lang/rust` | `code_only` | `` | interpret: ensure that calls via no-unwind ABIs do not unwind |
| https://github.com/rust-lang/rust/pull/161840 | `rust-lang/rust` | `code_and_docs` | `` | Rollup of 5 pull requests |
| https://github.com/rust-lang/rust/pull/161690 | `rust-lang/rust` | `code_only` | `` | Deny #[inline] on EII declarations |
| https://github.com/rust-lang/rust/pull/161210 | `rust-lang/rust` | `code_only` | `` | Improve missing extern crate diagnostics in Rust 2015 |
| https://github.com/rust-lang/rust/pull/159502 | `rust-lang/rust` | `code_and_docs` | `` | Enhance suggestions for unresolved links with typos path |
| https://github.com/rust-lang/rust/pull/161736 | `rust-lang/rust` | `code_and_docs` | `` | Tidy: show todo reason when lint fails (and fix the lint's tidy allow statement which was weird and broken...) |
| https://github.com/rust-lang/rust/pull/161552 | `rust-lang/rust` | `code_only` | `` | also trigger overflow FCW when going from overflow -> error |
| https://github.com/rust-lang/rust/pull/160720 | `rust-lang/rust` | `code_only` | `` | triagebot: add ubiratan to infra-ci |
| https://github.com/rust-lang/rust/pull/161822 | `rust-lang/rust` | `code_only` | `` | Rollup of 4 pull requests |
| https://github.com/rust-lang/rust/pull/161718 | `rust-lang/rust` | `code_only` | `` | Fix the wasm32-unknown-unknown target feature/cfg bug |
| https://github.com/rust-lang/rust/pull/161701 | `rust-lang/rust` | `code_only` | `` | Rename dlltool helper function |
| https://github.com/rust-lang/rust/pull/161744 | `rust-lang/rust` | `code_only` | `` | Remove `RawDefPathHash` |
| https://github.com/rust-lang/rust/pull/161433 | `rust-lang/rust` | `code_only` | `` | Overhaul `rustc_middle::query` |
| https://github.com/rust-lang/rust/pull/150067 | `rust-lang/rust` | `code_only` | `` | Alloc `String::retain` optimization |
| https://github.com/rust-lang/rust/pull/153973 | `rust-lang/rust` | `code_only` | `` | std::process: fix UEFI ExitStatus::code() silent truncation of error … |
| https://github.com/rust-lang/rust/pull/161801 | `rust-lang/rust` | `code_and_docs` | `` | Rollup of 7 pull requests |
| https://github.com/rust-lang/rust/pull/161796 | `rust-lang/rust` | `code_only` | `` | Remove dead parse error recovery (underscores in expressions) |
| https://github.com/rust-lang/rust/pull/160183 | `rust-lang/rust` | `code_only` | `` | panic_unwind: Use global_asm! for IMGREL relocations |
| https://github.com/rust-lang/rust/pull/158370 | `rust-lang/rust` | `code_only` | `` | rewrite never type documentation |
| https://github.com/rust-lang/rust/pull/161707 | `rust-lang/rust` | `code_only` | `` | pattern_type: make print format match the current syntax |
| https://github.com/rust-lang/rust/pull/161447 | `rust-lang/rust` | `code_only` | `` | Construct paramenvs from an iterator |
| https://github.com/rust-lang/rust/pull/160354 | `rust-lang/rust` | `code_only` | `` | update `ambiguous_glob_imported_trait` lint explanation and example. |
| https://github.com/rust-lang/rust/pull/161807 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | bootstrap: skip StdarchVerify when remote testing is enabled |
| https://github.com/rust-lang/rust/pull/161773 | `rust-lang/rust` | `code_only` | `` | Update WASI targets to wasi-sdk-34 |
| https://github.com/rust-lang/rust/pull/161774 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | Add codegen test for disjunction fed to unreachable_unchecked |
| https://github.com/rust-lang/rust/pull/161724 | `rust-lang/rust` | `code_only_tests_or_fixtures` | `` | Add codegen test for static table search loop unrolling |
| https://github.com/rust-lang/rust/pull/161740 | `rust-lang/rust` | `code_only` | `` | do not compress debuginfo for Cygwin |
| https://github.com/rust-lang/rust/pull/160007 | `rust-lang/rust` | `code_only` | `` | allow `-Ldependency` search paths for panic runtimes |
| https://github.com/rust-lang/rust/pull/160871 | `rust-lang/rust` | `code_only` | `` | Remove `#[rustc_reservation_impl]` |
| https://github.com/rust-lang/rust/pull/155254 | `rust-lang/rust` | `code_only` | `` | Recover on attribute in use tree |
| https://github.com/rust-lang/rust/pull/157036 | `rust-lang/rust` | `code_only` | `` | lint against repeated repr attributes |
| https://github.com/rust-lang/rust/pull/161747 | `rust-lang/rust` | `code_only` | `` | explicitly state that allocations cannot grow to the left |
| https://github.com/rust-lang/rust/pull/161684 | `rust-lang/rust` | `code_only` | `` | Replace `Allocator + Clone` with `AllocatorClone` in btree |
| https://github.com/rust-lang/rust/pull/161443 | `rust-lang/rust` | `code_and_docs` | `` | add internal DSL for testing binders |
| https://github.com/rust-lang/rust/pull/161464 | `rust-lang/rust` | `code_only` | `` | various cleanups of `rustc_builtin_macros` |
| https://github.com/ClickHouse/ClickHouse/pull/116129 | `clickhouse/clickhouse` | `code_only` | `` | Fix iceberg identity partitioned reading |
| https://github.com/ClickHouse/ClickHouse/pull/116695 | `clickhouse/clickhouse` | `code_only` | `` | Fix crash after DETACH/ATTACH of a patch partition |
| https://github.com/ClickHouse/ClickHouse/pull/117070 | `clickhouse/clickhouse` | `code_only` | `` | Backport #116695 to 26.8: Fix crash after DETACH/ATTACH of a patch partition |
| https://github.com/ClickHouse/ClickHouse/pull/107991 | `clickhouse/clickhouse` | `code_only` | `` | validate discriminators in Variant binary bulk deserialization |
| https://github.com/ClickHouse/ClickHouse/pull/115443 | `clickhouse/clickhouse` | `code_only` | `` | Validate Variant discriminator in ColumnVariant arena deserialization |
| https://github.com/ClickHouse/ClickHouse/pull/115487 | `clickhouse/clickhouse` | `code_only` | `` | Do not push a bucket while any input is still at it in `GroupingAggregatedTransform` |
| https://github.com/ClickHouse/ClickHouse/pull/113507 | `clickhouse/clickhouse` | `code_only` | `` | Fix wrong statistics part pruning for negated float predicates with NaN |
| https://github.com/ClickHouse/ClickHouse/pull/116538 | `clickhouse/clickhouse` | `code_only` | `` | Restore short-circuit of a filter on an empty IN set over a Nullable column |
| https://github.com/ClickHouse/ClickHouse/pull/108790 | `clickhouse/clickhouse` | `code_only` | `` | Fix Bad cast ColumnSparse to ColumnString in groupConcat over Tuple with sparse subcolumn |
| https://github.com/ClickHouse/ClickHouse/pull/111701 | `clickhouse/clickhouse` | `code_only_tests_or_fixtures` | `` | Fix flaky test_kafka_formats_with_broken_message |
| https://github.com/ClickHouse/ClickHouse/pull/116976 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #116538 to 26.8: Restore short-circuit of a filter on an empty IN set over a Nullable column |
| https://github.com/ClickHouse/ClickHouse/pull/116975 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #116538 to 26.7: Restore short-circuit of a filter on an empty IN set over a Nullable column |
| https://github.com/ClickHouse/ClickHouse/pull/116546 | `clickhouse/clickhouse` | `code_only` | `` | Score PREWHERE conditions of unknown size in bytes, not rows |
| https://github.com/ClickHouse/ClickHouse/pull/115963 | `clickhouse/clickhouse` | `code_only_tests_or_fixtures` | `` | Weight most integration tests so shards actually balance by duration |
| https://github.com/ClickHouse/ClickHouse/pull/115700 | `clickhouse/clickhouse` | `code_only` | `` | Bound the recursion in several parsers and schema readers |
| https://github.com/ClickHouse/ClickHouse/pull/115954 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115700 to 26.6: Bound the recursion in several parsers and schema readers |
| https://github.com/ClickHouse/ClickHouse/pull/116974 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #116538 to 26.6: Restore short-circuit of a filter on an empty IN set over a Nullable column |
| https://github.com/ClickHouse/ClickHouse/pull/116021 | `clickhouse/clickhouse` | `code_and_docs` | `` | ref: rework filter pushdown: ActionsDAG converter, temporal types and… |
| https://github.com/ClickHouse/ClickHouse/pull/115717 | `clickhouse/clickhouse` | `code_only` | `` | Fix silent data loss in named tuple conversion and allow repeated aliases of tuple elements |
| https://github.com/ClickHouse/ClickHouse/pull/115705 | `clickhouse/clickhouse` | `code_only` | `` | Fix a crash of a window function over a Tuple with a sparse element |
| https://github.com/ClickHouse/ClickHouse/pull/91152 | `clickhouse/clickhouse` | `code_only` | `` | Fix possible inconsistent dynamic structure during writing in compact parts |
| https://github.com/ClickHouse/ClickHouse/pull/116620 | `clickhouse/clickhouse` | `code_only` | `` | Fix corrupted framed data packets with `http_write_exception_in_output_format` |
| https://github.com/ClickHouse/ClickHouse/pull/109747 | `clickhouse/clickhouse` | `code_only` | `` | Avoid server abort on type mismatch during partial result evaluation |
| https://github.com/ClickHouse/ClickHouse/pull/107511 | `clickhouse/clickhouse` | `code_only` | `` | Fix LOGICAL_ERROR on UNION subquery with INTERSECT/EXCEPT children (old analyzer) |
| https://github.com/ClickHouse/ClickHouse/pull/103478 | `clickhouse/clickhouse` | `code_only` | `` | Push equi-key filter into the left input of RIGHT JOIN for cross-type USING keys |
| https://github.com/ClickHouse/ClickHouse/pull/117063 | `clickhouse/clickhouse` | `code_only` | `` | Backport #116620 to 26.8: Fix corrupted framed data packets with `http_write_exception_in_output_format` |
| https://github.com/ClickHouse/ClickHouse/pull/117052 | `clickhouse/clickhouse` | `code_only` | `` | Backport #107511 to 26.6: Fix LOGICAL_ERROR on UNION subquery with INTERSECT/EXCEPT children (old analyzer) |
| https://github.com/ClickHouse/ClickHouse/pull/117049 | `clickhouse/clickhouse` | `code_only` | `` | Backport #109747 to 26.6: Avoid server abort on type mismatch during partial result evaluation |
| https://github.com/ClickHouse/ClickHouse/pull/117027 | `clickhouse/clickhouse` | `code_only` | `` | Backport #103478 to 26.6: Push equi-key filter into the left input of RIGHT JOIN for cross-type USING keys |
| https://github.com/ClickHouse/ClickHouse/pull/115744 | `clickhouse/clickhouse` | `code_only` | `` | Make Parquet dictionary-filter pruning cheaper: sorted hash vector, no per-value Field |
| https://github.com/ClickHouse/ClickHouse/pull/115733 | `clickhouse/clickhouse` | `code_only` | `` | Cancel in-flight merges and mutations on server shutdown |
| https://github.com/ClickHouse/ClickHouse/pull/117059 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #115705 to 26.6: Fix a crash of a window function over a Tuple with a sparse element |
| https://github.com/ClickHouse/ClickHouse/pull/115422 | `clickhouse/clickhouse` | `code_and_docs` | `` | add dimensional metrics for S3Queue |
| https://github.com/ClickHouse/ClickHouse/pull/117062 | `clickhouse/clickhouse` | `code_and_docs` | `` | Backport #115422 to 26.8: add dimensional metrics for S3Queue |
| https://github.com/ClickHouse/ClickHouse/pull/117058 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #115705 to 26.3: Fix a crash of a window function over a Tuple with a sparse element |
| https://github.com/ClickHouse/ClickHouse/pull/116371 | `clickhouse/clickhouse` | `code_only` | `` | Fix a `_table`/`_database` filter over a `Merge` table returning no rows for children that read from other tables |
| https://github.com/ClickHouse/ClickHouse/pull/115819 | `clickhouse/clickhouse` | `code_only` | `` | Parquet: fuse dictionary-index decoding with the dictionary gather |
| https://github.com/ClickHouse/ClickHouse/pull/117061 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115705 to 26.8: Fix a crash of a window function over a Tuple with a sparse element |
| https://github.com/ClickHouse/ClickHouse/pull/117057 | `clickhouse/clickhouse` | `code_only` | `` | Backport #116371 to 26.8: Fix a `_table`/`_database` filter over a `Merge` table returning no rows for children that read from other tables |
| https://github.com/ClickHouse/ClickHouse/pull/117055 | `clickhouse/clickhouse` | `code_only` | `` | Backport #116371 to 26.6: Fix a `_table`/`_database` filter over a `Merge` table returning no rows for children that read from other tables |
| https://github.com/ClickHouse/ClickHouse/pull/112414 | `clickhouse/clickhouse` | `code_only` | `` | Write per-file statistics into Iceberg manifest entries on INSERT |
| https://github.com/ClickHouse/ClickHouse/pull/116639 | `clickhouse/clickhouse` | `code_only` | `` | Build profile diff: do not report the debug-info offset as a size change |
| https://github.com/ClickHouse/ClickHouse/pull/115833 | `clickhouse/clickhouse` | `code_only` | `` | Less logging in the parallel replicas coordinator |
| https://github.com/ClickHouse/ClickHouse/pull/115348 | `clickhouse/clickhouse` | `code_only` | `` | Use the text index when a tokenizer argument matches the index tokenizer |
| https://github.com/ClickHouse/ClickHouse/pull/115791 | `clickhouse/clickhouse` | `code_only` | `` | Hide aws_external_id in DataLakeCatalog SHOW CREATE DATABASE |
| https://github.com/ClickHouse/ClickHouse/pull/108256 | `clickhouse/clickhouse` | `code_only` | `` | Do not use projections for distributed reads in make_distributed_plan |
| https://github.com/ClickHouse/ClickHouse/pull/117051 | `clickhouse/clickhouse` | `code_only` | `` | Backport #108256 to 26.6: Do not use projections for distributed reads in make_distributed_plan |
| https://github.com/ClickHouse/ClickHouse/pull/116861 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115791 to 26.3: Hide aws_external_id in DataLakeCatalog SHOW CREATE DATABASE |
| https://github.com/ClickHouse/ClickHouse/pull/116319 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115700 to 26.3: Bound the recursion in several parsers and schema readers |
| https://github.com/ClickHouse/ClickHouse/pull/115334 | `clickhouse/clickhouse` | `code_only` | `` | Do not let SET <name> = DEFAULT bypass the settings constraints |
| https://github.com/ClickHouse/ClickHouse/pull/116265 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115334 to 26.6: Do not let SET <name> = DEFAULT bypass the settings constraints |
| https://github.com/ClickHouse/ClickHouse/pull/116877 | `clickhouse/clickhouse` | `code_only` | `` | Report a missing delimiter in Values as a missing delimiter |
| https://github.com/ClickHouse/ClickHouse/pull/116635 | `clickhouse/clickhouse` | `code_only_tests_or_fixtures` | `` | Fix dead cross-entity fragment links in the built-in `/docs` page |
| https://github.com/ClickHouse/ClickHouse/pull/116809 | `clickhouse/clickhouse` | `code_only` | `` | Put the actionable part of analyzer error messages first |
| https://github.com/ClickHouse/ClickHouse/pull/116812 | `clickhouse/clickhouse` | `code_only` | `` | Replace two internal error messages for plain SQL mistakes |
| https://github.com/ClickHouse/ClickHouse/pull/112984 | `clickhouse/clickhouse` | `code_only` | `` | Bound the integration tests' nested containers by the job's memory limit |
| https://github.com/ClickHouse/ClickHouse/pull/113059 | `clickhouse/clickhouse` | `code_only_tests_or_fixtures` | `` | Collect SQL stacktraces on the hung-check and server-died abort paths |
| https://github.com/ClickHouse/ClickHouse/pull/113006 | `clickhouse/clickhouse` | `code_only` | `` | Reject malformed compressed Arrow IPC buffers before allocating for them |
| https://github.com/ClickHouse/ClickHouse/pull/112691 | `clickhouse/clickhouse` | `code_only` | `` | Do not read part sizes while committing under the parts lock |
| https://github.com/ClickHouse/ClickHouse/pull/117038 | `clickhouse/clickhouse` | `code_only_tests_or_fixtures` | `` | Report what the per-arch Bugfix validation jobs actually said |
| https://github.com/ClickHouse/ClickHouse/pull/115222 | `clickhouse/clickhouse` | `code_only` | `` | Bound text index posting list deserialization |
| https://github.com/ClickHouse/ClickHouse/pull/116536 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115222 to 26.7: Bound text index posting list deserialization |
| https://github.com/ClickHouse/ClickHouse/pull/116616 | `clickhouse/clickhouse` | `code_only` | `` | Interleave the `iota` fill loops four ways on AArch64 |
| https://github.com/ClickHouse/ClickHouse/pull/99980 | `clickhouse/clickhouse` | `code_only` | `` | Add TLP and NoREC correctness oracles to the server-side AST fuzzer |
| https://github.com/ClickHouse/ClickHouse/pull/115147 | `clickhouse/clickhouse` | `code_only` | `` | Fix THERE_IS_NO_COLUMN for DISTINCT with an aggregate projection |
| https://github.com/ClickHouse/ClickHouse/pull/116880 | `clickhouse/clickhouse` | `code_only` | `` | Use a 256-bit bitmap as the state of `groupUniqArray` for 8-bit types |
| https://github.com/ClickHouse/ClickHouse/pull/116590 | `clickhouse/clickhouse` | `code_only` | `` | Let the `Revert CI regressions` job merge the revert it opens |
| https://github.com/ClickHouse/ClickHouse/pull/117026 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #116371 to 26.8: Fix a `_table`/`_database` filter over a `Merge` table returning no rows for children that read from other t... |
| https://github.com/ClickHouse/ClickHouse/pull/117025 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #116371 to 26.7: Fix a `_table`/`_database` filter over a `Merge` table returning no rows for children that read from other t... |
| https://github.com/ClickHouse/ClickHouse/pull/117024 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #116371 to 26.6: Fix a `_table`/`_database` filter over a `Merge` table returning no rows for children that read from other t... |
| https://github.com/ClickHouse/ClickHouse/pull/104979 | `clickhouse/clickhouse` | `code_only` | `` | Fix LOGICAL_ERROR on system.detached_tables WHERE uuid filter |
| https://github.com/ClickHouse/ClickHouse/pull/113917 | `clickhouse/clickhouse` | `code_and_docs` | `` | Docs: Document snappy compression for file and object-storage I/O |
| https://github.com/ClickHouse/ClickHouse/pull/114981 | `clickhouse/clickhouse` | `code_only` | `` | Do not drop the whole GROUP BY when unwrapping injective functions of constants |
| https://github.com/ClickHouse/ClickHouse/pull/116964 | `clickhouse/clickhouse` | `code_only` | `` | Cherry pick #113507 to 26.6: Fix wrong statistics part pruning for negated float predicates with NaN |
| https://github.com/ClickHouse/ClickHouse/pull/117029 | `clickhouse/clickhouse` | `code_only` | `` | Backport #103478 to 26.8: Push equi-key filter into the left input of RIGHT JOIN for cross-type USING keys |
| https://github.com/ClickHouse/ClickHouse/pull/113695 | `clickhouse/clickhouse` | `code_only` | `` | Fix `Files metadata is empty` logical error on the object storage queue read path |
| https://github.com/ClickHouse/ClickHouse/pull/116654 | `clickhouse/clickhouse` | `code_only` | `` | Backport #113695 to 26.6: Fix `Files metadata is empty` logical error on the object storage queue read path |
| https://github.com/ClickHouse/ClickHouse/pull/109170 | `clickhouse/clickhouse` | `code_only` | `` | Fix parallel_view_processing setting being ignored for MV fan-out |
| https://github.com/ClickHouse/ClickHouse/pull/116984 | `clickhouse/clickhouse` | `code_only` | `` | Backport #109170 to 26.6: Fix parallel_view_processing setting being ignored for MV fan-out |
| https://github.com/ClickHouse/ClickHouse/pull/114182 | `clickhouse/clickhouse` | `code_only` | `` | Fix top-K dynamic filtering for empty Tuple columns |
| https://github.com/ClickHouse/ClickHouse/pull/115396 | `clickhouse/clickhouse` | `code_only` | `` | Complete ZooKeeper finalization before logging exceptions |
| https://github.com/ClickHouse/ClickHouse/pull/116532 | `clickhouse/clickhouse` | `code_only` | `` | Remove the sharded aggregator in favor of the adaptive aggregator |
| https://github.com/ClickHouse/ClickHouse/pull/115074 | `clickhouse/clickhouse` | `code_only` | `` | Fix gRPC and Arrow Flight listeners for wildcard listen hosts |
| https://github.com/ClickHouse/ClickHouse/pull/116403 | `clickhouse/clickhouse` | `code_only` | `` | Backport #115443 to 26.6: Validate Variant discriminator in ColumnVariant arena deserialization |
| https://github.com/ClickHouse/ClickHouse/pull/110958 | `clickhouse/clickhouse` | `code_only` | `` | Fix toTime key-expression type mismatch under use_legacy_to_time |
| https://github.com/ClickHouse/ClickHouse/pull/112163 | `clickhouse/clickhouse` | `code_only` | `` | Fix Iceberg OPTIMIZE MANIFEST when table metadata omits `refs` |
| https://github.com/ClickHouse/ClickHouse/pull/115759 | `clickhouse/clickhouse` | `code_only` | `` | Activate adaptive write buffers from the number of streams a wide part writes |
| https://github.com/ClickHouse/ClickHouse/pull/115039 | `clickhouse/clickhouse` | `code_and_docs` | `` | Offer the `/`-commands of the client, and name them when misspelled |
| https://github.com/ClickHouse/ClickHouse/pull/116679 | `clickhouse/clickhouse` | `code_only` | `` | Do not count rows read by executable and loop inner pipelines twice |
| https://github.com/ClickHouse/ClickHouse/pull/115548 | `clickhouse/clickhouse` | `code_only` | `` | Report an HTTP handler config error as itself, not a listen failure |
| https://github.com/ClickHouse/ClickHouse/pull/113994 | `clickhouse/clickhouse` | `code_only` | `` | Fix spurious PreconditionFailed on a retried Iceberg metadata write |
| https://github.com/ClickHouse/ClickHouse/pull/114125 | `clickhouse/clickhouse` | `code_only` | `` | Honour lock_acquire_timeout for the lightweight update lock in Keeper |
| https://github.com/ClickHouse/ClickHouse/pull/115489 | `clickhouse/clickhouse` | `code_only` | `` | Attach the system tables in `clickhouse local` on first access |
| https://github.com/ClickHouse/ClickHouse/pull/116582 | `clickhouse/clickhouse` | `code_only` | `` | Do not hold the context lock while checking that a database exists |
| https://github.com/ClickHouse/ClickHouse/pull/116973 | `clickhouse/clickhouse` | `code_only` | `` | Backport #116582 to 26.8: Do not hold the context lock while checking that a database exists |
| https://github.com/ClickHouse/ClickHouse/pull/116231 | `clickhouse/clickhouse` | `code_only` | `` | Do not open the storage object in SHOW CREATE unless the table is an Alias |
| https://github.com/ClickHouse/ClickHouse/pull/110344 | `clickhouse/clickhouse` | `code_only` | `` | Fix wrong primary-key pruning for toStartOfDay and relative-number functions on out-of-range DateTime64 |
| https://github.com/ClickHouse/ClickHouse/pull/116969 | `clickhouse/clickhouse` | `code_only` | `` | Backport #110344 to 26.8: Fix wrong primary-key pruning for toStartOfDay and relative-number functions on out-of-range DateTime64 |
| https://github.com/ClickHouse/ClickHouse/pull/116966 | `clickhouse/clickhouse` | `code_only` | `` | Backport #113507 to 26.8: Fix wrong statistics part pruning for negated float predicates with NaN |
| https://github.com/ClickHouse/ClickHouse/pull/116963 | `clickhouse/clickhouse` | `code_only` | `` | Backport #114182 to 26.8: Fix top-K dynamic filtering for empty Tuple columns |
| https://github.com/ClickHouse/ClickHouse/pull/116961 | `clickhouse/clickhouse` | `code_only` | `` | Backport #114182 to 26.6: Fix top-K dynamic filtering for empty Tuple columns |
| https://github.com/ClickHouse/ClickHouse/pull/116960 | `clickhouse/clickhouse` | `code_only` | `` | Backport #116231 to 26.8: Do not open the storage object in SHOW CREATE unless the table is an Alias |
| https://github.com/ClickHouse/ClickHouse/pull/116518 | `clickhouse/clickhouse` | `code_and_docs` | `` | Prometheus HTTP API: implement /api/v1/metadata |
| https://github.com/ClickHouse/ClickHouse/pull/115585 | `clickhouse/clickhouse` | `code_only` | `` | Bound each statement of the stateful data preparation |
| https://github.com/ClickHouse/ClickHouse/pull/114530 | `clickhouse/clickhouse` | `code_only` | `` | Reject a Parquet offset index whose first page does not start at row 0 |
| https://github.com/ClickHouse/ClickHouse/pull/116645 | `clickhouse/clickhouse` | `code_only` | `` | Reject a PRIMARY KEY that a table created from a table function cannot format back |
| https://github.com/ClickHouse/ClickHouse/pull/116878 | `clickhouse/clickhouse` | `code_only` | `` | Pop all finished distributed plan stages in one `execute` call |
| https://github.com/ClickHouse/ClickHouse/pull/115618 | `clickhouse/clickhouse` | `code_only` | `` | Fix pre-epoch `toDateTime64OrNull` conversions with zero precision |
| https://github.com/ClickHouse/ClickHouse/pull/116564 | `clickhouse/clickhouse` | `code_only` | `` | Fix a crash on an Iceberg manifest list with a huge manifest_length |
| https://github.com/ClickHouse/ClickHouse/pull/115603 | `clickhouse/clickhouse` | `code_only` | `` | Add virtual columns from v3 spec for CDC pipelines |
| https://github.com/keycloak/keycloak/pull/52132 | `keycloak/keycloak` | `code_and_docs` | `` | Deprecate clusterless feature |
| https://github.com/keycloak/keycloak/pull/52084 | `keycloak/keycloak` | `code_and_docs` | `` | Check CA Subject DN in X509 user authenticators too |
| https://github.com/keycloak/keycloak/pull/52170 | `keycloak/keycloak` | `code_only` | `` | Update scan dependencies to use trivyignore from erach branch |
| https://github.com/keycloak/keycloak/pull/52162 | `keycloak/keycloak` | `code_only` | `` | Backport to 26.7: Fix-51286:Implemented param stripping for all OIDC response modes (#52022) |
| https://github.com/keycloak/keycloak/pull/52163 | `keycloak/keycloak` | `code_only` | `` | Backport 26.6:Fix-51286:Implemented param stripping for all OIDC response modes (#52022) |
| https://github.com/keycloak/keycloak/pull/51840 | `keycloak/keycloak` | `code_only` | `` | Preserve configured order when evaluating password policies |
| https://github.com/keycloak/keycloak/pull/52032 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Migrate WebAuthnOtherSettingsTest |
| https://github.com/keycloak/keycloak/pull/52138 | `keycloak/keycloak` | `code_only` | `` | SAML ECP SOAP fault client id disclosure fix. (26.4) |
| https://github.com/keycloak/keycloak/pull/52137 | `keycloak/keycloak` | `code_only` | `` | SAML ECP SOAP fault client id disclosure fix. (26.6) |
| https://github.com/keycloak/keycloak/pull/52135 | `keycloak/keycloak` | `code_only` | `` | SAML ECP SOAP fault client id disclosure fix. (26.7) |
| https://github.com/keycloak/keycloak/pull/52141 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Fixing flaky pages assertions in the AbstractAdvancedBrokerTest#loginWithExistingUserWithBruteForceEnabled |
| https://github.com/keycloak/keycloak/pull/52143 | `keycloak/keycloak` | `code_only` | `` | (26.6) Fix signed-JWT client authentication policy bypass with forged assertion |
| https://github.com/keycloak/keycloak/pull/52142 | `keycloak/keycloak` | `code_only` | `` | (26.7) Fix signed-JWT client authentication policy bypass with forged assertion |
| https://github.com/keycloak/keycloak/pull/52115 | `keycloak/keycloak` | `code_only` | `` | (26.6) Check consento for JWT Authorization Grant |
| https://github.com/keycloak/keycloak/pull/52114 | `keycloak/keycloak` | `code_only` | `` | (26.7) Check consento for JWT Authorization Grant |
| https://github.com/keycloak/keycloak/pull/52064 | `keycloak/keycloak` | `code_and_docs` | `` | Backport 26.6:Fixes #51712 by improving post-logout redirect URI validation. (#51909) |
| https://github.com/keycloak/keycloak/pull/52061 | `keycloak/keycloak` | `code_and_docs` | `` | Backport 26.7 - Fixes #51712 by improving post-logout redirect URI validation. (#51909) |
| https://github.com/keycloak/keycloak/pull/52123 | `keycloak/keycloak` | `code_only` | `` | Do not log MariaDB 1020-HY000 warnings |
| https://github.com/keycloak/keycloak/pull/52124 | `keycloak/keycloak` | `code_only` | `` | Do not log MariaDB 1020-HY000 warnings |
| https://github.com/keycloak/keycloak/pull/52040 | `keycloak/keycloak` | `code_only` | `` | fix: workaround to inhibit the connection close handler from running |
| https://github.com/keycloak/keycloak/pull/51969 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Don't wrap exceptions when running tests remotely in the new test framework |
| https://github.com/keycloak/keycloak/pull/51952 | `keycloak/keycloak` | `code_and_docs` | `` | Concurrent DB index creation on databases |
| https://github.com/keycloak/keycloak/pull/52077 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Stabilize flaky test PasskeysUsernameFormTest |
| https://github.com/keycloak/keycloak/pull/52096 | `keycloak/keycloak` | `code_only` | `` | [CVE-2026-16089] Authorization codes can be retargeted to another cli… |
| https://github.com/keycloak/keycloak/pull/52095 | `keycloak/keycloak` | `code_only` | `` | [CVE-2026-16089] Authorization codes can be retargeted to another cli… |
| https://github.com/keycloak/keycloak/pull/52067 | `keycloak/keycloak` | `code_only` | `` | Fix signed-JWT client authentication policy bypass with forged assertion |
| https://github.com/keycloak/keycloak/pull/51673 | `keycloak/keycloak` | `code_and_docs` | `` | [OID4VP] Delegate trust material to an external trust IdP by alias |
| https://github.com/keycloak/keycloak/pull/52083 | `keycloak/keycloak` | `code_only` | `` | Do not log MariaDB 1020-HY000 warnings |
| https://github.com/keycloak/keycloak/pull/52086 | `keycloak/keycloak` | `code_and_docs` | `` | Auto-create delegation client scopes as Optional for all realms |
| https://github.com/keycloak/keycloak/pull/52000 | `keycloak/keycloak` | `code_only` | `` | Add client identity to delegation audit events |
| https://github.com/keycloak/keycloak/pull/52030 | `keycloak/keycloak` | `code_only` | `` | Filter stale role IDs in Infinispan client adapters |
| https://github.com/keycloak/keycloak/pull/52031 | `keycloak/keycloak` | `code_only` | `` | Filter stale role IDs in Infinispan client adapters |
| https://github.com/keycloak/keycloak/pull/51910 | `keycloak/keycloak` | `code_only` | `` | refactor: migrating more logic to the type provider |
| https://github.com/keycloak/keycloak/pull/52081 | `keycloak/keycloak` | `code_only` | `` | Persist client session note removals with persistent user sessions (#52038 26.6 Backport) |
| https://github.com/keycloak/keycloak/pull/51966 | `keycloak/keycloak` | `code_and_docs` | `` | Validate group policy claims against realm memberships |
| https://github.com/keycloak/keycloak/pull/51217 | `keycloak/keycloak` | `code_only` | `` | Fix ArrayIndexOutOfBoundsException in Base64Url on padding-only input |
| https://github.com/keycloak/keycloak/pull/52079 | `keycloak/keycloak` | `code_only` | `` | Check consento for JWT Authorization Grant |
| https://github.com/keycloak/keycloak/pull/52022 | `keycloak/keycloak` | `code_only` | `` | Fix-51286:Implemented param stripping for all OIDC response modes |
| https://github.com/keycloak/keycloak/pull/52062 | `keycloak/keycloak` | `code_only` | `` | [CVE-2026-16089] Authorization codes can be retargeted to another cli… |
| https://github.com/keycloak/keycloak/pull/52043 | `keycloak/keycloak` | `code_and_docs` | `` | [Backport 26.4] Skip resolving roles when processing transient tokens on FGAP requests |
| https://github.com/keycloak/keycloak/pull/52080 | `keycloak/keycloak` | `code_only` | `` | Persist client session note removals with persistent user sessions |
| https://github.com/keycloak/keycloak/pull/51264 | `keycloak/keycloak` | `code_only` | `` | Add briefRepresentation parameter for organization group-by-path endpoint |
| https://github.com/keycloak/keycloak/pull/50809 | `keycloak/keycloak` | `code_only` | `` | Honor configured admin realm in ClientManager.isInternalClient |
| https://github.com/keycloak/keycloak/pull/52003 | `keycloak/keycloak` | `code_only` | `` | Fix for #51328 Client-type bypass for fullScopeAllowed, nodeReRegistrationTimeout, and authorizationServicesEnabled |
| https://github.com/keycloak/keycloak/pull/52039 | `keycloak/keycloak` | `code_only` | `` | Persist client session note removals with persistent user sessions |
| https://github.com/keycloak/keycloak/pull/52019 | `keycloak/keycloak` | `code_only` | `` | SAML ECP SOAP fault client id disclosure fix. |
| https://github.com/keycloak/keycloak/pull/52035 | `keycloak/keycloak` | `code_only` | `` | (26.7) fix client nbf bypass |
| https://github.com/keycloak/keycloak/pull/52036 | `keycloak/keycloak` | `code_only` | `` | (26.6) fix client nbf bypass |
| https://github.com/keycloak/keycloak/pull/51565 | `keycloak/keycloak` | `code_only` | `` | Optimize composite realm role mappings |
| https://github.com/keycloak/keycloak/pull/51793 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | migrate the remain login page to theme |
| https://github.com/keycloak/keycloak/pull/52054 | `keycloak/keycloak` | `code_only` | `` | Add initial trivyignore file |
| https://github.com/keycloak/keycloak/pull/52053 | `keycloak/keycloak` | `code_only` | `` | Add initial trivyignore file |
| https://github.com/keycloak/keycloak/pull/52055 | `keycloak/keycloak` | `code_only` | `` | Add initial trivyignore file |
| https://github.com/keycloak/keycloak/pull/52051 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Fix DistributionKeycloakServer hanging on Windows when server startup… |
| https://github.com/keycloak/keycloak/pull/52050 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Fix DistributionKeycloakServer hanging on Windows when server startup… (#52008) |
| https://github.com/keycloak/keycloak/pull/52014 | `keycloak/keycloak` | `code_and_docs` | `` | Implement asynchronous DB commit for Oracle and MSSQL |
| https://github.com/keycloak/keycloak/pull/51904 | `keycloak/keycloak` | `code_and_docs` | `` | Avoid updates to IDX_USER_SESSION_EXPIRATION_LAST_REFRESH on every token refresh |
| https://github.com/keycloak/keycloak/pull/51291 | `keycloak/keycloak` | `code_and_docs` | `` | fix: removing EnvConfigSource keys that are not intended |
| https://github.com/keycloak/keycloak/pull/51773 | `keycloak/keycloak` | `code_and_docs` | `` | [Backport 26.6] Skip resolving roles when processing transient tokens on FGAP requests |
| https://github.com/keycloak/keycloak/pull/51772 | `keycloak/keycloak` | `code_and_docs` | `` | [Backport 26.7] Skip resolving roles when processing transient tokens on FGAP requests |
| https://github.com/keycloak/keycloak/pull/51714 | `keycloak/keycloak` | `code_only` | `` | Removes obsolete DirExportProvider.recursiveDeleteDir and replaces test usages with Apache Commons FileUtils. |
| https://github.com/keycloak/keycloak/pull/51982 | `keycloak/keycloak` | `code_and_docs` | `` | Deprecate route appended to AUTH_SESSION_ID cookie |
| https://github.com/keycloak/keycloak/pull/51997 | `keycloak/keycloak` | `code_only` | `` | Avoid aurora_version() probe on standard PostgreSQL |
| https://github.com/keycloak/keycloak/pull/52008 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Fix DistributionKeycloakServer hanging on Windows when server startup… |
| https://github.com/keycloak/keycloak/pull/52024 | `keycloak/keycloak` | `code_and_docs` | `` | Deprecate initiating_idp parameter |
| https://github.com/keycloak/keycloak/pull/52027 | `keycloak/keycloak` | `code_only` | `` | Chunk parent role ids in JpaRealmProvider#getCompositeRolesStream |
| https://github.com/keycloak/keycloak/pull/50815 | `keycloak/keycloak` | `code_only` | `` | SSF: Reject mismatched user+tenant subjects in synthetic SSF emit (#50812) |
| https://github.com/keycloak/keycloak/pull/51937 | `keycloak/keycloak` | `code_only` | `` | Remove default namespace in SAML writers for better signature compatibility |
| https://github.com/keycloak/keycloak/pull/52021 | `keycloak/keycloak` | `code_only` | `` | Chunk parent role ids in JpaRealmProvider#getCompositeRolesStream (#51510) |
| https://github.com/keycloak/keycloak/pull/51907 | `keycloak/keycloak` | `code_and_docs` | `` | Rename 'delegation' scope to better reflect the intent |
| https://github.com/keycloak/keycloak/pull/51981 | `keycloak/keycloak` | `code_only` | `` | (26.6) Full-scope-disabled client policy validation can be bypassed by omitting fullScopeAllowed |
| https://github.com/keycloak/keycloak/pull/51980 | `keycloak/keycloak` | `code_only` | `` | (26.7) Full-scope-disabled client policy validation can be bypassed by omitting fullScopeAllowed |
| https://github.com/keycloak/keycloak/pull/51909 | `keycloak/keycloak` | `code_and_docs` | `` | Fixes #51712 by improving post-logout redirect URI validation. |
| https://github.com/keycloak/keycloak/pull/51885 | `keycloak/keycloak` | `code_only` | `` | Fix refresh token same-second replay vulnerability |
| https://github.com/keycloak/keycloak/pull/52002 | `keycloak/keycloak` | `code_only` | `` | (26.7) Regression in UI in JS keycloak-admin-client (#51985) |
| https://github.com/keycloak/keycloak/pull/51616 | `keycloak/keycloak` | `code_only` | `` | Filter stale role IDs in Infinispan client adapters |
| https://github.com/keycloak/keycloak/pull/51675 | `keycloak/keycloak` | `code_only` | `` | fix: renaming the admin client tests module for use by the operator |
| https://github.com/keycloak/keycloak/pull/51995 | `keycloak/keycloak` | `code_only` | `` | Only check links in documentation in main repository |
| https://github.com/keycloak/keycloak/pull/51996 | `keycloak/keycloak` | `code_only` | `` | Only check links in documentation in main repository |
| https://github.com/keycloak/keycloak/pull/51994 | `keycloak/keycloak` | `code_only` | `` | Only check links in documentation in main repository |
| https://github.com/keycloak/keycloak/pull/51810 | `keycloak/keycloak` | `code_and_docs` | `` | Client scope boundary bypassed when resolving admin roles via KeycloakIdentity |
| https://github.com/keycloak/keycloak/pull/51991 | `keycloak/keycloak` | `code_only` | `` | Only check links in documentation in main repository |
| https://github.com/keycloak/keycloak/pull/51774 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Migrate WebAuthnOtherSettingsTest  |
| https://github.com/keycloak/keycloak/pull/51976 | `keycloak/keycloak` | `code_only` | `` | Apply modifySql to the logged SQL statements |
| https://github.com/keycloak/keycloak/pull/51977 | `keycloak/keycloak` | `code_only` | `` | Apply modifySql to the logged SQL statements |
| https://github.com/keycloak/keycloak/pull/51985 | `keycloak/keycloak` | `code_only` | `` | Regression in UI in JS keycloak-admin-client |
| https://github.com/keycloak/keycloak/pull/51604 | `keycloak/keycloak` | `code_and_docs` | `` | [CVE-2026-16072] Organization managers can create managed members thr… |
| https://github.com/keycloak/keycloak/pull/51794 | `keycloak/keycloak` | `code_only` | `` | Avoid aurora_version() probe on standard PostgreSQL |
| https://github.com/keycloak/keycloak/pull/51306 | `keycloak/keycloak` | `code_only` | `` | Token Exchange Delegation for Clients |
| https://github.com/keycloak/keycloak/pull/51947 | `keycloak/keycloak` | `code_only` | `` | (26.6) Client access-type condition evaluates updates against the old client… |
| https://github.com/keycloak/keycloak/pull/51946 | `keycloak/keycloak` | `code_only` | `` | (26.7) Client access-type condition evaluates updates against the old client type |
| https://github.com/keycloak/keycloak/pull/51632 | `keycloak/keycloak` | `code_only` | `` | [OID4VP] Introduce SD-JWT User Attribute / Session mappers |
| https://github.com/keycloak/keycloak/pull/51975 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Update old testsuite to commons-configuration2 |
| https://github.com/keycloak/keycloak/pull/51903 | `keycloak/keycloak` | `code_only` | `` | Apply modifySql to the logged SQL statements |
| https://github.com/keycloak/keycloak/pull/48535 | `keycloak/keycloak` | `code_only` | `` | feat(org): add client_id param to invite-user endpoint |
| https://github.com/keycloak/keycloak/pull/51694 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Migrate cookies package to the new test framework |
| https://github.com/keycloak/keycloak/pull/51942 | `keycloak/keycloak` | `code_only` | `` | (26.6) Client-protocol condition can be bypassed on admin client creation by omitting protocol |
| https://github.com/keycloak/keycloak/pull/51941 | `keycloak/keycloak` | `code_only` | `` | (26.7) Client-protocol condition can be bypassed on admin client creation by omitting protocol |
| https://github.com/keycloak/keycloak/pull/51930 | `keycloak/keycloak` | `code_only` | `` | Full-scope-disabled client policy validation can be bypassed by omitt… |
| https://github.com/keycloak/keycloak/pull/51926 | `keycloak/keycloak` | `code_only` | `` | Client access-type condition evaluates updates against the old client… |
| https://github.com/keycloak/keycloak/pull/51924 | `keycloak/keycloak` | `code_and_docs` | `` | Deprecate legacy OIDC client switches from 'OpenID Connect Compatibil… |
| https://github.com/keycloak/keycloak/pull/51891 | `keycloak/keycloak` | `code_and_docs` | `` | Mark the Client Secret Rotation feature as supported |
| https://github.com/keycloak/keycloak/pull/51925 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | DPoPTest migration |
| https://github.com/keycloak/keycloak/pull/51919 | `keycloak/keycloak` | `code_only_tests_or_fixtures` | `` | Update old testsuite to commons-configuration2 |
| https://github.com/keycloak/keycloak/pull/51911 | `keycloak/keycloak` | `code_only` | `` | Normalize again in JavaKeystoreKeyProviderFactory validation of the path (26.4) |
| https://github.com/keycloak/keycloak/pull/51901 | `keycloak/keycloak` | `code_only` | `` | Normalize again in JavaKeystoreKeyProviderFactory validation of the path (26.6) |
| https://github.com/keycloak/keycloak/pull/51879 | `keycloak/keycloak` | `code_only` | `` | Normalize again in JavaKeystoreKeyProviderFactory validation of the path (26.7) |
| https://github.com/keycloak/keycloak/pull/51914 | `keycloak/keycloak` | `code_only` | `` | Add Quarkus snapshot cache restore to Helm chart CI jobs |
| https://github.com/keycloak/keycloak/pull/51296 | `keycloak/keycloak` | `code_and_docs` | `` | [Backport 26.6] Group hierarchy search discloses hidden parent groups under FGAP v2 |
| https://github.com/keycloak/keycloak/pull/51822 | `keycloak/keycloak` | `code_and_docs` | `` | [Backport 26.6] Partial evaluation misses ancestor group policies with extendChildren |
| https://github.com/trinodb/trino/pull/23900 | `trinodb/trino` | `code_only` | `` | Add LDAP Group Provider Plugin |
| https://github.com/trinodb/trino/pull/30853 | `trinodb/trino` | `code_only` | `` | Prevent stack overflow when planning large disjunctions |
| https://github.com/trinodb/trino/pull/30933 | `trinodb/trino` | `code_only` | `` | Adjust method place in BigQueryConfig |
| https://github.com/trinodb/trino/pull/30871 | `trinodb/trino` | `code_only` | `` | Add Databricks 18 LTS product test environment |
| https://github.com/trinodb/trino/pull/30918 | `trinodb/trino` | `code_only` | `` | Preserve conjunct order under unsafe pushdown |
| https://github.com/trinodb/trino/pull/30929 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Disable TestIcebergNessieCatalogConnectorSmokeTest.testDeleteRowsConcurrently |
| https://github.com/trinodb/trino/pull/30927 | `trinodb/trino` | `code_and_docs` | `` | Retry BigQuery Storage Write API appends on RESOURCE_EXHAUSTED |
| https://github.com/trinodb/trino/pull/30220 | `trinodb/trino` | `code_only` | `` | Report memory usage from DeltaLakeMergeSink parquet reader |
| https://github.com/trinodb/trino/pull/30920 | `trinodb/trino` | `code_only` | `` | Add retry policy for listing tables in BigQuery |
| https://github.com/trinodb/trino/pull/30614 | `trinodb/trino` | `code_only` | `` | Fix dangling reference when copying a plan containing a Let expression |
| https://github.com/trinodb/trino/pull/30868 | `trinodb/trino` | `code_and_docs` | `` | Add ALTER MATERIALIZED VIEW ... EXECUTE engine support |
| https://github.com/trinodb/trino/pull/30906 | `trinodb/trino` | `code_only` | `` | Update dependencies |
| https://github.com/trinodb/trino/pull/30912 | `trinodb/trino` | `code_only` | `` | Load compiled filter input blocks on first use |
| https://github.com/trinodb/trino/pull/30865 | `trinodb/trino` | `code_only` | `` | Replace page source provider memory polling with shared memory context |
| https://github.com/trinodb/trino/pull/30877 | `trinodb/trino` | `code_only` | `` | Improve page processing of dictionary encoded data |
| https://github.com/trinodb/trino/pull/30897 | `trinodb/trino` | `code_only` | `` | Bump the web-ui-dependencies group in /core/trino-web-ui/src/main/resources/webapp with 4 updates |
| https://github.com/trinodb/trino/pull/30852 | `trinodb/trino` | `code_only` | `` | Suppress invalid metadata when listing columns in OpenSearch & Elasticsearch |
| https://github.com/trinodb/trino/pull/30885 | `trinodb/trino` | `code_only` | `` | Make DirectTrinoClient work under fault-tolerant execution |
| https://github.com/trinodb/trino/pull/30844 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Update trinodb/docker-images to 129 |
| https://github.com/trinodb/trino/pull/30884 | `trinodb/trino` | `code_only` | `` | Fix permissions for test-with-secrets |
| https://github.com/trinodb/trino/pull/30873 | `trinodb/trino` | `code_only` | `` | Allow NULL environment as resource group wildcard |
| https://github.com/trinodb/trino/pull/30855 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Change kryo-shaded to runtime in Hudi |
| https://github.com/trinodb/trino/pull/30856 | `trinodb/trino` | `code_and_docs` | `` | Bound REST case-insensitive mapping caches |
| https://github.com/trinodb/trino/pull/30816 | `trinodb/trino` | `code_only` | `` | Reuse catalog OAuth2 session for REST catalog operations |
| https://github.com/trinodb/trino/pull/30755 | `trinodb/trino` | `code_only` | `` | Finalize task info on worker restart |
| https://github.com/trinodb/trino/pull/30567 | `trinodb/trino` | `code_only` | `` | Preserve original case in TrinoPrincipal |
| https://github.com/trinodb/trino/pull/30870 | `trinodb/trino` | `code_only` | `` | Fix zizmor template-injection violations |
| https://github.com/trinodb/trino/pull/30869 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Add random suffix to view tests |
| https://github.com/trinodb/trino/pull/30861 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Fix common test flakes and improve diagnostics |
| https://github.com/trinodb/trino/pull/30863 | `trinodb/trino` | `code_only` | `` | Run product test suites in parallel |
| https://github.com/trinodb/trino/pull/30556 | `trinodb/trino` | `code_only` | `` | Harden CI/CD workflows with zizmor |
| https://github.com/trinodb/trino/pull/30846 | `trinodb/trino` | `code_only` | `` | Reduce product test bundle from 5 GB to 250 MB |
| https://github.com/trinodb/trino/pull/30825 | `trinodb/trino` | `code_and_docs` | `` | Update MongoDB image versions in tests |
| https://github.com/trinodb/trino/pull/30224 | `trinodb/trino` | `code_only` | `` | Limit uncorrelated EXISTS subquery to single row |
| https://github.com/trinodb/trino/pull/30841 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Retry HiveServer2 communication failures |
| https://github.com/trinodb/trino/pull/30859 | `trinodb/trino` | `code_only` | `` | Fix USE in PREPARE |
| https://github.com/trinodb/trino/pull/30854 | `trinodb/trino` | `code_only` | `` | Accept locally built trino in product tests |
| https://github.com/trinodb/trino/pull/30818 | `trinodb/trino` | `code_only` | `` | Default to PARQUET for new Hive tables |
| https://github.com/trinodb/trino/pull/30857 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Add SQL Language annotation to product tests |
| https://github.com/trinodb/trino/pull/30830 | `trinodb/trino` | `code_only` | `` | Add PR description check workflow |
| https://github.com/trinodb/trino/pull/30653 | `trinodb/trino` | `code_only` | `` | Report missing Iceberg metadata and manifest files as not-found |
| https://github.com/trinodb/trino/pull/30834 | `trinodb/trino` | `code_only` | `` | Close BigQuery read client if page source construction fails |
| https://github.com/trinodb/trino/pull/30683 | `trinodb/trino` | `code_only` | `` | Push legacy CHAR to VARCHAR cast into connectors correctly |
| https://github.com/trinodb/trino/pull/30747 | `trinodb/trino` | `code_only` | `` | Fix REST catalog case-insensitive name mapping cache |
| https://github.com/trinodb/trino/pull/30836 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Warn on memory pressure in product test suites |
| https://github.com/trinodb/trino/pull/30850 | `trinodb/trino` | `code_only` | `` | Skip conflicting delete file validation for Iceberg DELETE |
| https://github.com/trinodb/trino/pull/30489 | `trinodb/trino` | `code_only` | `` | Validate pull request commit messages |
| https://github.com/trinodb/trino/pull/30805 | `trinodb/trino` | `code_only` | `` | Remove redundant BigQueryClient.getTable call |
| https://github.com/trinodb/trino/pull/30481 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Use Floci for GCS connector smoke tests |
| https://github.com/trinodb/trino/pull/30840 | `trinodb/trino` | `code_only` | `` | Reapply BigQuery read timeout default |
| https://github.com/trinodb/trino/pull/30845 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Shorten TTL to 1h in BigQuery cleanup test |
| https://github.com/trinodb/trino/pull/30800 | `trinodb/trino` | `code_only` | `` | Bump the web-ui-dependencies group in /core/trino-web-ui/src/main/resources/webapp with 12 updates |
| https://github.com/trinodb/trino/pull/30793 | `trinodb/trino` | `code_only` | `` | Fix bogus `isImplicitCoercion` in `DomainTranslator` |
| https://github.com/trinodb/trino/pull/30794 | `trinodb/trino` | `code_only` | `` | Avoid boxing for function literal parameters |
| https://github.com/trinodb/trino/pull/30130 | `trinodb/trino` | `code_only` | `` | Fix double-rounding in shortDecimalToReal for high-scale short decimals |
| https://github.com/trinodb/trino/pull/30613 | `trinodb/trino` | `code_only` | `` | Fix reading null Parquet structures with VARIANT |
| https://github.com/trinodb/trino/pull/30770 | `trinodb/trino` | `code_and_docs` | `` | Support gcs.json-key property for Iceberg Google security |
| https://github.com/trinodb/trino/pull/30821 | `trinodb/trino` | `code_only` | `` | Skip checkCanSetUser() in RangerAccessControl |
| https://github.com/trinodb/trino/pull/30791 | `trinodb/trino` | `code_and_docs` | `` | Support AWS default credentials chain for SigV4 REST catalog |
| https://github.com/trinodb/trino/pull/30828 | `trinodb/trino` | `code_only` | `` | Fix CI |
| https://github.com/trinodb/trino/pull/30745 | `trinodb/trino` | `code_only` | `` | Extract config to build test matrix |
| https://github.com/trinodb/trino/pull/30784 | `trinodb/trino` | `code_only` | `` | Simplify Bun caching in CI |
| https://github.com/trinodb/trino/pull/30788 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Wait for ClickHouse mutations in execute test |
| https://github.com/trinodb/trino/pull/30749 | `trinodb/trino` | `code_only` | `` | Support returning metrics in `CALL` syntax and Iceberg `migrate` procedure |
| https://github.com/trinodb/trino/pull/30645 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Enable Iceberg BigLake metastore register table tests |
| https://github.com/trinodb/trino/pull/30211 | `trinodb/trino` | `code_only` | `` | Fix dynamic filtering on Redshift UNLOAD splits |
| https://github.com/trinodb/trino/pull/29939 | `trinodb/trino` | `code_and_docs` | `` | Reverse the implicit coercion between CHAR and VARCHAR |
| https://github.com/trinodb/trino/pull/30790 | `trinodb/trino` | `code_only` | `` | Account for outer join visited-position flags in hash builder |
| https://github.com/trinodb/trino/pull/30680 | `trinodb/trino` | `code_only` | `` | Remove varchar to char saturated floor cast |
| https://github.com/trinodb/trino/pull/30678 | `trinodb/trino` | `code_only` | `` | Prevent memory-exhausted cluster from starving zero-memory FTE tasks |
| https://github.com/trinodb/trino/pull/30774 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Fix broken DefaultDeltaLakeQueryRunnerMain |
| https://github.com/trinodb/trino/pull/30763 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Merge CTAS into TestMySqlSqlTests |
| https://github.com/trinodb/trino/pull/30773 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Set Snowflake log level as WARN in Iceberg tests |
| https://github.com/trinodb/trino/pull/30762 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Fix deprecated warning in product tests |
| https://github.com/trinodb/trino/pull/30771 | `trinodb/trino` | `code_only` | `` | Improve memory accounting and footprint of ORC dictionary writer |
| https://github.com/trinodb/trino/pull/30768 | `trinodb/trino` | `code_and_docs` | `` | Report removed statistics count in Iceberg drop_extended_stats |
| https://github.com/trinodb/trino/pull/30536 | `trinodb/trino` | `code_only` | `` | Use RLE for single-entry dictionaries |
| https://github.com/trinodb/trino/pull/30546 | `trinodb/trino` | `code_only` | `` | Add ALTER MATERIALIZED VIEW ... EXECUTE syntax |
| https://github.com/trinodb/trino/pull/30724 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Remove flaky TestFuzzAlluxioCacheFileSystem |
| https://github.com/trinodb/trino/pull/30756 | `trinodb/trino` | `code_only` | `` | Update dependencies |
| https://github.com/trinodb/trino/pull/30625 | `trinodb/trino` | `code_only` | `` | Avoid flushing each task result page |
| https://github.com/trinodb/trino/pull/30457 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Use Floci for GCS REST tests |
| https://github.com/trinodb/trino/pull/30675 | `trinodb/trino` | `code_only` | `` | Bound memory usage of Iceberg table statistics collection |
| https://github.com/trinodb/trino/pull/30731 | `trinodb/trino` | `code_only` | `` | Bump the web-ui-dependencies group in /core/trino-web-ui/src/main/resources/webapp with 5 updates |
| https://github.com/trinodb/trino/pull/30710 | `trinodb/trino` | `code_only` | `` | Skip check-commit-messages job for dependabot PR |
| https://github.com/trinodb/trino/pull/30712 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Disable flaky TestFuzzAlluxioCacheFileSystem.testFuzzTrinoInputStreamReadSkip |
| https://github.com/trinodb/trino/pull/30704 | `trinodb/trino` | `code_only` | `` | Web UI: Bump the web-ui-dependencies group in /core/trino-web-ui/src/main/resources/webapp with 15 updates |
| https://github.com/trinodb/trino/pull/29751 | `trinodb/trino` | `code_only` | `` | Parallelize and bulk-resolve getViews in the Iceberg JDBC catalog |
| https://github.com/trinodb/trino/pull/30690 | `trinodb/trino` | `code_only` | `` | Group web UI dependabot updates |
| https://github.com/trinodb/trino/pull/30701 | `trinodb/trino` | `code_only` | `` | Simplify `SqlScalarFunction.specialize` signature |
| https://github.com/trinodb/trino/pull/30654 | `trinodb/trino` | `code_only` | `` | Throw correctly div by 0 from divide_round_to_scale |
| https://github.com/trinodb/trino/pull/29849 | `trinodb/trino` | `code_only` | `` | Fix SHOW CREATE SCHEMA failure for Iceberg JDBC catalog with invalid namespace properties |
| https://github.com/trinodb/trino/pull/30665 | `trinodb/trino` | `code_only` | `` | Bump @types/react-dom from 19.2.3 to 19.2.4 in /core/trino-web-ui/src/main/resources/webapp |
| https://github.com/trinodb/trino/pull/30667 | `trinodb/trino` | `code_only` | `` | Bump @types/lodash from 4.17.24 to 4.17.25 in /core/trino-web-ui/src/main/resources/webapp |
| https://github.com/trinodb/trino/pull/30670 | `trinodb/trino` | `code_only` | `` | Bump @types/react from 19.2.17 to 19.2.18 in /core/trino-web-ui/src/main/resources/webapp |
| https://github.com/trinodb/trino/pull/30657 | `trinodb/trino` | `code_only` | `` | Resolve column types once in Iceberg statistics |
| https://github.com/trinodb/trino/pull/30669 | `trinodb/trino` | `code_only` | `` | Bump @typescript-eslint/parser from 8.65.0 to 8.66.0 in /core/trino-web-ui/src/main/resources/webapp |
| https://github.com/trinodb/trino/pull/30672 | `trinodb/trino` | `code_only` | `` | Bump @typescript-eslint/eslint-plugin from 8.65.0 to 8.66.0 in /core/trino-web-ui/src/main/resources/webapp |
| https://github.com/trinodb/trino/pull/30673 | `trinodb/trino` | `code_only` | `` | Bump axios from 1.18.1 to 1.19.0 in /core/trino-web-ui/src/main/resources/webapp |
| https://github.com/trinodb/trino/pull/30630 | `trinodb/trino` | `code_only` | `` | Compute `sum(decimal)` in sliding window efficiently |
| https://github.com/trinodb/trino/pull/30664 | `trinodb/trino` | `code_only` | `` | Bump actions/setup-java from 5.6.0 to 5.7.0 in /.github/actions/setup |
| https://github.com/trinodb/trino/pull/30663 | `trinodb/trino` | `code_only` | `` | Bump dorny/paths-filter from 4.0.2 to 4.0.3 |
| https://github.com/trinodb/trino/pull/30659 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Update TrinoContainer to use compatible substitute for Docker image |
| https://github.com/trinodb/trino/pull/30632 | `trinodb/trino` | `code_only` | `` | Validate time zone offset when encoding time with time zone |
| https://github.com/trinodb/trino/pull/30649 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Fix REST catalog test servlet ETag handling |
| https://github.com/trinodb/trino/pull/30197 | `trinodb/trino` | `code_only` | `` | Add week and quarter support for date_trunc predicate pushdown |
| https://github.com/trinodb/trino/pull/30637 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Bump dep.nessie.version from 0.108.3 to 0.108.4 |
| https://github.com/trinodb/trino/pull/30600 | `trinodb/trino` | `code_only` | `` | Fix wrong results by failing the query when sum(bigint) overflows in a window function |
| https://github.com/trinodb/trino/pull/30629 | `trinodb/trino` | `code_only` | `` | Reject negative divisor in $divide_round_to_scale  |
| https://github.com/trinodb/trino/pull/30604 | `trinodb/trino` | `code_only_tests_or_fixtures` | `` | Improve product test logging |
| https://github.com/hashicorp/terraform-provider-aws/pull/44383 | `hashicorp/terraform-provider-aws` | `code_and_docs` | `` | OpenSearch Ingestion: new resources pipeline endpoint and resource policy resources |
| https://github.com/hashicorp/terraform-provider-aws/pull/49177 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | docs/cloudfront_realtime_log_config: document cf.logCustomData() log fields |
| https://github.com/hashicorp/terraform-provider-aws/pull/49157 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New List Resource: `aws_osis_pipeline` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49140 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_bedrockagentcore_memory_strategy: Add reflection configuration for episodic memory |
| https://github.com/hashicorp/terraform-provider-aws/pull/49135 | `hashicorp/terraform-provider-aws` | `code_only` | `` | new list resource: rekognition_collection |
| https://github.com/hashicorp/terraform-provider-aws/pull/49121 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New list resource: `aws_eks_access_policy_association` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49096 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Adds sweepers for `aws_vpc_ipam_pool` and `aws_vpc_ipam_pool_cidr` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49093 | `hashicorp/terraform-provider-aws` | `code_only` | `` | internal/backoff: move go-vcr check into `backoff.SDKv2HelperRetryCompatibleDelay` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49092 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Clarifies instructions for Semgrep rule `map_block_key-meaningful-names` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49090 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New list resource: `aws_eks_access_entry` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49086 | `hashicorp/terraform-provider-aws` | `code_only` | `` | l/aws_flow_log: new list resource |
| https://github.com/hashicorp/terraform-provider-aws/pull/49076 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_cloudwatch_log_storage_tier_policy: Add intelligent logs tiering |
| https://github.com/hashicorp/terraform-provider-aws/pull/49073 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New list resource: `aws_eks_node_group` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49071 | `hashicorp/terraform-provider-aws` | `code_only` | `` | autoscaling: New style sweepers and reset `instance_lifecycle_policy` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49044 | `hashicorp/terraform-provider-aws` | `code_and_docs` | `` | r/aws_bedrock_evaluation_job: new resource  |
| https://github.com/hashicorp/terraform-provider-aws/pull/49043 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/`aws_mailmanager_traffic_policy` : New Resource |
| https://github.com/hashicorp/terraform-provider-aws/pull/49032 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_dynamodb_table: No longer replace resource when decreasing `warm_throughput` values |
| https://github.com/hashicorp/terraform-provider-aws/pull/49022 | `hashicorp/terraform-provider-aws` | `code_only` | `` | rekognition: add resource identity to service |
| https://github.com/hashicorp/terraform-provider-aws/pull/49007 | `hashicorp/terraform-provider-aws` | `code_only` | `` | list resource/aws_sqs_queue: Removes resource Read function from List |
| https://github.com/hashicorp/terraform-provider-aws/pull/48989 | `hashicorp/terraform-provider-aws` | `code_only` | `` | list resource/aws_secretsmanager_secret_version: Removes resource Read function from List |
| https://github.com/hashicorp/terraform-provider-aws/pull/48934 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | autoscaling: document and test reservations-then-balanced AZ distribution mode |
| https://github.com/hashicorp/terraform-provider-aws/pull/48892 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_launch_template: add ena_queue_count to network_interfaces |
| https://github.com/hashicorp/terraform-provider-aws/pull/48869 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_eks_pod_identity_association: add policy argument |
| https://github.com/hashicorp/terraform-provider-aws/pull/48781 | `hashicorp/terraform-provider-aws` | `code_only` | `` | feat: add MultiRegionClusters support in aws_fis_experiment_templates |
| https://github.com/hashicorp/terraform-provider-aws/pull/48758 | `hashicorp/terraform-provider-aws` | `code_only` | `` | enhance(bedrockagentcore_memory_strategy): add reflection_configuration for EPISODIC type |
| https://github.com/hashicorp/terraform-provider-aws/pull/46918 | `hashicorp/terraform-provider-aws` | `code_only` | `` | d/aws_vpc multiple ipv6_cidr_block_associations |
| https://github.com/hashicorp/terraform-provider-aws/pull/46414 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Implementation to support managed secrets in terraform provider for AWS |
| https://github.com/hashicorp/terraform-provider-aws/pull/42507 | `hashicorp/terraform-provider-aws` | `code_only` | `` | [Enhancement] aws_codepipeline:  support for `Compute` action |
| https://github.com/hashicorp/terraform-provider-aws/pull/49711 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Prefix allocations for Direct Connect virtual interfaces |
| https://github.com/hashicorp/terraform-provider-aws/pull/48704 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_bedrockagentcore_gateway_target: add HTTP passthrough target with schema and stickiness |
| https://github.com/hashicorp/terraform-provider-aws/pull/49728 | `hashicorp/terraform-provider-aws` | `code_only` | `` | F data source eks kube controller manager config |
| https://github.com/hashicorp/terraform-provider-aws/pull/49721 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | service/vpclattice: fix auth policy and resource policy disappears tests |
| https://github.com/hashicorp/terraform-provider-aws/pull/49730 | `hashicorp/terraform-provider-aws` | `code_only` | `` | F eks cluster versions pod gc controller config |
| https://github.com/hashicorp/terraform-provider-aws/pull/49724 | `hashicorp/terraform-provider-aws` | `code_and_docs` | `` | New list resource: `aws_lambdamicrovms_image` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49725 | `hashicorp/terraform-provider-aws` | `code_only` | `` | feat(eks): Add pod_gc_controller_config to kube_controller_manager_config |
| https://github.com/hashicorp/terraform-provider-aws/pull/49712 | `hashicorp/terraform-provider-aws` | `code_only` | `` | l/aws_key_pair: RI + List Support |
| https://github.com/hashicorp/terraform-provider-aws/pull/49580 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New Resource: aws_mailmanager_archive |
| https://github.com/hashicorp/terraform-provider-aws/pull/48897 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New Lambda Microvms Service |
| https://github.com/hashicorp/terraform-provider-aws/pull/49718 | `hashicorp/terraform-provider-aws` | `code_only` | `` | new list resource: opensearchserveress_lifecycle_policy |
| https://github.com/hashicorp/terraform-provider-aws/pull/49717 | `hashicorp/terraform-provider-aws` | `code_only` | `` | new list resource: opensearchserveress_access_policy |
| https://github.com/hashicorp/terraform-provider-aws/pull/49716 | `hashicorp/terraform-provider-aws` | `code_only` | `` | skaff: tidy test config filepath build |
| https://github.com/hashicorp/terraform-provider-aws/pull/48984 | `hashicorp/terraform-provider-aws` | `code_only` | `` | 🤖 New Resource: aws_lambdamicrovms_microvm |
| https://github.com/hashicorp/terraform-provider-aws/pull/48706 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_bedrockagentcore_gateway_target: add connector MCP target configuration |
| https://github.com/hashicorp/terraform-provider-aws/pull/49690 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_redshift_namespace_registration: Adds Resource Identity tests |
| https://github.com/hashicorp/terraform-provider-aws/pull/49689 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Fixes error in Framework Import by Resource with optional identity attributes |
| https://github.com/hashicorp/terraform-provider-aws/pull/49701 | `hashicorp/terraform-provider-aws` | `code_and_docs` | `` | docs: port AI agent guides to `.agents/skills` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49699 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | Adds missing PreCheck for Directory Bucket tests |
| https://github.com/hashicorp/terraform-provider-aws/pull/44260 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_elasticache_replication_group: add write-only arguments for auth_token |
| https://github.com/hashicorp/terraform-provider-aws/pull/48765 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_bedrockagentcore_memory_strategy: add memory_record_schema |
| https://github.com/hashicorp/terraform-provider-aws/pull/48766 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_bedrockagentcore_memory_strategy: add self_managed custom configuration |
| https://github.com/hashicorp/terraform-provider-aws/pull/48877 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_bedrockagentcore_memory: support adding indexed keys after creation |
| https://github.com/hashicorp/terraform-provider-aws/pull/49114 | `hashicorp/terraform-provider-aws` | `code_only` | `` | [bugfix] aws_elasticache_cluster plan time validation for transit_encryption_enabled |
| https://github.com/hashicorp/terraform-provider-aws/pull/49264 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_savingsplans_savings_plan: mark upfront_payment_amount as Computed |
| https://github.com/hashicorp/terraform-provider-aws/pull/49687 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_s3_account_public_access_block: Handle eventual consistency on create |
| https://github.com/hashicorp/terraform-provider-aws/pull/49395 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_cloudfront_function: Add validation of input variables. |
| https://github.com/hashicorp/terraform-provider-aws/pull/49455 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Update Go devcontainer image to 1.26 |
| https://github.com/hashicorp/terraform-provider-aws/pull/49660 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New Resource: aws_sesv2_multi_region_endpoint |
| https://github.com/hashicorp/terraform-provider-aws/pull/49676 | `hashicorp/terraform-provider-aws` | `code_only` | `` | l/aws_dsql_cluster_policy: new list resource |
| https://github.com/hashicorp/terraform-provider-aws/pull/49679 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_savingsplan_savings_plan: mark `purchase_time` as `Optional` and `Computed` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49673 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_dsql_cluster_policy: prefer AutoFlex, consolidate `PutPolicy` logic |
| https://github.com/hashicorp/terraform-provider-aws/pull/49696 | `hashicorp/terraform-provider-aws` | `code_only` | `` | l/`aws_ecr_lifecycle_policy`: New List Resource |
| https://github.com/hashicorp/terraform-provider-aws/pull/49678 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_savingsplan_savings_plan: mark `queued` as a target state during creation |
| https://github.com/hashicorp/terraform-provider-aws/pull/49582 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Syncs smoke tests in Makefile and TeamCity |
| https://github.com/hashicorp/terraform-provider-aws/pull/49682 | `hashicorp/terraform-provider-aws` | `code_only` | `` | new list resource: aws_ecs_cluster |
| https://github.com/hashicorp/terraform-provider-aws/pull/49585 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_resiliencehubv2_input_source: Change `resource_configuration.resource_tag` from `List` to `Set` |
| https://github.com/hashicorp/terraform-provider-aws/pull/48967 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_pinpointsmsvoicev2_keyword: New resource |
| https://github.com/hashicorp/terraform-provider-aws/pull/49659 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_secretsmanager_secret_rotation: support disabling rotation |
| https://github.com/hashicorp/terraform-provider-aws/pull/49587 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_dx_private_virtual_interface: support long BGP ASN |
| https://github.com/hashicorp/terraform-provider-aws/pull/49662 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | resource/aws_iam_role_policy: Removes redundant test |
| https://github.com/hashicorp/terraform-provider-aws/pull/49588 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_dx_transit_virtual_interface: support long BGP ASN |
| https://github.com/hashicorp/terraform-provider-aws/pull/49668 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/`aws_workspaces_directory`: Add `workspace_access_properties.access_endpoint_config` argument |
| https://github.com/hashicorp/terraform-provider-aws/pull/49602 | `hashicorp/terraform-provider-aws` | `code_only` | `` | new list resource: aws_db_instance |
| https://github.com/hashicorp/terraform-provider-aws/pull/49656 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_observabilityadmin_centralization_rule_for_organization: add tag_propagation_configuration |
| https://github.com/hashicorp/terraform-provider-aws/pull/49654 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Enable `iface` and `mirror` golangci-lint linters |
| https://github.com/hashicorp/terraform-provider-aws/pull/49603 | `hashicorp/terraform-provider-aws` | `code_only` | `` | r/aws_resiliencehubv2_service: Add `associated_system.user_journey_ids` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49604 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_ssoadmin_application: Fixes error in no-refresh no-change test case |
| https://github.com/hashicorp/terraform-provider-aws/pull/49268 | `hashicorp/terraform-provider-aws` | `code_only` | `` | [bugfix] `aws_elasticache_replication_group` add write-only auth_token arguments |
| https://github.com/hashicorp/terraform-provider-aws/pull/49657 | `hashicorp/terraform-provider-aws` | `code_only` | `` | l/aws_dsql_cluster: new list resource |
| https://github.com/hashicorp/terraform-provider-aws/pull/49606 | `hashicorp/terraform-provider-aws` | `code_and_docs` | `` | Adds `shellcheck` make target and GHA |
| https://github.com/hashicorp/terraform-provider-aws/pull/49625 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Adds Semgrep rule to prevent `fwflex.StringValueToFramework(ctx, *stringPtr)` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49612 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Teamcity: gh CLI and mod cache addition |
| https://github.com/hashicorp/terraform-provider-aws/pull/49623 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Adds Semgrep rule to prevent `fwflex.StringValueToFramework(ctx, aws.ToString(...))` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49614 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_cloudwatch_log_resource_policy: Fixes error when importing by identity for resource-scope |
| https://github.com/hashicorp/terraform-provider-aws/pull/49619 | `hashicorp/terraform-provider-aws` | `code_only` | `` | sweeper/aws_bedrockagentcore_evaluator: Excludes third-party evaluators when sweeping |
| https://github.com/hashicorp/terraform-provider-aws/pull/49620 | `hashicorp/terraform-provider-aws` | `code_only` | `` | List/aws_bedrockagentcore_evaluator: excludes third-party evaluators |
| https://github.com/hashicorp/terraform-provider-aws/pull/49613 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | resource/aws_cloudwatch_log_resource_policy: Updates `basic` tests |
| https://github.com/hashicorp/terraform-provider-aws/pull/49658 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New PlanModifier: `tfsetplanmodifier.RequiresReplaceIfElementsDeleted` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49605 | `hashicorp/terraform-provider-aws` | `code_only` | `` | CI: Performance script is failing silently |
| https://github.com/hashicorp/terraform-provider-aws/pull/48853 | `hashicorp/terraform-provider-aws` | `code_only` | `` | list resource/aws_s3_bucket_public_access_block: Removes resource Read function from List |
| https://github.com/hashicorp/terraform-provider-aws/pull/48958 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New Data Source: `aws_elasticache_service_update_actions` |
| https://github.com/hashicorp/terraform-provider-aws/pull/48855 | `hashicorp/terraform-provider-aws` | `code_only` | `` | list resource/aws_s3_object: Removes resource Read function from List |
| https://github.com/hashicorp/terraform-provider-aws/pull/49058 | `hashicorp/terraform-provider-aws` | `code_only` | `` | l/aws_secretsmanager_secret_policy: new list resource  |
| https://github.com/hashicorp/terraform-provider-aws/pull/48974 | `hashicorp/terraform-provider-aws` | `code_only` | `` | aws_s3_bucket_notification: Add list support |
| https://github.com/hashicorp/terraform-provider-aws/pull/48904 | `hashicorp/terraform-provider-aws` | `code_only` | `` | feat(bedrockagent): add Managed Knowledge Base support (type=MANAGED) |
| https://github.com/hashicorp/terraform-provider-aws/pull/49040 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Bump actions/labeler from 6.2.0 to 7.0.0 |
| https://github.com/hashicorp/terraform-provider-aws/pull/48979 | `hashicorp/terraform-provider-aws` | `code_only` | `` | closed_items: pin checkout to base ref for merged fork PRs |
| https://github.com/hashicorp/terraform-provider-aws/pull/49039 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Bump actions/checkout from 7.0.0 to 7.0.1 |
| https://github.com/hashicorp/terraform-provider-aws/pull/48966 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_sagemaker_endpoint: Prevent error why retrying creation |
| https://github.com/hashicorp/terraform-provider-aws/pull/48516 | `hashicorp/terraform-provider-aws` | `code_only` | `` | datazone: use smerr |
| https://github.com/hashicorp/terraform-provider-aws/pull/48998 | `hashicorp/terraform-provider-aws` | `code_only` | `` | teamcity: configuration for running tests in PRs |
| https://github.com/hashicorp/terraform-provider-aws/pull/48962 | `hashicorp/terraform-provider-aws` | `code_only` | `` | fix: stabilize ActiveMQ shared resources state |
| https://github.com/hashicorp/terraform-provider-aws/pull/48993 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | Updates naming guidance for `aws_sagemaker_endpoint` and `aws_sagemaker_endpoint_configuration` |
| https://github.com/hashicorp/terraform-provider-aws/pull/48736 | `hashicorp/terraform-provider-aws` | `code_only` | `` | Support `TF_AWS_WEB_IDENTITY_TOKEN` environment variable as an alternative to `assume_role_with_web_identity.web_identity_token` |
| https://github.com/hashicorp/terraform-provider-aws/pull/46483 | `hashicorp/terraform-provider-aws` | `code_only` | `` | b-ipam-resource-pool-cross-account: Allow cross account VPC IPAM resource pools |
| https://github.com/hashicorp/terraform-provider-aws/pull/49012 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | Reverts change to `Disappears` step |
| https://github.com/hashicorp/terraform-provider-aws/pull/48963 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New Action: `aws_elasticache_apply_service_update` |
| https://github.com/hashicorp/terraform-provider-aws/pull/49004 | `hashicorp/terraform-provider-aws` | `code_only` | `` | opensearchserverless: use smerr |
| https://github.com/hashicorp/terraform-provider-aws/pull/49011 | `hashicorp/terraform-provider-aws` | `code_only_tests_or_fixtures` | `` | resource/aws_sagemaker_endpoint: Adds tests for Auto Scaling |
| https://github.com/hashicorp/terraform-provider-aws/pull/48977 | `hashicorp/terraform-provider-aws` | `code_only` | `` | resource/aws_eks_node_group: Add warm_pool configuration block |
| https://github.com/hashicorp/terraform-provider-aws/pull/48965 | `hashicorp/terraform-provider-aws` | `code_only` | `` | New Data Source: S3 Buckets  |
| https://github.com/mattermost/mattermost/pull/36820 | `mattermost/mattermost` | `code_only` | `` | MM-68283 - Add render-time ABAC permission decisions for file upload/download |
| https://github.com/mattermost/mattermost/pull/38114 | `mattermost/mattermost` | `code_only` | `` | [MM-67123] Prevent mention clicks in preview from submitting the draft |
| https://github.com/mattermost/mattermost/pull/38124 | `mattermost/mattermost` | `code_and_docs` | `` | Deduplicate System Console config isDisabled dependencies |
| https://github.com/mattermost/mattermost/pull/37881 | `mattermost/mattermost` | `code_only` | `` | MM 70120 channel attributes foundation |
| https://github.com/mattermost/mattermost/pull/37743 | `mattermost/mattermost` | `code_only` | `` | MM-70018: Remove unused config fields for v12 |
| https://github.com/mattermost/mattermost/pull/38141 | `mattermost/mattermost` | `code_only` | `` | MM-70366: Add a readOnly mode to WysiwygEditor |
| https://github.com/mattermost/mattermost/pull/38173 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37928 |
| https://github.com/mattermost/mattermost/pull/37928 | `mattermost/mattermost` | `code_only` | `` | [MM-63470] Fix messages being sent to the previous channel after /msg or Cmd+K |
| https://github.com/mattermost/mattermost/pull/38022 | `mattermost/mattermost` | `code_and_docs` | `` | [MM-57807] Graduate Hardened Mode out of Experimental Features |
| https://github.com/mattermost/mattermost/pull/38025 | `mattermost/mattermost` | `code_and_docs` | `` | Graduate account deactivation and user status away timeout to Site Configuration > Users and Teams |
| https://github.com/mattermost/mattermost/pull/38054 | `mattermost/mattermost` | `code_only` | `` | MM-69945: Align post type validation across post and scheduled post paths |
| https://github.com/mattermost/mattermost/pull/38138 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | E2E/Playwright: Fix tests using file server host |
| https://github.com/mattermost/mattermost/pull/38150 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38040 |
| https://github.com/mattermost/mattermost/pull/38014 | `mattermost/mattermost` | `code_and_docs` | `` | E2E/Playwright: Upgrade playwright@1.62 and its deps |
| https://github.com/mattermost/mattermost/pull/38148 | `mattermost/mattermost` | `code_only` | `` | Backport i18n packaging and locale fallback fixes |
| https://github.com/mattermost/mattermost/pull/38040 | `mattermost/mattermost` | `code_only` | `` | Allow public permalink clicks to join when compliance is enabled |
| https://github.com/mattermost/mattermost/pull/38149 | `mattermost/mattermost` | `code_only` | `` | Fix English i18n source typos and audit wording |
| https://github.com/mattermost/mattermost/pull/37871 | `mattermost/mattermost` | `code_only` | `` | Add OnLicenseChanged plugin hook |
| https://github.com/mattermost/mattermost/pull/38118 | `mattermost/mattermost` | `code_only` | `` | MM-70307: Update dependencies (11.7) |
| https://github.com/mattermost/mattermost/pull/38018 | `mattermost/mattermost` | `code_only` | `` | [GH-30481] Add negative caching for missing custom emoji names in LocalCacheEmojiStore |
| https://github.com/mattermost/mattermost/pull/38142 | `mattermost/mattermost` | `code_only` | `` | Update latest patch version to 11.7.11 |
| https://github.com/mattermost/mattermost/pull/38101 | `mattermost/mattermost` | `code_only` | `` | [MM-65738] Clarify main logger shutdown timeout diagnostic |
| https://github.com/mattermost/mattermost/pull/38132 | `mattermost/mattermost` | `code_only` | `` | [MM-70313] Detect CJK analyzer plugins reported under a prefixed component name |
| https://github.com/mattermost/mattermost/pull/38073 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | E2E/Playwright: Fix file server host |
| https://github.com/mattermost/mattermost/pull/37907 | `mattermost/mattermost` | `code_only` | `` | [MM-69895] Delete bot access tokens when permanently deleting a bot |
| https://github.com/mattermost/mattermost/pull/38059 | `mattermost/mattermost` | `code_only` | `` | [MM-70389] Add Android to the user_agent_platform session attribute values |
| https://github.com/mattermost/mattermost/pull/38126 | `mattermost/mattermost` | `code_and_docs` | `` | Cherry pick #38010 to release-11.11 |
| https://github.com/mattermost/mattermost/pull/38125 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38059 |
| https://github.com/mattermost/mattermost/pull/38010 | `mattermost/mattermost` | `code_and_docs` | `` | [MM-70291] Add Global Relay custom EML header setting |
| https://github.com/mattermost/mattermost/pull/38115 | `mattermost/mattermost` | `code_only` | `` | [MM-70402] Fix Channel Settings showing unsaved changes on open for channels with untidy stored text |
| https://github.com/mattermost/mattermost/pull/37987 | `mattermost/mattermost` | `code_only` | `` | Log file IDs instead of filenames during file upload and content extraction |
| https://github.com/mattermost/mattermost/pull/38123 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | Fix nil context panic in TestDoSetupSessionAttributesProperties |
| https://github.com/mattermost/mattermost/pull/38116 | `mattermost/mattermost` | `code_only` | `` | [MM-63635] Fix plugin RHS panels not opening from the App Bar in the Threads view |
| https://github.com/mattermost/mattermost/pull/38105 | `mattermost/mattermost` | `code_only` | `` | MM-70307: Bump Go version to v1.26.7 (11.7) |
| https://github.com/mattermost/mattermost/pull/38095 | `mattermost/mattermost` | `code_and_docs` | `` | MM-70307: Change Postgres test password to mostest_password  (11.7) |
| https://github.com/mattermost/mattermost/pull/37636 | `mattermost/mattermost` | `code_only` | `` | [MM-70224] Migrate property field reads to request context |
| https://github.com/mattermost/mattermost/pull/38120 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38115 |
| https://github.com/mattermost/mattermost/pull/37966 | `mattermost/mattermost` | `code_only` | `` | [MM-69646] Disallow MoveThreadsEnabled feature flag (fail server startup) |
| https://github.com/mattermost/mattermost/pull/38100 | `mattermost/mattermost` | `code_only` | `` | Update latest patch version to 11.10.2 |
| https://github.com/mattermost/mattermost/pull/38084 | `mattermost/mattermost` | `code_only` | `` | [MM-70290] Run app migrations locked to the master DB |
| https://github.com/mattermost/mattermost/pull/37971 | `mattermost/mattermost` | `code_only` | `` | MM-69962: Fix inline media flickering between sizes near the 480px container threshold |
| https://github.com/mattermost/mattermost/pull/38088 | `mattermost/mattermost` | `code_only` | `` | MM-70307: Update dependencies (11.10) |
| https://github.com/mattermost/mattermost/pull/38086 | `mattermost/mattermost` | `code_only` | `` | MM-70307: Update dependencies |
| https://github.com/mattermost/mattermost/pull/38094 | `mattermost/mattermost` | `code_only` | `` | MM-70307: Update dependencies (11.11) |
| https://github.com/mattermost/mattermost/pull/37037 | `mattermost/mattermost` | `code_only` | `` | MM-69232 Enable concurrent React in E2E tests |
| https://github.com/mattermost/mattermost/pull/38081 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #34903 |
| https://github.com/mattermost/mattermost/pull/38069 | `mattermost/mattermost` | `code_and_docs` | `` | Automated cherry pick of #38060 |
| https://github.com/mattermost/mattermost/pull/38068 | `mattermost/mattermost` | `code_and_docs` | `` | Automated cherry pick of #38060 |
| https://github.com/mattermost/mattermost/pull/34903 | `mattermost/mattermost` | `code_only` | `` | Mattermost emoji reaction fix |
| https://github.com/mattermost/mattermost/pull/37818 | `mattermost/mattermost` | `code_only` | `` | MM-70100: Adjust Slack import user handling based on import type |
| https://github.com/mattermost/mattermost/pull/38079 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | ci: bump test-system-io-summary action for missed-spec status (#37804) |
| https://github.com/mattermost/mattermost/pull/37804 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | ci: bump test-system-io-summary action for missed-spec status |
| https://github.com/mattermost/mattermost/pull/38066 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38038 |
| https://github.com/mattermost/mattermost/pull/38064 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38038 |
| https://github.com/mattermost/mattermost/pull/38063 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38038 |
| https://github.com/mattermost/mattermost/pull/38065 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38038 |
| https://github.com/mattermost/mattermost/pull/38055 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37802 |
| https://github.com/mattermost/mattermost/pull/38067 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38038 |
| https://github.com/mattermost/mattermost/pull/37802 | `mattermost/mattermost` | `code_only` | `` | MM-70071: Automatically select hosted push notification server based on license |
| https://github.com/mattermost/mattermost/pull/38028 | `mattermost/mattermost` | `code_only` | `` | Cherry-pick #37420 to release-11.7 |
| https://github.com/mattermost/mattermost/pull/38060 | `mattermost/mattermost` | `code_and_docs` | `` | MM-70307: Change Postgres test password to mostest_password |
| https://github.com/mattermost/mattermost/pull/38038 | `mattermost/mattermost` | `code_only` | `` | Precompute multibyte mention keywords once per post |
| https://github.com/mattermost/mattermost/pull/38002 | `mattermost/mattermost` | `code_only` | `` | [MM-69866] Add Applies-to resource picker (Users, Channels, Posts) to New attribute |
| https://github.com/mattermost/mattermost/pull/38008 | `mattermost/mattermost` | `code_only` | `` | MM-50202 Remove redundant findDOMNode from UserSettingsModal |
| https://github.com/mattermost/mattermost/pull/37974 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | [MM-70198] Fix post preview layout shift by overlaying the "Show more" control |
| https://github.com/mattermost/mattermost/pull/37569 | `mattermost/mattermost` | `code_only` | `` | [MM-70277] Improve plugin upload dropzone UX |
| https://github.com/mattermost/mattermost/pull/38077 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | Automated cherry pick of #37804 |
| https://github.com/mattermost/mattermost/pull/38075 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | Automated cherry pick of #37804 |
| https://github.com/mattermost/mattermost/pull/38076 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | Automated cherry pick of #37804 |
| https://github.com/mattermost/mattermost/pull/37352 | `mattermost/mattermost` | `code_and_docs` | `` | SEC-10587 E2E/Playwright: Migrate RFQA browser tests (batch 1, 1-20) |
| https://github.com/mattermost/mattermost/pull/38042 | `mattermost/mattermost` | `code_only` | `` | Trim whitespace when saving comma-separated System Console settings |
| https://github.com/mattermost/mattermost/pull/38027 | `mattermost/mattermost` | `code_and_docs` | `` | Graduate theme and onboarding settings to Site Configuration > Customization |
| https://github.com/mattermost/mattermost/pull/38013 | `mattermost/mattermost` | `code_only` | `` | Reuse Timestamp for user-preferred datetime formats |
| https://github.com/mattermost/mattermost/pull/38026 | `mattermost/mattermost` | `code_and_docs` | `` | Graduate Enable Channel Viewed WebSocket Messages to Environment > Web Server |
| https://github.com/mattermost/mattermost/pull/37968 | `mattermost/mattermost` | `code_only` | `` | [MM-69643] Fail server startup when the AppsEnabled feature flag is enabled |
| https://github.com/mattermost/mattermost/pull/37648 | `mattermost/mattermost` | `code_and_docs` | `` | [MM-70221] Use request loggers in store methods |
| https://github.com/mattermost/mattermost/pull/37809 | `mattermost/mattermost` | `code_only` | `` | Data spillage exposure radius report generation |
| https://github.com/mattermost/mattermost/pull/38015 | `mattermost/mattermost` | `code_only_tests_or_fixtures` | `` | E2E/Test: Bump playwright workers from 15 to 20 |
| https://github.com/mattermost/mattermost/pull/37970 | `mattermost/mattermost` | `code_only` | `` | [MM-70252] Return 400 for malformed date filters in logs query API |
| https://github.com/mattermost/mattermost/pull/38003 | `mattermost/mattermost` | `code_only` | `` | [M-70285] Fix plugin settings section handling |
| https://github.com/mattermost/mattermost/pull/38032 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37809 |
| https://github.com/mattermost/mattermost/pull/37998 | `mattermost/mattermost` | `code_and_docs` | `` | Enforce snake_case for mlog field keys |
| https://github.com/mattermost/mattermost/pull/38021 | `mattermost/mattermost` | `code_and_docs` | `` | Remove dead Email login button color settings |
| https://github.com/mattermost/mattermost/pull/38023 | `mattermost/mattermost` | `code_and_docs` | `` | Graduate user typing settings to Site Configuration > Posts |
| https://github.com/mattermost/mattermost/pull/37875 | `mattermost/mattermost` | `code_only` | `` | [MM-69865] Add Delete row action to Manage Attributes |
| https://github.com/mattermost/mattermost/pull/37284 | `mattermost/mattermost` | `code_only` | `` | Remove atmos/camo image proxy support |
| https://github.com/mattermost/mattermost/pull/37285 | `mattermost/mattermost` | `code_only` | `` | Bump minimum supported Postgres version to v15 |
| https://github.com/mattermost/mattermost/pull/37496 | `mattermost/mattermost` | `code_only` | `` | MM-67510 Drop deprecated autotranslation column from ChannelMembers |
| https://github.com/mattermost/mattermost/pull/37283 | `mattermost/mattermost` | `code_only` | `` | [MM-68249] Drop support for OpenSearch v1.x |
| https://github.com/mattermost/mattermost/pull/37999 | `mattermost/mattermost` | `code_and_docs` | `` | Remove deprecated built-in Slack import API and CLI |
| https://github.com/mattermost/mattermost/pull/37759 | `mattermost/mattermost` | `code_and_docs` | `` | MM-68396: Remove deprecated dialog date/datetime fields for v12.0 |
| https://github.com/mattermost/mattermost/pull/37505 | `mattermost/mattermost` | `code_only` | `` | [MM-66243] Omit sanitized last_viewed_at/last_update_at instead of returning -1 for other users |
| https://github.com/mattermost/mattermost/pull/37820 | `mattermost/mattermost` | `code_only` | `` | Data spillage exposure radius UI integration |
| https://github.com/mattermost/mattermost/pull/37357 | `mattermost/mattermost` | `code_only` | `` | Fix link preview image layout shift by using SizeAwareImage |
| https://github.com/mattermost/mattermost/pull/37420 | `mattermost/mattermost` | `code_only` | `` | MM-69174 Fix most layout shift caused by images in posts |
| https://github.com/mattermost/mattermost/pull/38019 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38012 |
| https://github.com/mattermost/mattermost/pull/38012 | `mattermost/mattermost` | `code_only` | `` | MM-70294: Keep a collapse toggle for single video attachments |
| https://github.com/mattermost/mattermost/pull/38017 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #38012 |
| https://github.com/mattermost/mattermost/pull/38001 | `mattermost/mattermost` | `code_only` | `` | Disable TTL/grace period editing for server-derived attributes |
| https://github.com/mattermost/mattermost/pull/37202 | `mattermost/mattermost` | `code_only` | `` | Allow granting delegated administration roles from the Manage Roles modal |
| https://github.com/mattermost/mattermost/pull/38004 | `mattermost/mattermost` | `code_only` | `` | [MM-70283] Fix mixed custom-section fallback hiding valid plugin settings |
| https://github.com/mattermost/mattermost/pull/37163 | `mattermost/mattermost` | `code_only` | `` | [MM-67868] Remove deprecated Slack compatibility type aliases and functions |
| https://github.com/mattermost/mattermost/pull/37167 | `mattermost/mattermost` | `code_only` | `` | [MM-67157] Remove format parameter requirement from client license endpoint |
| https://github.com/mattermost/mattermost/pull/37997 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37818 |
| https://github.com/mattermost/mattermost/pull/37996 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37848 |
| https://github.com/mattermost/mattermost/pull/37994 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37818 |
| https://github.com/mattermost/mattermost/pull/37989 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37848 |
| https://github.com/mattermost/mattermost/pull/37993 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37848 |
| https://github.com/mattermost/mattermost/pull/37992 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37818 |
| https://github.com/mattermost/mattermost/pull/37991 | `mattermost/mattermost` | `code_only` | `` | Automated cherry pick of #37848 |
| https://github.com/PostHog/posthog/pull/91224 | `posthog/posthog` | `code_only` | `` | feat(desktop): pick a cloud environment or image, and star a favorite |
| https://github.com/PostHog/posthog/pull/91298 | `posthog/posthog` | `code_only` | `` | feat(signals): offer scout model pins as a dropdown |
| https://github.com/PostHog/posthog/pull/91264 | `posthog/posthog` | `code_only` | `` | fix(signals): accept report_id alias on inbox-reports-retrieve |
| https://github.com/PostHog/posthog/pull/89456 | `posthog/posthog` | `code_only` | `` | fix(data-warehouse): correct webhook step copy to not contradict the wizard's own gating |
| https://github.com/PostHog/posthog/pull/91247 | `posthog/posthog` | `code_only` | `` | fix(data-warehouse): treat S3 permission denials as transient in repartition |
| https://github.com/PostHog/posthog/pull/91239 | `posthog/posthog` | `code_only` | `` | fix(apple_search_ads): mark v5 API 400 responses as non-retryable |
| https://github.com/PostHog/posthog/pull/91171 | `posthog/posthog` | `code_only` | `` | feat(marketing-analytics): explain what the retention numbers mean |
| https://github.com/PostHog/posthog/pull/91256 | `posthog/posthog` | `code_only` | `` | fix(apple-search-ads): classify transient API 5xx and 429 as retryable |
| https://github.com/PostHog/posthog/pull/91029 | `posthog/posthog` | `code_only` | `` | feat(engineering-analytics): stack the three lead-time box plots on the Health tab |
| https://github.com/PostHog/posthog/pull/65 | `posthog/posthog` | `code_only` | `` | 61 fix action url not saving |
| https://github.com/PostHog/posthog/pull/88859 | `posthog/posthog` | `code_only` | `` | fix(new_relic): retry NerdGraph's generic NRDB error instead of failing the sync |
| https://github.com/PostHog/posthog/pull/90964 | `posthog/posthog` | `code_only` | `` | fix(mssql): suppress transient EOF-from-server errors from error tracking |
| https://github.com/PostHog/posthog/pull/90874 | `posthog/posthog` | `code_only` | `` | fix(langsmith): stop retrying on oversized API page response |
| https://github.com/PostHog/posthog/pull/89997 | `posthog/posthog` | `code_only` | `` | feat(warehouse_sources): support the Apple Ads Platform API v1 |
| https://github.com/PostHog/posthog/pull/91219 | `posthog/posthog` | `code_only` | `` | feat(desktop): add Open in new tab to task and canvas row context menu |
| https://github.com/PostHog/posthog/pull/91139 | `posthog/posthog` | `code_only` | `` | fix(surveys): filter lists before pagination |
| https://github.com/PostHog/posthog/pull/91199 | `posthog/posthog` | `code_only` | `` | chore(flags): remove starts-with-ends-with-operators flag |
| https://github.com/PostHog/posthog/pull/90492 | `posthog/posthog` | `code_and_docs` | `` | feat(pgapi): API + MCP server over the pgcollector stats database |
| https://github.com/PostHog/posthog/pull/91075 | `posthog/posthog` | `code_only` | `` | fix(desktop): suppress toasts for open task panels |
| https://github.com/PostHog/posthog/pull/90595 | `posthog/posthog` | `code_only` | `` | perf(marketing-analytics): bound the attribution fan-out per person |
| https://github.com/PostHog/posthog/pull/87287 | `posthog/posthog` | `code_only` | `` | fix(flags): count blast radius via HogQL, drop legacy PersonQuery |
| https://github.com/PostHog/posthog/pull/91098 | `posthog/posthog` | `code_only` | `` | feat(managed-warehouse): enroll onboarding orgs in the Trino cell |
| https://github.com/PostHog/posthog/pull/91153 | `posthog/posthog` | `code_only` | `` | chore(deps): Update @posthog/react-native-plugin to 2.5.1 |
| https://github.com/PostHog/posthog/pull/91130 | `posthog/posthog` | `code_only` | `` | fix(data-modeling): fall back to the untouched query when the DESCRIBE probe fails |
| https://github.com/PostHog/posthog/pull/91121 | `posthog/posthog` | `code_only` | `` | feat(mcp-analytics): add feedback survey button |
| https://github.com/PostHog/posthog/pull/90598 | `posthog/posthog` | `code_only` | `` | fix(desktop): open reports on the first click |
| https://github.com/PostHog/posthog/pull/91149 | `posthog/posthog` | `code_only` | `` | chore(deps): Update posthog-react-native to 4.66.2 |
| https://github.com/PostHog/posthog/pull/91039 | `posthog/posthog` | `code_only` | `` | fix(desktop): restore Command Center task actions |
| https://github.com/PostHog/posthog/pull/91160 | `posthog/posthog` | `code_and_docs` | `` | feat(product-empty-states): preview any empty state with ?empty_state=1 |
| https://github.com/PostHog/posthog/pull/91090 | `posthog/posthog` | `code_only` | `` | chore(dags): move skip_on_kill_switch to the shared dags module |
| https://github.com/PostHog/posthog/pull/88759 | `posthog/posthog` | `code_only_tests_or_fixtures` | `` | feat(autoresearch): cut backend test collection overhead |
| https://github.com/PostHog/posthog/pull/89797 | `posthog/posthog` | `code_only` | `` | feat(cohorts): sweep membership rows a completed reconcile did not assert |
| https://github.com/PostHog/posthog/pull/90952 | `posthog/posthog` | `code_and_docs` | `` | feat(eng-analytics): trunk quarantine debt scoreboard |
| https://github.com/PostHog/posthog/pull/90491 | `posthog/posthog` | `code_and_docs` | `` | feat(pgcollector): Postgres telemetry collector for RDS/Aurora |
| https://github.com/PostHog/posthog/pull/90615 | `posthog/posthog` | `code_only` | `` | chore(ingestion): extract the $os_name alias into normalizeOsAlias |
| https://github.com/PostHog/posthog/pull/83403 | `posthog/posthog` | `code_only` | `` | feat(flags): add evaluation context selector to experiment creation |
| https://github.com/PostHog/posthog/pull/91107 | `posthog/posthog` | `code_and_docs` | `` | fix(signals): stop scouts fetching built-in skills with skill-get |
| https://github.com/PostHog/posthog/pull/91074 | `posthog/posthog` | `code_and_docs` | `` | feat(mcp-analytics): gate intent clustering |
| https://github.com/PostHog/posthog/pull/91040 | `posthog/posthog` | `code_and_docs` | `` | fix(data-catalog): support dotted warehouse table names |
| https://github.com/PostHog/posthog/pull/90956 | `posthog/posthog` | `code_only` | `` | feat(signals): make the redesigned inbox welcome the default |
| https://github.com/PostHog/posthog/pull/91115 | `posthog/posthog` | `code_only` | `` | fix(warehouse-sources): escape column names in the s3 structure argument |
| https://github.com/PostHog/posthog/pull/90953 | `posthog/posthog` | `code_and_docs` | `` | chore(ci): alert and trace on the hourly master matrices |
| https://github.com/PostHog/posthog/pull/89631 | `posthog/posthog` | `code_and_docs` | `` | feat(metrics): create the metrics kafka ingest chain via migration |
| https://github.com/PostHog/posthog/pull/91054 | `posthog/posthog` | `code_only` | `` | chore(frontend): move FeaturePreviews out of layout into lib/components |
| https://github.com/PostHog/posthog/pull/90636 | `posthog/posthog` | `code_only` | `` | feat(desktop): add a dark appearance to the app icon |
| https://github.com/PostHog/posthog/pull/90618 | `posthog/posthog` | `code_only` | `` | feat(desktop): replace the loading gif with an animated SVG logo |
| https://github.com/PostHog/posthog/pull/90563 | `posthog/posthog` | `code_only` | `` | feat(nav): ship the nav search bar and remove the Cmd+K experiment |
| https://github.com/PostHog/posthog/pull/89057 | `posthog/posthog` | `code_only` | `` | test(backend): disable pytest exception cleanup plugins |
| https://github.com/PostHog/posthog/pull/51324 | `posthog/posthog` | `code_only` | `` | feat(experiments): create framework-free facade contract for experiments. |
| https://github.com/PostHog/posthog/pull/91108 | `posthog/posthog` | `code_only_tests_or_fixtures` | `` | fix(ingestion): stop the Rust consumer e2e from racing on worker ports |
| https://github.com/PostHog/posthog/pull/91071 | `posthog/posthog` | `code_only_tests_or_fixtures` | `` | chore(marketing-analytics): snapshot the attribution SQL |
| https://github.com/PostHog/posthog/pull/91020 | `posthog/posthog` | `code_only` | `` | feat(signals): split the scout roster's need-you stat into pausing soon and recently paused |
| https://github.com/PostHog/posthog/pull/90981 | `posthog/posthog` | `code_only` | `` | fix(mcp-analytics): paginate tool quality results |
| https://github.com/PostHog/posthog/pull/90779 | `posthog/posthog` | `code_only` | `` | fix(navigation): shorten navbar product tooltips to a tag and a line |
| https://github.com/PostHog/posthog/pull/90241 | `posthog/posthog` | `code_and_docs` | `` | feat(mcp-store): share new MCP connections with every agent by default |
| https://github.com/PostHog/posthog/pull/88029 | `posthog/posthog` | `code_only` | `` | feat(marketing-analytics): compare channels side by side in retention |
| https://github.com/PostHog/posthog/pull/87269 | `posthog/posthog` | `code_only` | `` | feat(wizard): mint scoped gateway tokens per run |
| https://github.com/PostHog/posthog/pull/88928 | `posthog/posthog` | `code_only` | `` | fix(warehouse): reconcile property definition provenance |
| https://github.com/PostHog/posthog/pull/91003 | `posthog/posthog` | `code_only` | `` | fix(notebooks): make the variables bar as wide as the notebook |
| https://github.com/PostHog/posthog/pull/90966 | `posthog/posthog` | `code_only` | `` | chore(deps): Update posthog-js to 1.422.5 |
| https://github.com/PostHog/posthog/pull/91056 | `posthog/posthog` | `code_only` | `` | fix(web-analytics): stitch live today into precomputed trend charts |
| https://github.com/PostHog/posthog/pull/90973 | `posthog/posthog` | `code_only` | `` | fix(engineering-analytics): scope PR-list CI rollups to visible PRs |
| https://github.com/PostHog/posthog/pull/90936 | `posthog/posthog` | `code_only` | `` | fix(mcp-analytics): open low-volume projects on activity |
| https://github.com/PostHog/posthog/pull/91030 | `posthog/posthog` | `code_only` | `` | chore(clickhouse): match events_recent ttl to production at 9 days |
| https://github.com/PostHog/posthog/pull/90832 | `posthog/posthog` | `code_only` | `` | feat(mcp): add event-definition-create tool |
| https://github.com/PostHog/posthog/pull/90568 | `posthog/posthog` | `code_only` | `` | feat(max): ship product-grouped capability badges and remove the experiment |
| https://github.com/PostHog/posthog/pull/86764 | `posthog/posthog` | `code_only` | `` | chore(oauth): drop the cimd_metadata_url column |
| https://github.com/PostHog/posthog/pull/91028 | `posthog/posthog` | `code_only_tests_or_fixtures` | `` | chore(signals): wait for legacy inbox story to load |
| https://github.com/PostHog/posthog/pull/90725 | `posthog/posthog` | `code_only` | `` | feat(logs): expose pattern columns in hogql |
| https://github.com/PostHog/posthog/pull/89677 | `posthog/posthog` | `code_only` | `` | feat(ci): shadow per-team slices in weekly flaky report |
| https://github.com/PostHog/posthog/pull/86909 | `posthog/posthog` | `code_only` | `` | feat(marketing-analytics): retention explorer tab |
| https://github.com/PostHog/posthog/pull/90805 | `posthog/posthog` | `code_only` | `` | feat(insights): copy an insight chart to the clipboard as an image |
| https://github.com/PostHog/posthog/pull/90579 | `posthog/posthog` | `code_only` | `` | refactor(cdp): render the filter taxonomy from the real taxonomy |
| https://github.com/PostHog/posthog/pull/90499 | `posthog/posthog` | `code_only` | `` | fix(ci): install protoc for the replay vision eval workflow |
| https://github.com/PostHog/posthog/pull/90421 | `posthog/posthog` | `code_only` | `` | feat(desktop): add organization beta consent controls |
| https://github.com/PostHog/posthog/pull/90409 | `posthog/posthog` | `code_only` | `` | chore(temporal): use itertools.batched instead of local copies |
| https://github.com/PostHog/posthog/pull/86452 | `posthog/posthog` | `code_only` | `` | fix(insights): give the insight Duplicate button loading and failure feedback |
| https://github.com/PostHog/posthog/pull/90404 | `posthog/posthog` | `code_only` | `` | fix(aio): mask short provider keys with the shared masker |
| https://github.com/PostHog/posthog/pull/90400 | `posthog/posthog` | `code_only` | `` | chore(egress): route github public-keys fetch through egress |
| https://github.com/PostHog/posthog/pull/91000 | `posthog/posthog` | `code_only` | `` | chore(alerts): drop always-true alerts-investigation-agent flag check |
| https://github.com/PostHog/posthog/pull/90619 | `posthog/posthog` | `code_only` | `` | feat(growth): move product suggestions off UserProductList.reason |
| https://github.com/PostHog/posthog/pull/90240 | `posthog/posthog` | `code_only` | `` | fix(signals): stop exec from advertising gateway tools to scout runs |
| https://github.com/PostHog/posthog/pull/84088 | `posthog/posthog` | `code_and_docs` | `` | chore(ci): make weekly flaky report informational |
| https://github.com/PostHog/posthog/pull/90999 | `posthog/posthog` | `code_only` | `` | fix(desktop): always include task attribution |
| https://github.com/PostHog/posthog/pull/90908 | `posthog/posthog` | `code_only` | `` | fix(tasks): report whether a Pi steer landed |
| https://github.com/PostHog/posthog/pull/90890 | `posthog/posthog` | `code_only` | `` | fix(integrations): send Resend OAuth to the correct authorize host |
| https://github.com/PostHog/posthog/pull/90855 | `posthog/posthog` | `code_and_docs` | `` | fix(tasks): reserve a cpu floor for dev-stack image sandboxes |
| https://github.com/PostHog/posthog/pull/90676 | `posthog/posthog` | `code_only` | `` | fix(skills): cap skill descriptions at the 1024 spec limit |
| https://github.com/PostHog/posthog/pull/90544 | `posthog/posthog` | `code_only` | `` | perf(data-modeling): stop DESCRIBE from scanning subqueries |
| https://github.com/PostHog/posthog/pull/90537 | `posthog/posthog` | `code_only` | `` | feat(clickhouse): refresh native-tcp pool credentials from a file |
| https://github.com/PostHog/posthog/pull/89938 | `posthog/posthog` | `code_only` | `` | feat(notebooks): limit how many cell runs execute at once |
| https://github.com/PostHog/posthog/pull/90967 | `posthog/posthog` | `code_only` | `` | feat(logs): point the empty logs state at drop rules |
| https://github.com/PostHog/posthog/pull/90875 | `posthog/posthog` | `code_only` | `` | feat(workflows): send a test email from the template library editor |
| https://github.com/PostHog/posthog/pull/90176 | `posthog/posthog` | `code_only` | `` | fix(funnels): apply step renames made outside the rename modal |
| https://github.com/PostHog/posthog/pull/89978 | `posthog/posthog` | `code_only` | `` | feat(desktop): render http(s) step details as external links |
| https://github.com/PostHog/posthog/pull/90955 | `posthog/posthog` | `code_only` | `` | chore(health): drop beta banners from health pages |
| https://github.com/PostHog/posthog/pull/90945 | `posthog/posthog` | `code_only` | `` | fix(replay): clamp down to 15000 mutations in second |
| https://github.com/PostHog/posthog/pull/90857 | `posthog/posthog` | `code_and_docs` | `` | feat(warehouse_sources): add Tally folders and form analytics metrics tables |
| https://github.com/PostHog/posthog/pull/90848 | `posthog/posthog` | `code_and_docs` | `` | feat(warehouse_sources): add Zonka Feedback survey_links table |
| https://github.com/PostHog/posthog/pull/90800 | `posthog/posthog` | `code_only` | `` | fix(google_ads): default report tables to segments.date incremental field |
| https://github.com/PostHog/posthog/pull/90793 | `posthog/posthog` | `code_only` | `` | fix(clerk): stop failing the invitations sync on a 404 not-found |
| https://github.com/PostHog/posthog/pull/90760 | `posthog/posthog` | `code_only` | `` | fix(data-imports): silence closed-connection noise from stranded-run reconcile sweep |
| https://github.com/PostHog/posthog/pull/90313 | `posthog/posthog` | `code_only` | `` | fix(customer-analytics): let users manage own Google connection |
| https://github.com/PostHog/posthog/pull/90944 | `posthog/posthog` | `code_only` | `` | fix(batch-exports): bump Snowflake login timeout from 5s to 20s |
| https://github.com/PostHog/posthog/pull/90900 | `posthog/posthog` | `code_only` | `` | fix(desktop): trust Pi task folders |
| https://github.com/PostHog/posthog/pull/90898 | `posthog/posthog` | `code_only` | `` | feat(warehouse_sources): list a source's schemas on its admin page |
| https://github.com/PostHog/posthog/pull/90836 | `posthog/posthog` | `code_only` | `` | fix(desktop): keep Pi session loading state |
| https://github.com/PostHog/posthog/pull/90790 | `posthog/posthog` | `code_and_docs` | `` | chore(ingestion): remove the HTTP transport between consumer and workers |
| https://github.com/PostHog/posthog/pull/90513 | `posthog/posthog` | `code_only` | `` | chore(experiments): experiments scene product migration constants |
| https://github.com/PostHog/posthog/pull/90203 | `posthog/posthog` | `code_only` | `` | fix(devbox): verify devbox commit signing at setup |
| https://github.com/metabase/metabase/pull/80551 | `metabase/metabase` | `code_only` | `` | update driver-test-results with missing driver tests |
| https://github.com/metabase/metabase/pull/80760 | `metabase/metabase` | `code_only` | `` | Remove ability to skip test suites upfront |
| https://github.com/metabase/metabase/pull/80594 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Cover DB management permissions with targetted tests |
| https://github.com/metabase/metabase/pull/80614 | `metabase/metabase` | `code_only` | `` | GDGT-3141 [Flaky Test]: should render saved top level blocks |
| https://github.com/metabase/metabase/pull/80133 | `metabase/metabase` | `code_only` | `` | Support Anthropic partner models via the Google provider |
| https://github.com/metabase/metabase/pull/81237 | `metabase/metabase` | `code_and_docs` | `` | Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command |
| https://github.com/metabase/metabase/pull/81444 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v61 backported "Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command" |
| https://github.com/metabase/metabase/pull/81441 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v62 backported "Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command" |
| https://github.com/metabase/metabase/pull/81445 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v60 backported "Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command" |
| https://github.com/metabase/metabase/pull/81442 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v58 backported "Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command" |
| https://github.com/metabase/metabase/pull/81446 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v59 backported "Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command" |
| https://github.com/metabase/metabase/pull/81443 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v63 backported "Never encrypt the app DB on startup when there is existing data; add `enable-encryption` command" |
| https://github.com/metabase/metabase/pull/81081 | `metabase/metabase` | `code_only` | `` | Encrypt security-sensitive settings at rest |
| https://github.com/metabase/metabase/pull/80397 | `metabase/metabase` | `code_only` | `` | Fix flaky remote-sync branch-switch e2e test |
| https://github.com/metabase/metabase/pull/81399 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "Fix flaky remote-sync branch-switch e2e test" |
| https://github.com/metabase/metabase/pull/81398 | `metabase/metabase` | `code_only` | `` | 🤖 v59 backported "Fix flaky remote-sync branch-switch e2e test" |
| https://github.com/metabase/metabase/pull/81400 | `metabase/metabase` | `code_only` | `` | 🤖 v60 backported "Fix flaky remote-sync branch-switch e2e test" |
| https://github.com/metabase/metabase/pull/81403 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "Fix flaky remote-sync branch-switch e2e test" |
| https://github.com/metabase/metabase/pull/81401 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Fix flaky remote-sync branch-switch e2e test" |
| https://github.com/metabase/metabase/pull/81228 | `metabase/metabase` | `code_only` | `` | bump dompurify to 3.4.14; removed from resolutions |
| https://github.com/metabase/metabase/pull/81309 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "bump dompurify to 3.4.14; removed from resolutions" |
| https://github.com/metabase/metabase/pull/81229 | `metabase/metabase` | `code_only` | `` | Bump js-yaml to 4.3.1 |
| https://github.com/metabase/metabase/pull/81310 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "bump dompurify to 3.4.14; removed from resolutions" |
| https://github.com/metabase/metabase/pull/81313 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "Bump js-yaml to 4.3.1" |
| https://github.com/metabase/metabase/pull/81315 | `metabase/metabase` | `code_only` | `` | 🤖 v60 backported "Bump js-yaml to 4.3.1" |
| https://github.com/metabase/metabase/pull/81416 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Temporarily disable Shoppy sample app tests |
| https://github.com/metabase/metabase/pull/81417 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v63 backported "Temporarily disable Shoppy sample app tests" |
| https://github.com/metabase/metabase/pull/81419 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v61 backported "Temporarily disable Shoppy sample app tests" |
| https://github.com/metabase/metabase/pull/81421 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v60 backported "Temporarily disable Shoppy sample app tests" |
| https://github.com/metabase/metabase/pull/81418 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v62 backported "Temporarily disable Shoppy sample app tests" |
| https://github.com/metabase/metabase/pull/81241 | `metabase/metabase` | `code_only` | `` | Add Databricks Workspace Sharding |
| https://github.com/metabase/metabase/pull/81314 | `metabase/metabase` | `code_only` | `` | 🤖 v59 backported "Bump js-yaml to 4.3.1" |
| https://github.com/metabase/metabase/pull/81312 | `metabase/metabase` | `code_only` | `` | 🤖 v58 backported "Bump js-yaml to 4.3.1" |
| https://github.com/metabase/metabase/pull/81369 | `metabase/metabase` | `code_only` | `` | Cache clojure cli download |
| https://github.com/metabase/metabase/pull/81385 | `metabase/metabase` | `code_only` | `` | 🤖 v58 backported "Cache clojure cli download" |
| https://github.com/metabase/metabase/pull/79128 | `metabase/metabase` | `code_only` | `` | Metrics explorer editor race fix (fixes a bunch of flaky tests) |
| https://github.com/metabase/metabase/pull/81387 | `metabase/metabase` | `code_only` | `` | 🤖 v59 backported "Cache clojure cli download" |
| https://github.com/metabase/metabase/pull/81389 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "Cache clojure cli download" |
| https://github.com/metabase/metabase/pull/81317 | `metabase/metabase` | `code_and_docs` | `` | Remove entity ids from data_app.yaml |
| https://github.com/metabase/metabase/pull/81384 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "Cache clojure cli download" |
| https://github.com/metabase/metabase/pull/81382 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Dwh gc parallel |
| https://github.com/metabase/metabase/pull/74973 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Hide all tenant groups/users from perms graph api |
| https://github.com/metabase/metabase/pull/81386 | `metabase/metabase` | `code_only` | `` | 🤖 v60 backported "Cache clojure cli download" |
| https://github.com/metabase/metabase/pull/81388 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Cache clojure cli download" |
| https://github.com/metabase/metabase/pull/77401 | `metabase/metabase` | `code_only` | `` | Make `isRenderedWithinViewport` retry until element settles in viewport |
| https://github.com/metabase/metabase/pull/81364 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "Make `isRenderedWithinViewport` retry until element settles in viewport" |
| https://github.com/metabase/metabase/pull/81360 | `metabase/metabase` | `code_only` | `` | 🤖 v59 backported "Make `isRenderedWithinViewport` retry until element settles in viewport" |
| https://github.com/metabase/metabase/pull/79849 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Cleanup data warehouses nightly |
| https://github.com/metabase/metabase/pull/81362 | `metabase/metabase` | `code_only` | `` | 🤖 v58 backported "Make `isRenderedWithinViewport` retry until element settles in viewport" |
| https://github.com/metabase/metabase/pull/81361 | `metabase/metabase` | `code_only` | `` | 🤖 v60 backported "Make `isRenderedWithinViewport` retry until element settles in viewport" |
| https://github.com/metabase/metabase/pull/81227 | `metabase/metabase` | `code_only` | `` | Encrypt subscription/alert recipient details; enforce allow-list on send |
| https://github.com/metabase/metabase/pull/81326 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "Encrypt subscription/alert recipient details; enforce allow-list on send" |
| https://github.com/metabase/metabase/pull/81365 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "Make `isRenderedWithinViewport` retry until element settles in viewport" |
| https://github.com/metabase/metabase/pull/81352 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Wait for the content-translation dictionary in the SDK rerender spec |
| https://github.com/metabase/metabase/pull/81363 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Make `isRenderedWithinViewport` retry until element settles in viewport" |
| https://github.com/metabase/metabase/pull/81330 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Encrypt subscription/alert recipient details; enforce allow-list on send" |
| https://github.com/metabase/metabase/pull/81214 | `metabase/metabase` | `code_only` | `` | Fix lint-eslint-pure warning noise in fresh worktrees |
| https://github.com/metabase/metabase/pull/81327 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "Encrypt subscription/alert recipient details; enforce allow-list on send" |
| https://github.com/metabase/metabase/pull/81329 | `metabase/metabase` | `code_only` | `` | 🤖 v60 backported "Encrypt subscription/alert recipient details; enforce allow-list on send" |
| https://github.com/metabase/metabase/pull/80467 | `metabase/metabase` | `code_and_docs` | `` | [GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon |
| https://github.com/metabase/metabase/pull/80983 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v59 backported "[GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon" |
| https://github.com/metabase/metabase/pull/81331 | `metabase/metabase` | `code_only` | `` | 🤖 v59 backported "Encrypt subscription/alert recipient details; enforce allow-list on send" |
| https://github.com/metabase/metabase/pull/80984 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v58 backported "[GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon" |
| https://github.com/metabase/metabase/pull/80761 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Stabilize Embedding Parameters test |
| https://github.com/metabase/metabase/pull/81022 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v60 backported "Stabilize Embedding Parameters test" |
| https://github.com/metabase/metabase/pull/81026 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v59 backported "Stabilize Embedding Parameters test" |
| https://github.com/metabase/metabase/pull/81025 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v58 backported "Stabilize Embedding Parameters test" |
| https://github.com/metabase/metabase/pull/81332 | `metabase/metabase` | `code_only` | `` | Match permissions URLs for databases without schemas |
| https://github.com/metabase/metabase/pull/81027 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | 🤖 v61 backported "Stabilize Embedding Parameters test" |
| https://github.com/metabase/metabase/pull/81234 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | Delete broken "Transforms" test from release-x.60.x |
| https://github.com/metabase/metabase/pull/80494 | `metabase/metabase` | `code_only` | `` | Check embedding saml popup source |
| https://github.com/metabase/metabase/pull/80670 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Check embedding saml popup source" |
| https://github.com/metabase/metabase/pull/79355 | `metabase/metabase` | `code_only` | `` | Sever visualizer, custom-viz and data-grid edges |
| https://github.com/metabase/metabase/pull/80810 | `metabase/metabase` | `code_only_tests_or_fixtures` | `` | [Backport v60] Fix flaky embedding-hub sandbox column-update test |
| https://github.com/metabase/metabase/pull/80981 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v62 backported "[GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon" |
| https://github.com/metabase/metabase/pull/80979 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v63 backported "[GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon" |
| https://github.com/metabase/metabase/pull/80982 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v60 backported "[GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon" |
| https://github.com/metabase/metabase/pull/81316 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "Bump js-yaml to 4.3.1" |
| https://github.com/metabase/metabase/pull/81306 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "bump dompurify to 3.4.14; removed from resolutions" |
| https://github.com/metabase/metabase/pull/81311 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Bump js-yaml to 4.3.1" |
| https://github.com/metabase/metabase/pull/81300 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Fix collapsed visualization in the dashboard new-question query builder" |
| https://github.com/metabase/metabase/pull/80980 | `metabase/metabase` | `code_and_docs` | `` | 🤖 v61 backported "[GDGT-3088] gate slack bug reports on bug-reporting-enabled and enforce attribution to session user when non-anon" |
| https://github.com/metabase/metabase/pull/81163 | `metabase/metabase` | `code_only` | `` | Fix collapsed visualization in the dashboard new-question query builder |
| https://github.com/metabase/metabase/pull/81045 | `metabase/metabase` | `code_only` | `` | 🤖 v63 backported "Fix tenant collections showing up as unknown in the dashboard question picker" |
| https://github.com/metabase/metabase/pull/81046 | `metabase/metabase` | `code_only` | `` | 🤖 v62 backported "Fix tenant collections showing up as unknown in the dashboard question picker" |
| https://github.com/metabase/metabase/pull/81047 | `metabase/metabase` | `code_only` | `` | 🤖 v61 backported "Fix tenant collections showing up as unknown in the dashboard question picker" |
| https://github.com/metabase/metabase/pull/81043 | `metabase/metabase` | `code_only` | `` | 🤖 v60 backported "Fix tenant collections showing up as unknown in the dashboard question picker" |
| https://github.com/metabase/metabase/pull/80671 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Check embedding saml popup source" |
| https://github.com/metabase/metabase/pull/80672 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Check embedding saml popup source" |
| https://github.com/metabase/metabase/pull/80673 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Check embedding saml popup source" |
| https://github.com/metabase/metabase/pull/80674 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Check embedding saml popup source" |
| https://github.com/metabase/metabase/pull/81147 | `metabase/metabase` | `code_only` | `` | Write the metadata mirror from one listener, not 33 endpoint hookups |
| https://github.com/metabase/metabase/pull/80970 | `metabase/metabase` | `code_only` | `` | Name the chunks that lazy routes load |
| https://github.com/metabase/metabase/pull/81280 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Metrics explorer editor race fix (fixes a bunch of flaky tests)" |
| https://github.com/metabase/metabase/pull/81157 | `metabase/metabase` | `code_only` | `` | Keep MCP node_modules out of the shared vendor chunk |
| https://github.com/metabase/metabase/pull/68607 | `metabase/metabase` | `code_only` | `` | Fix: Support Google Cloud Universe Domain in BigQuery driver |
| https://github.com/metabase/metabase/pull/79101 | `metabase/metabase` | `code_only` | `` | Skip fields when browsing tables of a schema-less database |
| https://github.com/metabase/metabase/pull/80396 | `metabase/metabase` | `code_only` | `` | Fix flaky remote-sync conflict-modal e2e test |
| https://github.com/metabase/metabase/pull/79103 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Skip fields when browsing tables of a schema-less database" |
| https://github.com/metabase/metabase/pull/80707 | `metabase/metabase` | `code_only` | `` | 🤖 backported "Fix flaky remote-sync conflict-modal e2e test" |

## Reject Summary Sample

| Repository | PR | Reason | Bucket |
| --- | ---: | --- | --- |
| `godotengine/godot` | `122734` | `not_merged` | `None` |
| `godotengine/godot` | `109195` | `not_merged` | `None` |
| `godotengine/godot` | `120648` | `not_merged` | `None` |
| `godotengine/godot` | `110954` | `not_merged` | `None` |
| `godotengine/godot` | `122969` | `not_merged` | `None` |
| `godotengine/godot` | `122839` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `122877` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `122914` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `82532` | `not_merged` | `None` |
| `godotengine/godot` | `122937` | `not_merged` | `None` |
| `godotengine/godot` | `122864` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `122896` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `122826` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `83761` | `not_merged` | `None` |
| `godotengine/godot` | `122890` | `not_merged` | `None` |
| `godotengine/godot` | `115554` | `not_merged` | `None` |
| `godotengine/godot` | `120429` | `not_merged` | `None` |
| `godotengine/godot` | `122678` | `not_merged` | `None` |
| `godotengine/godot` | `114188` | `not_merged` | `None` |
| `godotengine/godot` | `122868` | `not_merged` | `None` |
| `godotengine/godot` | `122797` | `not_merged` | `None` |
| `godotengine/godot` | `114158` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `120866` | `not_merged` | `None` |
| `godotengine/godot` | `122305` | `not_merged` | `None` |
| `godotengine/godot` | `122817` | `not_merged` | `None` |
| `godotengine/godot` | `122810` | `not_merged` | `None` |
| `godotengine/godot` | `122812` | `not_merged` | `None` |
| `godotengine/godot` | `122727` | `not_merged` | `None` |
| `godotengine/godot` | `114462` | `not_merged` | `None` |
| `godotengine/godot` | `122435` | `not_merged` | `None` |
| `godotengine/godot` | `122436` | `not_merged` | `None` |
| `godotengine/godot` | `122476` | `not_merged` | `None` |
| `godotengine/godot` | `122440` | `not_merged` | `None` |
| `godotengine/godot` | `122794` | `not_merged` | `None` |
| `godotengine/godot` | `120426` | `not_merged` | `None` |
| `godotengine/godot` | `122800` | `not_merged` | `None` |
| `godotengine/godot` | `122787` | `not_merged` | `None` |
| `godotengine/godot` | `122788` | `not_merged` | `None` |
| `godotengine/godot` | `122792` | `not_merged` | `None` |
| `godotengine/godot` | `122790` | `not_merged` | `None` |
| `godotengine/godot` | `118899` | `not_merged` | `None` |
| `godotengine/godot` | `83903` | `not_merged` | `None` |
| `godotengine/godot` | `122778` | `not_merged` | `None` |
| `godotengine/godot` | `120789` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `122775` | `not_merged` | `None` |
| `godotengine/godot` | `122717` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `godotengine/godot` | `115537` | `not_merged` | `None` |
| `godotengine/godot` | `122762` | `not_merged` | `None` |
| `godotengine/godot` | `107242` | `not_merged` | `None` |
| `godotengine/godot` | `122017` | `not_merged` | `None` |
| `godotengine/godot` | `101340` | `not_merged` | `None` |
| `godotengine/godot` | `122712` | `not_merged` | `None` |
| `godotengine/godot` | `122733` | `not_merged` | `None` |
| `godotengine/godot` | `59444` | `not_merged` | `None` |
| `godotengine/godot` | `122722` | `not_merged` | `None` |
| `godotengine/godot` | `122747` | `not_merged` | `None` |
| `godotengine/godot` | `122710` | `not_merged` | `None` |
| `godotengine/godot` | `122731` | `not_merged` | `None` |
| `godotengine/godot` | `122627` | `not_merged` | `None` |
| `godotengine/godot` | `115593` | `not_merged` | `None` |
| `godotengine/godot` | `122698` | `not_merged` | `None` |
| `godotengine/godot` | `122168` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35597` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35598` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35594` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35590` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35340` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35560` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `ethereum/go-ethereum` | `35536` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35424` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35444` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `32818` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `33707` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35532` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35556` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35562` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35568` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `ethereum/go-ethereum` | `35336` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `ethereum/go-ethereum` | `35313` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `33837` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34063` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35440` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35540` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35549` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `32069` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34779` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `33879` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34789` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35290` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34788` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35538` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35453` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35511` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34091` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35445` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35437` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35438` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35139` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35507` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `122` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35517` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35522` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35492` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35500` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35516` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35297` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35326` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35294` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35487` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35505` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34886` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35491` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35494` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35160` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34994` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35452` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35456` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35434` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `22897` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35432` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35073` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `ethereum/go-ethereum` | `33954` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35414` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35375` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35422` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `ethereum/go-ethereum` | `35416` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35419` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35409` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35417` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35420` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35274` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `34089` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `31748` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `32169` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35142` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35183` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35401` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35361` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35398` | `not_merged` | `None` |
| `ethereum/go-ethereum` | `35064` | `not_merged` | `None` |
| `dapr/dapr` | `10417` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10418` | `docs_only_excluded` | `docs_only` |
| `dapr/dapr` | `10412` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10202` | `not_merged` | `None` |
| `dapr/dapr` | `10390` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10392` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10299` | `not_merged` | `None` |
| `dapr/dapr` | `10298` | `not_merged` | `None` |
| `dapr/dapr` | `10376` | `not_merged` | `None` |
| `dapr/dapr` | `10375` | `not_merged` | `None` |
| `dapr/dapr` | `10368` | `fetch_pr_files_failed` | `None` |
| `dapr/dapr` | `10362` | `docs_only_excluded` | `docs_only` |
| `dapr/dapr` | `10360` | `not_merged` | `None` |
| `dapr/dapr` | `10361` | `not_merged` | `None` |
| `dapr/dapr` | `10357` | `docs_only_excluded` | `docs_only` |
| `dapr/dapr` | `9782` | `not_merged` | `None` |
| `dapr/dapr` | `9807` | `not_merged` | `None` |
| `dapr/dapr` | `10270` | `not_merged` | `None` |
| `dapr/dapr` | `10306` | `not_merged` | `None` |
| `dapr/dapr` | `10295` | `not_merged` | `None` |
| `dapr/dapr` | `10296` | `not_merged` | `None` |
| `dapr/dapr` | `10269` | `not_merged` | `None` |
| `dapr/dapr` | `9736` | `not_merged` | `None` |
| `dapr/dapr` | `10098` | `not_merged` | `None` |
| `dapr/dapr` | `10268` | `not_merged` | `None` |
| `dapr/dapr` | `10297` | `not_merged` | `None` |
| `dapr/dapr` | `9824` | `not_merged` | `None` |
| `dapr/dapr` | `10277` | `not_merged` | `None` |
| `dapr/dapr` | `10279` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10259` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10258` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `dapr/dapr` | `10255` | `not_merged` | `None` |
| `dapr/dapr` | `10096` | `not_merged` | `None` |
| `dapr/dapr` | `10241` | `not_merged` | `None` |
| `rust-lang/rust` | `161980` | `not_merged` | `None` |
| `rust-lang/rust` | `159658` | `too_many_changed_files` | `code_and_docs` |
| `rust-lang/rust` | `161784` | `not_merged` | `None` |
| `rust-lang/rust` | `135931` | `not_merged` | `None` |
| `rust-lang/rust` | `161914` | `docs_only_excluded` | `docs_only` |
| `rust-lang/rust` | `161590` | `not_merged` | `None` |
| `rust-lang/rust` | `161952` | `not_merged` | `None` |
| `rust-lang/rust` | `161955` | `not_merged` | `None` |
| `rust-lang/rust` | `161899` | `other_or_binary_only_excluded` | `other_or_binary_only` |
| `rust-lang/rust` | `161949` | `not_merged` | `None` |
| `rust-lang/rust` | `161942` | `not_merged` | `None` |
| `rust-lang/rust` | `161939` | `not_merged` | `None` |
| `rust-lang/rust` | `161906` | `too_many_changed_files` | `code_only` |
| `rust-lang/rust` | `161934` | `not_merged` | `None` |
| `rust-lang/rust` | `159103` | `too_many_changed_files` | `code_only` |
| `rust-lang/rust` | `160088` | `not_merged` | `None` |
| `rust-lang/rust` | `152620` | `not_merged` | `None` |
| `rust-lang/rust` | `160973` | `not_merged` | `None` |
| `rust-lang/rust` | `161911` | `not_merged` | `None` |
| `rust-lang/rust` | `161872` | `not_merged` | `None` |
| `rust-lang/rust` | `161398` | `too_many_changed_files` | `code_only` |
| `rust-lang/rust` | `161884` | `not_merged` | `None` |
| `rust-lang/rust` | `161905` | `not_merged` | `None` |
| `rust-lang/rust` | `161901` | `not_merged` | `None` |
| `rust-lang/rust` | `160824` | `not_merged` | `None` |
| `rust-lang/rust` | `156034` | `not_merged` | `None` |