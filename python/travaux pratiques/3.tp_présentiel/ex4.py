import os
from pathlib import Path
from datetime import datetime
import re
from collections import Counter, defaultdict


# ============================================================================
# PARTIE 1 : AUDIT DE L'ARBORESCENCE
# ============================================================================

def scan_directory(base_path='archives'):
    print(f"[AUDIT] Scan du répertoire: {base_path}")
    
    base_path = Path(base_path)
    files_info = []
    
    if not base_path.exists():
        print(f"ERREUR: Le dossier {base_path} n'existe pas!")
        return files_info
    
    for root, files in os.walk(base_path):
        for filename in files:
            filepath = Path(root) / filename
            try:
                stats = filepath.stat()
                file_info = {
                    'chemin_absolu': str(filepath.absolute()),
                    'taille_ko': round(stats.st_size / 1024, 2),
                    'date_modif': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
                files_info.append(file_info)
            except Exception as e:
                print(f"Erreur lecture {filepath}: {e}")
    
    print(f"[AUDIT] {len(files_info)} fichiers recensés")
    return files_info


def generate_audit_report(files_info, output_file='audit_arborescence.txt'):
    """Génère le rapport d'audit"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT D'AUDIT - ARBORESCENCE DES ARCHIVES\n")
        f.write(f"Date du rapport: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Nombre total de fichiers: {len(files_info)}\n")
        total_size = sum(info['taille_ko'] for info in files_info)
        f.write(f"Taille totale: {total_size:.2f} Ko ({total_size/1024:.2f} Mo)\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("DÉTAILS DES FICHIERS\n")
        f.write("-" * 80 + "\n\n")
        
        for idx, info in enumerate(files_info, 1):
            f.write(f"[{idx}] Fichier: {info['chemin_absolu']}\n")
            f.write(f"    Taille: {info['taille_ko']} Ko\n")
            f.write(f"    Dernière modification: {info['date_modif']}\n\n")
    
    print(f"[AUDIT] Rapport généré: {output_file}")


# ============================================================================
# PARTIE 2 : NETTOYAGE DES FICHIERS TEXTE
# ============================================================================

def clean_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur lecture {filepath}: {e}")
        return None
    
    # Supprimer caractères non-ASCII
    content = re.sub(r'[^\x00-\x7F]+', ' ', content)
    
    # Traiter ligne par ligne
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Supprimer espaces en trop
        line = ' '.join(line.split())
        # Ignorer lignes vides
        if line.strip():
            # Convertir en minuscules
            cleaned_lines.append(line.lower())
    
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Calculer statistiques
    num_lines = len(cleaned_lines)
    num_words = sum(len(line.split()) for line in cleaned_lines)
    max_line_length = max((len(line) for line in cleaned_lines), default=0)
    
    return {
        'content': cleaned_content,
        'num_lines': num_lines,
        'num_words': num_words,
        'max_line_length': max_line_length
    }


def process_all_text_files(base_path='archives', output_dir='cleaned'):
    base_path = Path(base_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"[NETTOYAGE] Recherche des fichiers texte dans {base_path}")
    
    txt_files = list(base_path.rglob('*.txt'))
    print(f"[NETTOYAGE] {len(txt_files)} fichiers texte trouvés")
    
    stats = []
    
    for txt_file in txt_files:
        print(f"  • Traitement: {txt_file.name}")
        result = clean_text_file(txt_file)
        
        if result:
            # Sauvegarder version nettoyée
            output_filename = f"cleaned_{txt_file.name}"
            output_path = output_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            
            stats.append({
                'fichier_original': txt_file.name,
                'fichier_nettoye': output_filename,
                'num_lines': result['num_lines'],
                'num_words': result['num_words'],
                'max_line_length': result['max_line_length']
            })
    
    print(f"[NETTOYAGE] Fichiers nettoyés sauvegardés dans {output_dir}/")
    return stats


def generate_cleaning_report(stats, output_file='rapport_textes.txt'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DE NETTOYAGE - FICHIERS TEXTE\n")
        f.write(f"Date du rapport: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Nombre de fichiers traités: {len(stats)}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("STATISTIQUES PAR FICHIER\n")
        f.write("-" * 80 + "\n\n")
        
        for stat in stats:
            f.write(f"Fichier: {stat['fichier_original']}\n")
            f.write(f"  → Nettoyé: {stat['fichier_nettoye']}\n")
            f.write(f"  → Nombre de lignes: {stat['num_lines']}\n")
            f.write(f"  → Nombre total de mots: {stat['num_words']}\n")
            f.write(f"  → Longueur maximale d'une ligne: {stat['max_line_length']} caractères\n\n")
    
    print(f"[NETTOYAGE] Rapport généré: {output_file}")


# ============================================================================
# PARTIE 3 : ANALYSE LEXICALE APPROFONDIE
# ============================================================================

def load_grimoire(filepath='archives/grimoire.txt'):
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"ERREUR: Le fichier {filepath} n'existe pas!")
        return None
    
    print(f"[ANALYSE] Chargement de {filepath}")
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    print(f"[ANALYSE] {len(lines)} lignes chargées")
    return lines


def analyze_lexical(lines):
    print("[ANALYSE] Analyse en cours...")
    
    all_words = []
    word_freq = Counter()
    word_line_presence = defaultdict(set)
    
    for line_idx, line in enumerate(lines):
        # Extraire les mots (lettres uniquement)
        words = re.findall(r'\b[a-zàâäéèêëïîôùûü]+\b', line.lower())
        
        for word in words:
            all_words.append(word)
            word_freq[word] += 1
            word_line_presence[word].add(line_idx)
    
    print(f"[ANALYSE] {len(all_words)} mots au total")
    print(f"[ANALYSE] {len(word_freq)} mots uniques")
    
    return {
        'lines': lines,
        'all_words': all_words,
        'word_freq': word_freq,
        'word_line_presence': word_line_presence
    }


def get_top_words(word_freq, n=50):
    return word_freq.most_common(n)


def get_prevalent_words(word_line_presence, word_freq, num_lines, threshold=0.7):
    min_lines = num_lines * threshold
    prevalent = []
    
    for word, line_set in word_line_presence.items():
        if len(line_set) >= min_lines:
            prevalent.append((word, len(line_set), word_freq[word]))
    
    prevalent.sort(key=lambda x: x[1], reverse=True)
    return prevalent


def get_unique_words(word_freq):
    return [word for word, count in word_freq.items() if count == 1]


def get_palindromes(word_freq):
    palindromes = []
    for word in word_freq.keys():
        if len(word) >= 3 and word == word[::-1]:
            palindromes.append((word, word_freq[word]))
    palindromes.sort(key=lambda x: x[1], reverse=True)
    return palindromes


def generate_lexical_report(analysis_data, output_file='analyse_grimoire.txt'):
    lines = analysis_data['lines']
    all_words = analysis_data['all_words']
    word_freq = analysis_data['word_freq']
    word_line_presence = analysis_data['word_line_presence']
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANALYSE LEXICALE APPROFONDIE - GRIMOIRE.TXT\n")
        f.write(f"Date du rapport: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Statistiques générales
        f.write("STATISTIQUES GÉNÉRALES\n")
        f.write("-" * 80 + "\n")
        f.write(f"Nombre de lignes: {len(lines)}\n")
        f.write(f"Nombre total de mots: {len(all_words)}\n")
        f.write(f"Nombre de mots uniques: {len(word_freq)}\n\n")
        
        # Top 50 mots
        f.write("=" * 80 + "\n")
        f.write("TOP 50 DES MOTS LES PLUS FRÉQUENTS\n")
        f.write("=" * 80 + "\n")
        top_words = get_top_words(word_freq, 50)
        for rank, (word, count) in enumerate(top_words, 1):
            f.write(f"{rank:2d}. {word:20s} → {count:5d} occurrences\n")
        f.write("\n")
        
        # Mots prévalents (70% des lignes)
        f.write("=" * 80 + "\n")
        f.write("MOTS PRÉSENTS DANS AU MOINS 70% DES LIGNES\n")
        f.write("=" * 80 + "\n")
        prevalent = get_prevalent_words(word_line_presence, word_freq, len(lines), 0.7)
        if prevalent:
            for word, num_lines, total_count in prevalent:
                pct = (num_lines / len(lines)) * 100
                f.write(f"{word:20s} → {num_lines:4d} lignes ({pct:.1f}%) | {total_count} occurrences\n")
        else:
            f.write("Aucun mot ne répond à ce critère.\n")
        f.write("\n")
        
        # Mots uniques (1 seule fois)
        f.write("=" * 80 + "\n")
        f.write("MOTS UNIQUES (apparaissent 1 seule fois)\n")
        f.write("=" * 80 + "\n")
        unique_words = get_unique_words(word_freq)
        f.write(f"Nombre total: {len(unique_words)}\n\n")
        if len(unique_words) <= 100:
            for word in sorted(unique_words):
                f.write(f"  • {word}\n")
        else:
            f.write("Premiers 100 mots uniques:\n")
            for word in sorted(unique_words)[:100]:
                f.write(f"  • {word}\n")
            f.write(f"\n... et {len(unique_words) - 100} autres\n")
        f.write("\n")
        
        # Palindromes
        f.write("=" * 80 + "\n")
        f.write("MOTS PALINDROMES (longueur ≥ 3)\n")
        f.write("=" * 80 + "\n")
        palindromes = get_palindromes(word_freq)
        if palindromes:
            f.write(f"Nombre total: {len(palindromes)}\n\n")
            for word, count in palindromes:
                f.write(f"{word:20s} → {count} occurrence(s)\n")
        else:
            f.write("Aucun palindrome détecté.\n")
    
    print(f"[ANALYSE] Rapport généré: {output_file}")


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    print("\n" + "=" * 80)
    print("SYSTÈME DE GESTION D'ARCHIVES NUMÉRIQUES")
    print("=" * 80 + "\n")
    
    # 1. AUDIT INITIAL
    print("\n[PHASE 1] AUDIT DE L'ARBORESCENCE")
    print("-" * 80)
    files_info = scan_directory('archives')
    generate_audit_report(files_info, 'audit_arborescence.txt')
    
    # 2. NETTOYAGE DES FICHIERS TEXTE
    print("\n[PHASE 2] NETTOYAGE DES FICHIERS TEXTE")
    print("-" * 80)
    cleaning_stats = process_all_text_files('archives', 'cleaned')
    generate_cleaning_report(cleaning_stats, 'rapport_textes.txt')
    
    # 3. ANALYSE LEXICALE DU GRIMOIRE
    print("\n[PHASE 3] ANALYSE LEXICALE DU GRIMOIRE")
    print("-" * 80)
    grimoire_lines = load_grimoire('archives/grimoire.txt')
    if grimoire_lines:
        analysis_data = analyze_lexical(grimoire_lines)
        generate_lexical_report(analysis_data, 'analyse_grimoire.txt')
    
    print("\n" + "=" * 80)
    print("TRAITEMENT TERMINÉ")
    print("=" * 80)
    print("\nRapports générés:")
    print("  • audit_arborescence.txt")
    print("  • rapport_textes.txt")
    print("  • analyse_grimoire.txt")
    print("\nFichiers nettoyés disponibles dans: cleaned/")
    print()


if __name__ == "__main__":
    main()