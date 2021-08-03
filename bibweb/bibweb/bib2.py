#!/usr/bin/env python3

import biblib.bib
import argparse
import sys
import json
import biblib.algo
import logging as log
import os
from jinja2 import Template
import re

short_bibentry = Template("""
<div class='bib_entry'>
{% if e.paper_pdf %}
<a href={{e.paper_pdf}}>
{% elif e.url %}
<a href={{e.url}}>
{% endif %}
<span class='bib_title'>{{e.title}}</span> 
<span class='bib_author'>{{e.author}}</span>
<span class='bib_meta_block'>
{% if e.type == 'inproceedings' %}
<span class='bib_meta'>{{e.venue}}</span>
{% elif e.type == 'article' %}
<span class='bib_meta'>{{e.venue}}</span>
{% elif e.type == 'techreport' %}
<span class='bib_meta'>{{e.institution}} {{e.number}}</span>
{% elif e.type == 'phdthesis' %}
<span class='bib_meta'>{%if e.school %}{{e.school}}{% endif %} Ph.D. Thesis</span>
{% elif e.type == 'mastersthesis' %}
<span class='bib_meta'>{{e.school}} Masters Thesis</span>
{% endif %}
<span class='bib_meta'>{{e.year}}</span>
</span>
{% if e.paper_pdf %}
</a>
{% elif e.url %}
</a>
{% endif %}
</div>
""");

full_bibentry = Template("""
<div class='bib_entry {{e.type}}'>
{% if e.paper_pdf %}
<a href={{e.paper_pdf}}>
{% elif e.url %}
<a href={{e.url}}>
{% endif %}
<span class='bib_title'>{{e.title}}</span> 
<span class='bib_author'>{{e.author}}</span>
<span class='bib_meta_block'>

{% if e.type == 'inproceedings' %}
<span class='bib_meta'>In {{e.booktitle}}. {{e.publisher}}{% if e.location %}, {{e.location}}{% endif %}{% if e.pages %}, {{e.pages}}{% endif %}.</span>
{% elif e.type == 'article' %}
<span class='bib_meta'>{{e.journal}} {{e.volume}}, {{e.number}} ({% if e.month %}{{e.month}} {%endif%}{{e.year}}){%if e.pages %}, {{e.pages}}{% endif %}. </span>
{% elif e.type == 'techreport' %}
<span class='bib_meta'>{{e.institution}}. Technical Report {{e.number}}</span>
{% elif e.type == 'phdthesis' %}
<span class='bib_meta'>Ph.D. Dissertation. {% if e.school %}{{e.school}}{% endif %}. Advised by {{e.advisor}}.</span>
{% elif e.typee == 'mastersthesis' %}
<span class='bib_meta'>Masters Thesis. {{e.school}}. Advisor(s) {{e.advisor}}.</span>
{% endif %}
{% if e.doi %}<span class='bib_doi'> (DOI={{e.doi}})</span>{% endif %}
</span>
{% if e.paper_pdf %}
</a>
{% elif e.url %}
</a>
{% endif %}
</div>
""");

def fix_authors(s):
    authors = s.split(" and ")
    n = []
    for a in authors:
        if "," in a:

            (last, first) = a.split(", ")
            a = f"{first} {last}"
        n.append(a)
    return ", ".join(n)
    
def fix_paper_pdf(s):
    if "http" in s:
        return s

    if os.path.exists(f"pdfs/{s}"):
        return f"/data/bib/pdfs/{s}"
    else:
        log.error(f"pdf pdfs/{s} is missing")
    return None

def find_short_name(s, short_names):
    for p,v in short_names:
        if re.search(p, s, flags=re.IGNORECASE):
            return v
        if re.search(v, s, flags=re.IGNORECASE):
            return v
    return s

