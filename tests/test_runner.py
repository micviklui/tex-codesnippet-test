import codesnip_run.runner

import TexSoup
import TexSoup.utils


entire_tex_soup = TexSoup.TexSoup(r"""
\begin{document}

\section{Hello \textit{world}.}

\subsection{Watermelon}

(n.) A sacred fruit. Also known as:

\begin{itemize}
\item red lemon
\item life
\end{itemize}

Here is the prevalence of each synonym.

\begin{tabular}{c c}
red lemon & uncommon \\
life & common
\end{tabular}

\begin{codesnip}
    % i: 3
    python -c 'print(\variable{i} * \variable{i} + 1)'
\end{codesnip}

\begin{codesnip}
    echo \variable{y} = \variable{x}^2
\end{codesnip}

\begin{codesnip}
    % file: try_texsoup.py
    git diff \variable{file}
\end{codesnip}

\begin{codesnip}
    mpl_qt
\end{codesnip}

\end{document}
""")

def test_find_codesnips():
    codesnips = codesnip_run.runner.find_codesnips(entire_tex_soup)
    assert str(codesnips[0]) == (
        "\\begin{codesnip}\n"
        "    % i: 3\n"
        "    python -c 'print(\\variable{i} * \\variable{i} + 1)'\n"
        "\\end{codesnip}"
    )

    assert str(codesnips[1]) == (
        "\\begin{codesnip}\n"
        "    echo \\variable{y} = \\variable{x}^2\n"
        "\\end{codesnip}"
    )


codesnip_soup = TexSoup.TexSoup(r"""
\begin{codesnip}
    mpl_qt
\end{codesnip}
""")

#def test_get_command():
#    command = codesnip_run.runner.get_command(codesnip_soup)

def test_run_command():
    command = 'mpl_qt'
    codesnip_run.runner.run_command(command)
