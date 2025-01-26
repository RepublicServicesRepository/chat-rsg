// To change the supported text format files, change the extension list below.
export const TEXT_FILE_EXTENSIONS = [
  '.txt',
  '.py',
  '.ipynb',
  '.js',
  '.jsx',
  '.html',
  '.css',
  '.java',
  '.cs',
  '.php',
  '.c',
  '.cpp',
  '.cxx',
  '.h',
  '.hpp',
  '.rs',
  '.R',
  '.Rmd',
  '.swift',
  '.go',
  '.rb',
  '.kt',
  '.kts',
  '.ts',
  '.tsx',
  '.m',
  '.scala',
  '.rs',
  '.dart',
  '.lua',
  '.pl',
  '.pm',
  '.t',
  '.sh',
  '.bash',
  '.zsh',
  '.csv',
  '.log',
  '.ini',
  '.config',
  '.json',
  '.proto',
  '.yaml',
  '.yml',
  '.toml',
  '.lua',
  '.sql',
  '.bat',
  '.md',
  '.coffee',
  '.tex',
  '.latex',
];

// Supported non-text file extensions which can be handled on Converse API.
// Ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_DocumentBlock.html
export const NON_TEXT_FILE_EXTENSIONS = [
  '.pdf',
  '.doc',
  '.docx',
  '.xls',
  '.xlsx',
];

export const SUPPORTED_FILE_EXTENSIONS = [
  ...TEXT_FILE_EXTENSIONS,
  ...NON_TEXT_FILE_EXTENSIONS,
];

// Converse API limitations:
// You can include up to five documents. Each document’s size must be no more than 4.5 MB.
// Ref: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock-runtime/converse.html
export const MAX_FILE_SIZE_MB = 4.5;
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
export const MAX_ATTACHED_FILES = 5;
