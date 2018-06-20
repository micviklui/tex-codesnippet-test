import yaml
import copy

import TexSoup
import TexSoup.utils

soup = TexSoup.TexSoup(r"""
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
    \variable{i} = \variable{i} + 1
\end{codesnip}

\begin{codesnip}
    \variable{x} = \variable{x}^2
\end{codesnip}

\begin{codesnip}
    % file: try_texsoup.py
    git diff \variable{file}
\end{codesnip}

\end{document}
""")


def find_codesnips(soup):
    return [c for c in soup.find_all('codesnip')]

def pop_comments(node):
    comments = []
    for e in node.contents:
        if (isinstance(e, TexSoup.utils.TokenWithPosition)
            and e.startswith('%')):
            comments.append(e.lstrip('%'))
            node.expr.remove_content(e)
    return comments
    #return yaml.load('\n'.join(comments))

def compile_codesnip(codesnip):
    #comments = [e.lstrip('%') for e in c0
    #            if (isinstance(e, TexSoup.utils.TokenWithPosition)
    #                and e.startswith('%'))]
    #variable_dict = yaml.load('\n'.join(comments))
    comments = pop_comments(codesnip)
    variable_dict = yaml.load('\n'.join(comments))

    output = []
    for t in codesnip.contents:
        if (isinstance(t, TexSoup.data.TexNode)
            and t.name == 'variable'):
            output.append(str(variable_dict.get(t.string)))
        else:
            output.append(str(t))
    return '\n'.join(output)

#compiled = [compile_codesnip(c) for c in find_codesnips(soup)]

cs = find_codesnips(soup)
cs0 = cs[0]
print([type(c) for c in cs0])
print([c for c in cs0])


for codesnip in find_codesnips(soup):
    comments = pop_comments(codesnip)
    v_dict = yaml.load('\n'.join(comments))
    if v_dict is None:
        continue
    for e in codesnip.children:
        if e.name == 'variable':
            try:
                e.replace(v_dict[e.string])
            except KeyError:
                pass
    print(codesnip)

