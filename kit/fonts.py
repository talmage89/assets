"""Resolve installed font families/styles without distribution-specific paths."""
from functools import lru_cache
from pathlib import Path
import subprocess


@lru_cache(maxsize=None)
def find_font(family, style='Regular'):
    """Return a font filename, rejecting fontconfig's silent substitutions.

    Family and style must name installed faces (for example DejaVu Sans /
    Condensed Bold). No replacement font is accepted: it could change geometry
    and baked markings. fontconfig aliases in the returned metadata are allowed.
    """
    requested=f'{family}:style={style}'
    try:
        result=subprocess.run(
            ['fc-match', '-f', '%{file}\\n%{family}\\n%{style}\\n', requested],
            capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f'Cannot find font {family!r}, style {style!r}; '
                           'install fontconfig and the requested font.') from exc
    lines=result.stdout.splitlines()
    if (len(lines)!=3 or
        family.casefold() not in [v.strip().casefold() for v in lines[1].split(',')] or
        style.casefold() not in [v.strip().casefold() for v in lines[2].split(',')] or
        not Path(lines[0]).is_file()):
        raise RuntimeError(f'Missing font {family!r}, style {style!r}; '
                           'install this exact family and style (substitutes are rejected).')
    return lines[0]
