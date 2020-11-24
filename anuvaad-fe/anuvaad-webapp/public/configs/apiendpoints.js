const endpoints = {
  interactive_translate: "/interactive-translation",
  interactive_translate_v1: "/v1/interactive-translation",
  interactivesourceupdate: "/v1/interactive-editor/update-pdf-source-sentences",
  fetchfeedbackpending: "/check-feedback-pending",
  fetchlanguage: "/fetch-languages",
  fetchmodel: "/fetch-models",
  fetchmtworkspace: "/fetch-mt-workspace",
  fetchmtworkspacedetails: "/fetch-mt-workspace-detail",
  fetchpdf: "/v1/interactive-editor/fetch-pdf-parse-process",
  fetchpdfsentence: "/v1/interactive-editor/fetch-pdf-sentences",
  fetchquestions: "/fetch-feedback-questions",
  fetchsearchreplace: "/fetch-search-replace-sentence",
  fetchsearchreplacedetails: "/fetch-search-replace-workspace-detail",
  fetchsearchreplaceworkspace: "/fetch-search-replace-workspace",
  fetchtranslation: "/fetch-translation-process",
  fetchworkspace: "/fetch-paragraph-workspace",
  fetchworkspacedetails: "/fetch-paragraph-workspace-detail",
  forgotpassword: "/v1/user/forgot-user-password",
  graderreport: "/fetch-benchmark-reports",
  html_to_doc: "/html-to-doc",
  fetchducuments: '/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk',
  insertSentence: "/v1/interactive-editor/add-sentence-node",
  interactivesavesentence: "/v1/interactive-editor/update-pdf-sentences",
  interactivesourceupdate: "/v1/interactive-editor/update-pdf-source-sentences",
  InteractiveMerge: "/v1/interactive-editor/merge-split-sentence",
  acceptallsentence: "/accept-all-search-replace-sentence",
  activate_user: "/v1/user/activate-account",
  adduser: "/create-user",
  auto_ml: "/translate",
  fetch_filedeatils:"/api/v0/serve-file?",
  benchmark: "/fetch-benchmarks",
  benchmarktranslate: "/translate-with-hemat",
  comparisonreport: "/fetch-benchmark-analyzer-reports",
  compostionworkspace: "/save-composition-workspace",
  configupload: "/upload",
  corp: "/fetch-corpus",
  corpus: "/multiple",
  ocrpdffileupload:'/v2/interactive-editor/translate-pdf',
  createcorpus: "/upload-corpus",
  createworkspace: "/save-mt-workspace",
  deletefile: "/remove-process",
  downloaddoc: "/v1/interactive-editor/make-doc-from-sentences",
  fetchcompositionworkspace: "/fetch-composition-workspace",
  fetchcourtlist: "/fetch-high-courts",
  fetchdefaultconfig: "/fetch-default-config",
  fetchenchmarkcomparemodel: "/fetch-benchmark-compare-sentences",
  deleteSentence: "/v1/interactive-editor/delete-sentence",
  deleteTable: "/v1/interactive-editor/delete-table-sentence",
  fetchcompositionworkspacedetails: "/fetch-composition-workspace-detail",
  fetchenchmarkmodel: "/fetch-benchmark-sentences",
  pdffileupload: "/v1/interactive-editor/translate-pdf",
  workflow:"/anuvaad-etl/wf-manager/v1/workflow/initiate",
  signup: "/v1/user/signup-user",
  updatePdfTable: "/v1/interactive-editor/update-pdf-source-table",
  login: "/sysuser/login",
  nmt: "/translation_en",
  pdffile: "/upload",
  pdftodoc: "/convert-pdf-to-doc",
  qna: "/api",
  questionupload: "/save-feedback-questions",
  runexperiment: "/save-paragraph-workspace",
  savedatasource: "/save-mt-workspace-data",
  savefeedback: "/save-captured-feedback",
  savesearchreplaceworkspace: "/save-search-replace-workspace",
  savetool2datasource: "/save-paragraph-workspace-data",
  sentencereplace: "/update-search-replace-sentence",
  setpassword: "/set-user-password",
  documentupload:"/anuvaad-api/file-uploader/v0/upload-file",
  fecthcontent: "/api/v0/fetch-content"
};

export default endpoints;
