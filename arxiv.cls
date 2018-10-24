\LoadClassWithOptions{article}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{arxiv}[NVSL ArXiv submission class]
\RequirePackage{times}

\RequirePackage{geometry} 
 \geometry{
 total={6.5in,9in},
 left=1in,
 top=1in,
 }

\RequirePackage{fancyhdr}
\pagestyle{fancy}

\fancyhead{} % clear all header fields
\renewcommand{\headrulewidth}{0pt} % no line in header area
\fancyfoot{} % clear all footer fields

\fancyfoot[LE,RO]{\thepage}           % page number in ``outer'' position of footer line
\fancyfoot[RE,LO]{\scriptsize Copyright \textcopyright~\the\year\ the authors.\\{\tiny \gitcommit}} % other info in ``inner'' position of footer line
