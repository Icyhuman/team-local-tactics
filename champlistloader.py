from core import Champion


def _parse_champ(champ_text: str) -> Champion:
    name, rock, paper, scissors = champ_text.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))


def from_csv(filename: str) -> dict[str, Champion]:
    champions = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            champ = _parse_champ(line)
            champions[champ.name] = champ
    return champions

def from_csv2str(filename: str) -> dict[str, Champion]:
    champs = ""
    with open(filename, 'r') as f:
        for line in f.readlines():
            champs = champs+line
    return champs

def load_some_champs():
    return from_csv('some_champs.txt')

def load_champs_string():
    return from_csv2str('some_champs.txt')
