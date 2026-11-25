\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ICN}[2012/02/10 v0.1 ICN LaTeX English template class] % Need to be changed with new release
\LoadClass[a4paper, 10.5pt,twocolumn,twoside,journal]{article}
\RequirePackage{ifthen}
\usepackage{flushend}
\usepackage{graphicx}  %
%\usepackage{xeCJK}%
%\usepackage{carlito}%
\RequirePackage{picins}
\RequirePackage{ccaption}
\RequirePackage{calc}
%%--------PAGE FORMAT---------%%
\setlength{\topmargin}{28pt}
\setlength{\headsep}{13pt}
\setlength{\headheight}{6mm}
\setlength{\oddsidemargin}{-7mm}
\setlength{\evensidemargin}{-7mm}
\setlength{\voffset}{-0.40in}
\setlength{\hoffset}{0mm}
\setlength{\footskip}{3.5em}
\setlength{\columnsep}{8mm} %
\textwidth \paperwidth%
\textheight \paperheight%
\addtolength\textwidth{-38mm}
\addtolength\textheight{-62mm}
% extra vertical space between paragraphs normally
\setlength{\parskip}{0mm}
% extra vertical space between paragraphs within a list item
%\setlength{\parsep}{0mm}

%%
\setlength{\abovedisplayskip}{2pt plus 1pt minus 1pt}
\setlength{\belowdisplayskip}{3pt plus 2pt minus 2pt}

\setlength{\doublerulesep}{0.5pt}

