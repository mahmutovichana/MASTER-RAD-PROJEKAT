export type PatchMode = 'append_to_section' | 'replace_section' | 'append_to_file';

export interface DocGuardPatch {
  file: string;
  mode: PatchMode;
  section: string;
  text: string;
  preview: string;
  backend?: string;
  model_name?: string;
  generation_status?: string;
  generation_error?: string;
  postprocess_status?: string;
  verifier_status?: string;
  quality_label?: string;
  hallucination_risk?: string;
  grounded_tokens_found?: string[];
  warnings?: string[];
  fallback_patch?: DocGuardPatch;
}

export interface DocGuardResult {
  status: 'ok' | 'error';
  docs_update_required: boolean;
  doc_category: string;
  target_doc_file: string | null;
  target_section: string;
  scenario_type: string;
  confidence: number;
  reason: string;
  patch: DocGuardPatch | null;
  diagnostics: {
    changed_files: string[];
    model_used: string;
    classifier_architecture: string;
    input_mode: string;
    patch_backend?: string;
    patch_model?: string;
    analysis_backend?: string;
    analysis_model?: string;
    analysis_status?: string;
    analysis_error?: string;
    analysis_raw_decision?: string;
    runtime_ms: number;
  };
  error_message: string | null;
}
