from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import dataclasses, json
from pathlib import Path


class Statut(str, Enum):
    EN_ATTENTE = "en_attente"
    TRAITE = "traite"


@dataclass(frozen=True, slots=True)
class Document:
    id: str
    texte: str
    statut: Statut = Statut.EN_ATTENTE
    metadonnees: dict[str, str] = field(default_factory=dict)

    @property
    def taille(self) -> int:
        return len(self.texte)


class ErreurIngestion(Exception):
    pass


class DocumentIllisible(ErreurIngestion):
    def __init__(self, chemin: str, motif: str):
        super().__init__(f"document {chemin} : Illisible car {motif}")
        self.chemin = chemin
        self.motif = motif


def charger(chemin) -> Document:
    try:
        texte = Path(chemin).read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise DocumentIllisible(chemin, "octets non décodables en UTF-8") from e
    return Document(Path(chemin).name, texte)


# --- 2. égalité ---
a = Document("x", "meme texte")
b = Document("x", "meme texte")
print("a == b :", a == b)

# --- 3. isolation des métadonnées ---
a.metadonnees["source"] = "web"
print("a :", a.metadonnees)
print("b :", b.metadonnees)

# --- 4. json ---
print(json.dumps({"id": a.id, "statut": a.statut}))

# --- 5. frozen ---
try:
    a.statut = Statut.TRAITE
except dataclasses.FrozenInstanceError as e:
    print("refus :", e)
c = dataclasses.replace(a, statut=Statut.TRAITE)
print("copie :", c.statut, "| original :", a.statut)

# --- 6. boucle sur le corpus ---
documents, rejetes = [], []
for chemin in sorted(p for p in Path("corpus_test").rglob("*") if p.is_file()):
    try:
        documents.append(charger(chemin))
    except ErreurIngestion as e:
        rejetes.append(e.chemin)
print(f"{len(documents)} documents, {len(rejetes)} rejetés : {rejetes}")