def short_venue(e):
    if e['type'] == "inproceedings":
        return find_short_name(e['booktitle'],
                               [("file.*stor.*", "FAST"),
                                ("USENIX", "USENIX ATC"),
                                ("inter.*sympo.*comp.*arch", "ISCA"),
                                ("sympo.*comp.*scienc.*edu", "SIGCSE"),
                                ("ympo.*icroar", "MICRO"),
                                ("Networked.*Syst", "NSDI"),
                                ("Hot.*Storage", "HotStorage"),
                                ("Arch.*supp.*prog", "ASPLOS"),
                                ("Web Eng.*", "ICWE"),
                                ("Sym.*op.*prin", "SOSP"),
                                ("Oper.*syst.*desig.*Impl", "OSDI"),
                                ("Asia-Pacific", "APSys"),
                                ])
    elif e['type'] == "article":
        return find_short_name(e['journal'],
                               [("IEEE.*micro", "IEEE Micro"),
                                ("comm.*acm", "CACM"),
                                ("CoRR", "arXiv")
                                ])
    elif e['type'] == "techreport":
        return f"e['institution'] Tech Report"
    return ""

def load_bibs(bib, min_crossrefs):
    try:
        # Load databases
        db = biblib.bib.Parser().parse(bib, log_fp=sys.stderr).get_entries()

        # Optionally resolve cross-references
        if min_crossrefs is not None:
            db = biblib.bib.resolve_crossrefs(
                db, min_crossrefs=min_crossrefs)
        return db
    except biblib.messages.InputError:
        raise click.ClickException(f"Couldn't load bib files: {bib}")

@click.command(help='generate html of bib entries')
@click.option('--out','-o', default="-", type=click.File('w'), help='OUtput file')
@click.argument('bib', nargs="-1", required=True, type=click.File('r'), help='.bib file(s) to process')
def bib2html(bib=None, out =None):
    db = load_bibs(bib, None)

    entries = []
    for ent in db.values():
        try:
            key = ent.key
            type = ent.typ
            e = {x:biblib.algo.tex_to_unicode(ent.get(x, ""),pos=ent.field_pos[x]) for x in ent}
            e.update(dict(key=key,type=type))
            e['author'] = fix_authors(e['author'])
            entries.append((int(e['year']),full_bibentry.render(e=e)))
        except Exception as e:
            click.secho(f"Problem processing item with key '{ent}'", fg="red")
            raise

    entries.sort()
    for year, html in entries:
        out.write(html)
        
@click.command(help='Flatten macros, combine, and pretty-print .bib database(s)')
@click.argument('bib', nargs="-1", required=True, type=click.File('r'), help='.bib file(s) to process')
@click.option('--out','-o', default="-", type=click.File('w'), help='OUtput file')
@click.option("--min-crossrefs", type=int, default=None, help='minimum number of cross-referencing entries'
                            ' required to expand a crossref; if omitted, no'
                            ' expansion occurs')
def bib2json(bib=None, min_crossrefs=None, out=None):

    db = load_bibs(bib, min_crossrefs)
    # Pretty-print entries
    entries = dict()

    for ent in db.values():
        try:
            key = ent.key
            type = ent.typ
            e = {x:biblib.algo.tex_to_unicode(ent.get(x, ""),pos=ent.field_pos[x]) for x in ent}
            e.update(dict(key=key,type=type))
            e['author'] = fix_authors(e['author'])
            if 'paper_pdf' in e:
                e['paper_pdf'] = fix_paper_pdf(e['paper_pdf'])
                if not e['paper_pdf']: 
                    del e['paper_pdf']
            e['venue'] = short_venue(e)

            entries[key] = dict(short=short_bibentry.render(e=e),
                                full=full_bibentry.render(e=e),
                                raw=e)
        except Exception as e:
            click.secho(f"Problem processing item with key '{ent}'", fg="red")
            raise

    out.write(json.dumps(entries, sort_keys=True, indent=4, separators=(',', ': ')))

#    for t in entries:
#        sys.stderr.write(f"[jsoncontentimporterpro id=5 parser=twig param1='{t}']\n")
#for t in entries:
#        sys.stderr.write(f"[jsoncontentimporterpro id=6 parser=twig param1='{t}']\n")

if __name__ == '__main__':
    main()
