from repositories.citation_repository import get_all_citations

def citation_to_bibtex(citation):
    fields = {
        "author": citation.author,
        "title": citation.title,
        "year": citation.year,
        "journal": citation.journal,
        "volume": citation.volume,
        "pages": citation.pages,
        "publisher": citation.publisher,
        "booktitle": citation.booktitle,
        "doi": citation.doi,
    }

    lines = [f"@{citation.type}" + "{" + f"{citation.keyword},"]
    for key, value in fields.items():
        if value is not None:
            lines.append(f"  {key} = {{{value}}},")

    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)

def all_citations_to_bibtex():
    citations = get_all_citations()
    bibtex_entries = [citation_to_bibtex(citation) for citation in citations]
    return "\n\n".join(bibtex_entries)