%%
\renewcommand{\baselinestretch}{1.14}
\renewcommand{\arraystretch}{1.06}
%
%
\newlength\icn@linespace
\newcommand{\icn@choosefont}[3]{%
   \setlength{\icn@linespace}{#1*\real{\baselinestretch}}%
   \fontsize{#1}{\icn@linespace plus#2 minus #3}\selectfont}
%
% 1 in = 72 bp = 72.27 pt

\newcommand\size[1]{%
   \ifthenelse{\equal{#1}{0}}{%
       \icn@choosefont{42bp}{.5pt}{.3pt}}{}%
   \ifthenelse{\equal{#1}{0-}}{%
       \icn@choosefont{36bp}{.5pt}{.3pt}}{}%
   \ifthenelse{\equal{#1}{1}}{%
       \icn@choosefont{26bp}{.5pt}{.3pt}}{}%
   \ifthenelse{\equal{#1}{1-}}{%
       \icn@choosefont{24bp}{.5pt}{.3pt}}{}%
   \ifthenelse{\equal{#1}{2}}{%
       \icn@choosefont{22bp}{.5pt}{.3pt}}{}%
   \ifthenelse{\equal{#1}{2-}}{%
       \icn@choosefont{18bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{3}}{%
       \icn@choosefont{16bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{3-}}{%
       \icn@choosefont{15bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{4}}{%
       \icn@choosefont{14bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{4-}}{%
       \icn@choosefont{12bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{5}}{%
       \icn@choosefont{10.5bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{5--}}{%
       \icn@choosefont{10bp}{.3pt}{.2pt}}{}%
   \ifthenelse{\equal{#1}{5-}}{%
       \icn@choosefont{9bp}{.2pt}{.1pt}}{}%
   \ifthenelse{\equal{#1}{6}}{%
       \icn@choosefont{7.5bp}{.2pt}{.1pt}}{}%
   \ifthenelse{\equal{#1}{6-}}{%
       \icn@choosefont{6.5bp}{.2pt}{.1pt}}{}%
   \ifthenelse{\equal{#1}{7}}{%
       \icn@choosefont{5.5bp}{.1pt}{.1pt}}{}%
   \ifthenelse{\equal{#1}{8}}{%
       \icn@choosefont{5bp}{.1pt}{.1pt}}{}}
%
%%----- Redefine \tiny \scriptsize \footnotesize\small ----------%%
%%-------------------------\normalsize --------------------------%%
%%---------------\large \Large \LARGE \huge \Huge ---------------%%
%% Refer to ctex
\def\tiny{\size{7-}}
\def\scriptsize{\size{7}}
\def\footnotesize{\size{6-}}
\def\small{\size{6}}
\def\normalsize{\size{5-}}%
\def\large{\size{5}}%
\def\Large{\size{4}}%
\def\LARGE{\size{3}}%
\def\huge{\size{2-}}%
\def\Huge{\size{1-}}%
\def\IEEEproof{\@ifnextchar[{\@IEEEproof}{\@IEEEproof[\IEEEproofname]}}
\def\@IEEEproof[#1]{\par\noindent\hspace{1em}{\textbf #1{\quad}}}
\def\endIEEEproof{\hspace*{\fill}~$\blacksquare$\par}
\def\IEEEproofname{Proof}
\AtBeginDocument{\def\proof{\@IEEElegacywarn{proof}{IEEEproof}\IEEEproof}\def\endproof{\endIEEEproof}}




\normalsize  %make \baselinestretch take affect
%\renewcommand{\@biblabel}[1]{#1}
\let\@afterindentfalse\@afterindenttrue\@afterindenttrue
\def\@cite#1#2{\textsuperscript{[{#1\if@tempswa, #2\fi}]}}
\setlength{\footnotesep}{0pt}
\def\footnoterule{\kern-10\p@ \hrule width .4\columnwidth height 0.4pt \kern 6.6\p@}
%
%%-------- maketitle --------%%
%
%
\renewcommand{\title}[1]{\gdef\icn@title{{\huge\bf #1}}}
\renewcommand{\author}[1]{\gdef\icn@author{{\normalsize #1}}}
%\renewcommand{\address}[1]{\gdef\icn@address{{\footnotesize\it#1}}}
%\newcommand{\email}[1]{\gdef\icn@email{{\centering\footnotesize (E-mail: #1)}}}
\renewcommand{\abstract}[1]{\gdef\icn@abstract{{\noindent\small {\bf Abstract}\quad #1}}}
\newcommand{\keyword}[1]{\gdef\icn@keyword{{\noindent\small {\bf Key words}\quad #1}}}
\newcommand{\doi}[1]{\gdef\icn@doi{{\noindent\small {\bf DOI}\quad #1}}}
%
%
\renewcommand{\maketitle}{\par
 \begingroup
  \def\thefootnote{}%  the \thanks{} mark type is empty
  \def\footnotemark{}% and kill space from \thanks within author
   \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
   \long\def\@makefntext##1{\parindent 1em\noindent
           \hb@xt@0.5em{%
               \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
   \twocolumn[\@maketitle]%
   \thispagestyle{icn@firstheadings}%ssl
   \@thanks%
 \endgroup%
 \setcounter{footnote}{0}%
 \global\let\thanks\relax%
 \global\let\maketitle\relax%
 \global\let\@maketitle\relax%
 \global\let\@thanks\@empty%
 \global\let\@author\@empty%
 \global\let\@title\@empty%
 \global\let\title\relax%
 \global\let\author\relax%
 \global\let\and\relax%
%
 \global\let\cncl\relax%
 \global\let\email\relax%
%
 \global\let\icn@title\relax%
 \global\let\icn@author\relax%
 \global\let\icn@address\relax%
 \global\let\icn@abstract\relax%
 \global\let\icn@keyword\relax%
 \global\let\icn@doi\relax%
%
 \global\let\title\relax%
 \global\let\author\relax%
 \global\let\address\relax%
 \global\let\abstract\relax%
 \global\let\keyword\relax%
 \global\let\doi\relax%
}
%
\def\@maketitle{%
    \let\footnote\thanks%
    \newpage\null% an empty hbox
    \vskip 1.2\baselineskip%
    {\centering%
    {\icn@title\par}%
    {%\vskip 1.2em%
    \vskip 0.8\baselineskip%
    \begin{tabular}[t]{c}%
    \icn@author%
    \end{tabular}%
    \vskip 0.3em%
    \par%
    }%
    \vskip 0.2\baselineskip}%
    {\linespread{1.0}\selectfont\icn@abstract\par%
    \vskip 0.2\baselineskip%
    \icn@keyword\par%
    \vskip 0.2\baselineskip%
    \icn@doi\par
    }%
    \vskip 1.5\baselineskip%
}
%
\renewcommand{\refname}{\centering \normalsize\bf References}
%
\newenvironment{acknowledgement}{
    \vspace*{10pt}
    {\noindent\size{4}\bfseries Acknowledgements\par}
    \vspace*{10pt}
    \begingroup
    }{
    \par
    \endgroup
}
%
%%---------------- Define biography ----------------%%
\newenvironment{biography}[1][]{
\vskip 0.4\baselineskip%
\size{5-}
\parpic{%
\includegraphics[height=3.0cm,width=2.4cm]{#1}}%
}{\vskip 0.4\baselineskip\par}

%% For author who has no photo
\newenvironment{biographynophoto}{\vskip 0.4\baselineskip\size{5-}}{\vskip 0.4\baselineskip\par}

%%---------------- Redefine section -----------------%%
\setcounter{secnumdepth}{3}

\renewcommand\thesection {\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}

\renewcommand\section{\@startsection {section}{1}{\z@}%
                                   {-1.5ex \@plus -.2ex \@minus -.2ex}%
                                   {1.5ex \@plus.2ex}%
                                   {\size{4-}\bfseries}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-1.0ex \@plus -.2ex \@minus -.2ex}%
                                     {1.0ex \@plus .2ex}%
                                     {\size{5}\bfseries}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-0.5ex \@plus -.0ex \@minus -.2ex}%
                                     {0.5ex \@plus .0ex}%
                                     {\size{5}\bfseries}}
\renewcommand*\l@section[2]{%
  \ifnum \c@tocdepth >\z@
    \addpenalty\@secpenalty
    \addvspace{1.0em \@plus\p@}%
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
    \endgroup
  \fi}
%



\newcommand{\firstheadname}[1]{\gdef\icn@firstheadname{\size{5-} #1}}
\newcommand{\firstfootname}[1]{\gdef\icn@firstfootname{#1}}
\newcommand{\headevenname}[1]{\gdef\icn@headevenname{{\size{5-} #1}}}
\newcommand{\headoddname}[1]{\gdef\icn@headoddname{{\size{5-} #1}}}


%%------------------icn@firstheadings begin------------------------------------%%
\def\ps@icn@firstheadings{
   \let\@evenhead\@empty\let\@evenfoot\@empty
   \let\@oddhead\@empty\let\@oddfoot\@empty
    \def\@evenhead{%
        \vbox{%
            \vskip 3.2mm%
            \hbox to \textwidth{{\size{5-} \hbox{\icn@firstheadname} \hfill }}%
            \vskip 2.0mm%
%            \hrule width\textwidth height0.63pt\vskip0.85pt \hrule width\textwidth height0.63pt\vskip0.85pt \hrule width\textwidth height0.63pt%
        }%
    }
   \def\@evenfoot{
   \hbox{\icn@firstfootname}
    }
   \let\@oddhead\@evenhead%
   \let\@oddfoot\@evenfoot%
}
%%-----------------icn@firstheadings end--------------------------------------%%
%%-------------------icnheadings begin----------------------------------------%%
\def\ps@icnheadings{
    \let\@evenhead\@empty\let\@evenfoot\@empty
    \let\@oddhead\@empty\let\@oddfoot\@empty
    \def\@evenhead{%
        \vbox{%
            \vskip 3.2mm%
            \hbox to \textwidth {\mbox{\hspace {2mm}} {\size{5-} \thepage} \hfill \hbox{\icn@headevenname}  {\size{5-} \mbox{\hspace {2mm}}}}%
%            \vskip 2.0mm%
 %           \hbox to \textwidth{\noindent\rule[2mm]{\textwidth}{0.5pt}}%
        }%
    }
    \def\@oddhead{%
        \vbox{%
            \vskip 3.2mm%
            \hbox to \textwidth {{\size{5-} \mbox{\hspace {0mm}} \icn@headoddname}   \hfill {{\size{5-} \thepage} \mbox{\hspace {2mm}}}}%
   %         \vskip 2.0mm%
    %        \hbox to \textwidth{\noindent\rule[2mm]{\textwidth}{0.5pt}}%
        }
    }%
}
%---------------------headings end------------------------------------------%%
%
%%-------- Set the begin and end method for class -----%%
\AtBeginDocument{%
   \flushend
   \captiondelim{ } %
   \captionnamefont{\small}%
   \captiontitlefont{\small}%
   }
\AtEndDocument{\clearpage}
\endinput
%%-------- The end of icn.cls -------------%%
