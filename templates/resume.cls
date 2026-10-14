% Resume document class: global setup plus the layout macro layer.
% Every piece of spacing/typography lives here, so the emitter only ever emits
% semantic macro calls (\cvsection, \cventry, \cvbullet) and never layout.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2026/10/13 v0.1 Resume class]

\LoadClass[10pt,letterpaper]{article}

\RequirePackage[margin=0.75in]{geometry}
\RequirePackage{fontspec}
\setmainfont{Helvetica Neue}
\RequirePackage{xcolor}
\RequirePackage{tabularx}
\RequirePackage{etoolbox}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{bookmark}

\definecolor{accent}{HTML}{0B5FA5}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\renewcommand{\arraystretch}{1.15}

% Header: \cvheader{name}{contact line}
\newcommand{\cvheader}[2]{%
  \begin{center}%
    {\LARGE\bfseries #1}\\[4pt]%
    #2%
  \end{center}%
}

% Summary: \cvsummary{text}
\newcommand{\cvsummary}[1]{%
  \par#1\par
}

% Section heading: \cvsection{Title}
\newcommand{\cvsection}[1]{%
  \par\vspace{8pt}%
  {\large\bfseries\color{accent}\MakeUppercase{#1}}\par
  \vspace{2pt}\hrule\vspace{4pt}%
}

% Entry: \cventry{title}{subtitle}{dates}{location}
% subtitle and location may be empty.
\newcommand{\cventry}[4]{%
  \par\noindent
  \begin{tabularx}{\linewidth}{@{}Xr@{}}
    \textbf{#1}\ifstrempty{#2}{}{ --- \textit{#2}} & \textit{#3} \\
  \end{tabularx}%
  \ifstrempty{#4}{}{\par\noindent\textit{#4}}%
  \par
}

% Bullet list and bullet: \begin{cvbullets} \cvbullet{text} ...
\newenvironment{cvbullets}{\begin{itemize}}{\end{itemize}}
\newcommand{\cvbullet}[1]{\item #1}

% Skill line (inside cvbullets): \cvskill{label}{items}
\newcommand{\cvskill}[2]{\item \textbf{#1}: #2}
