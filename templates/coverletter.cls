% Cover letter document class: global setup plus the layout macro layer.
% Every piece of spacing/typography lives here, so the emitter only ever emits
% semantic macro calls (\letterheader, \letterdate, \letterrecipient,
% \letterpara) and never layout.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{coverletter}[2026/10/14 v0.1 Cover letter class]

\LoadClass[11pt,letterpaper]{article}

\RequirePackage[margin=1in]{geometry}
\RequirePackage{fontspec}
\setmainfont{Helvetica Neue}
\RequirePackage{xcolor}
\RequirePackage{etoolbox}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{bookmark}

\definecolor{accent}{HTML}{0B5FA5}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

% Sender block: \letterheader{name}{contact line}
\newcommand{\letterheader}[2]{%
  {\Large\bfseries\color{accent} #1}\par
  {\small #2}\par
  \vspace{4pt}\hrule\vspace{10pt}%
}

% Date line: \letterdate{date}
\newcommand{\letterdate}[1]{%
  #1\par
}

% Recipient block: \letterrecipient{recipient}{company}{role}
% recipient and role may be empty.
\newcommand{\letterrecipient}[3]{%
  \ifstrempty{#1}{}{\textbf{#1}\par}%
  \ifstrempty{#2}{}{#2\par}%
  \ifstrempty{#3}{}{\textit{#3}\par}%
  \vspace{8pt}%
}

% Body paragraph: \letterpara{text}
\newcommand{\letterpara}[1]{%
  #1\par
}

% Closing block: \letterclosing{sign-off}{name}
% Signature spacing belongs here, not in the manuscript's paragraph flow.
\newcommand{\letterclosing}[2]{%
  \vspace{12pt}#1\par
  \vspace{14pt}#2\par
}
