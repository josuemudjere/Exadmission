from typing import Any, Dict, List


SEUIL_ADMISSION = 75.0


def evaluer_admission(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Systeme expert simple d'admission a l'examen.
    Regle: l'etudiant est admis si sa participation atteint au moins 75%.
    """
    nom = (data.get("nom") or "Etudiant inconnu").strip()
    nom_cours = (data.get("nom_cours") or "").strip()
    unite = (data.get("unite") or "heures").strip().lower()
    total_cours = float(data.get("total_cours", 0) or 0)
    suivi = float(data.get("suivi", 0) or 0)

    if total_cours < 0:
        total_cours = 0
    if suivi < 0:
        suivi = 0

    suivi_effectif = min(suivi, total_cours) if total_cours > 0 else 0

    participation = 0.0
    if total_cours > 0:
        participation = (suivi_effectif / total_cours) * 100

    admis = participation >= SEUIL_ADMISSION
    statut = "Admis a l'examen" if admis else "Non admis a l'examen"

    manquant_unites = 0.0
    acompleter_unites = 0.0
    if total_cours > 0 and participation < SEUIL_ADMISSION:
        manquant_unites = max(0.0, total_cours - suivi_effectif)
        seuil_unites = (SEUIL_ADMISSION / 100) * total_cours
        acompleter_unites = max(0.0, seuil_unites - suivi_effectif)

    details: List[str] = []
    details.append(
        f"Participation calculee: {suivi_effectif:.2f}/{total_cours:.2f} {unite} ({participation:.2f}%)."
    )

    if admis:
        details.append(
            f"Le seuil minimal de {SEUIL_ADMISSION:.0f}% est atteint."
        )
    else:
        if total_cours == 0:
            details.append(
                "Le total du cours est nul, la participation ne peut pas etre evaluée."
            )
        else:
            details.append(
                f"L'Etudiant(e) {nom} s'est absenté pendant {manquant_unites:.2f} {unite}. il(elle) doit completer au moins {acompleter_unites:.2f} {unite} pour atteindre {SEUIL_ADMISSION:.0f}%."
            )

    return {
        "etudiant": nom,
        "nom_cours": nom_cours,
        "statut": statut,
        "admis": admis,
        "seuil": SEUIL_ADMISSION,
        "unite": unite,
        "total_cours": total_cours,
        "suivi": suivi_effectif,
        "participation": round(participation, 2),
        "manquant": round(manquant_unites, 2),
        "details": details,
    }
