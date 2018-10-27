\LoadClassWithOptions{article}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{arxiv}[NVSL ArXiv submission class]
\RequirePackage{times}


% Borrowed from acmart.cls.  Put abstract before \maketitle
\renewenvironment{abstract}{\collect@body\@saveabstract}{}
\long\def\@saveabstract#1{\long\gdef\@abstract{#1}}

\def\@mkabstract{\bgroup
  \ifx\@abstract\@lempty\else
  {%\phantomsection\addcontentsline{toc}{section}{Abstract}%
   \section*{Abstract}%
   \ignorespaces\@abstract\par}%
  \fi\egroup
  % Once we have rendered the absract once, restore the old abstract environment.  This allows the abstract to come after \maketitle
  \renewenvironment{abstract}{\section*{Abstract}}{}
}

% override \maketitle to render the abstract automatically.
\let\oldmaketitle\maketitle
\renewcommand{\maketitle}{\oldmaketitle\@mkabstract}

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
