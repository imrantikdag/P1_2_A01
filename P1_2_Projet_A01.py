import qcm
from random import shuffle

def generate_correct_answers(questions):
    """
    Génére la liste des bonnes réponses du questionnaire et calcule le score maximal

    `pre` - un questionnaire "questions" construit avec build_questionnaire()

    `post` - retourne une liste des indexes des bonnes réponses de chaque question dans l'ordre et le score maximal qu'il est possible d'obtenir
    """
    max_score = 0
    correct_answers = []
    for question in questions:
        a = question[1]
        correct_answers.append(set())
        for i in range(len(a)):
            if a[i][1]:
                correct_answers[-1].add(i)
                max_score += 1
    return correct_answers, max_score

def parse_answer_string(answer_string, max_answer):
    """
    Convertit les réponses de l'utilisateur (sous forme de lettres) en un set d'entiers correspondant aux indexes des réponses
    
    (Exemple: transforme `"ABD"` en `{0, 1, 3}`)

    ---
    `pre`:
    
    - un string "answer_string" qui contient des lettres
    - un entier "max_answer" qui détérmine l'indexe de réponse maximale qu'on peut accepter
    ---
    
    `post` - retourne un set avec les lettres données converties en nombres
    """
    answer_set = set()
    for char in answer_string:
        i = ord(char.upper()) - 65
        if i >= 0 and i < max_answer:
            answer_set.add(i)
    return answer_set

def generate_box(text):
    """
    Dessine une boite autour d'un string donné avec des caractères unicode

    `pre` - un string "text"

    `post` - retourne le string avec une boite autour
    """
    box  = "╭" + "─" * (len(text)+2) + "╮\n"
    box += "│ " + text + " │\n"
    box += "╰" + "─" * (len(text)+2) + "╯"
    return box

def input_with_retry(question, valid, retry="Réessayez. "):
    """
    Demande une entrée de l'utilisateur avec input() et redemande jusqu'à obtenir une réponse qui est valide

    ---
    `pre`:
    
    - un string "question": la question à poser à l'utilisateur
    - une liste "valid": une fonction lambda qui retourne True si la réponse (son argument) est valide
    - un string "retry" (optionnel): le texte à montrer à l'utilisateur lorsqu'il réessaye
    ---

    `post` - retourne la réponse valide donnée par l'utilisateur
    """
    answer = input(question)
    while not valid(answer):
        answer = input(retry)
    return answer

print(generate_box("Programme de QCM"))

try:
    filename = input("Lire quel fichier ? ")
    q = qcm.build_questionnaire(filename)
    user_answers = []

    # Un premier passage dans le questionnaire
    line_length = 0
    for i in range(len(q)):
        # On détérmine la longueur des lignes à dessiner, en fonction de la longueur maximale des questions
        if (len(q[i][0]) + 8) > line_length:
            line_length = len(q[i][0]) + 8
            
        # On mélange la liste de réponses avec la fonction `shuffle` dans `random`
        shuffle(q[i][1])

    correct_answers, max_score = generate_correct_answers(q)
except:
    print("Une erreur est survenue lors de la lecture du fichier.")
    print("Vérifiez que le fichier existe et qu'il est correctement formatté.")
else:
    # Il y a des erreurs qu'on ne peut pas attraper avec le try-except sans modifier qcm.py
    # Ces erreurs peuvent arriver si une ligne du fichier est mal formée
    # qcm.py affiche ces erreurs dans la console (au lieu de `raise` une exception),
    # mais finit quand même par charger le questionnaire, avec des questions ou des réponses qui manquent
    print("Lecture du fichier terminée.")
    print("")

    comparatif = input_with_retry("Afficher le score final avec (1) ou sans (2) le mode comparatif ? ", lambda x: x in ("1", "2"))
    comparatif = not bool(int(comparatif)-1) # Cette ligne convertit 1 en True et 2 en False

    if not comparatif:
        malus = input_with_retry("Calculer le score final avec (1) ou sans (2) malus ? ", lambda x: x in ("1", "2"))
        malus = not bool(int(malus)-1) # idem

    print("")
    print(f"{filename} contient {str(len(q))} questions.")
    print("Pour chaque question, tapez les lettres qui correspondent aux réponses qui vous semblent correctes, puis appuyez sur la touche ENTER.")

    # On pose les questions à l'utilisateur
    for i, question in enumerate(q):
        a = question[1]
        print("─" * line_length)

        # Affiche la question
        print(generate_box(f"{str(i+1)} | {question[0]}"))

        # Convertit les indexes des propositions en lettres majuscules
        valid_letters = [chr(65 + i) for i in range(len(a))]

        # Affiche les propositions
        for j, answer in enumerate(a):
            print(f"  {valid_letters[j]} | {answer[0]}")
        
        print("")

        # `len(correct_answers[i]) > 1` indique que c'est une QRM
        if (len(correct_answers[i]) > 1):
            print("Plusieurs réponses sont correctes.")

        # On demande la réponse de l'utilisateur
        answer_string = input_with_retry(
            "Votre réponse: ",
            # Cette fonction lambda vérifie que:
            # (1) Tous les caractères de la réponse sont inclus dans valid_letters
            # ET (2) il y a 1 seul caractère dans la réponse, OU c'est une QRM
            lambda x: all(letter.upper() in valid_letters for letter in x) and (len(x) == 1 or len(correct_answers[i]) > 1),
            "Réponse invalide.\nRéessayez : "
        )
        answer_set = parse_answer_string(answer_string, len(a))
        user_answers.append(answer_set)

    print("─" * line_length)

    score = 0
    score_malus = 0
    for i in range(len(user_answers)):  # Pour chaque set de réponses donné,
        for a in user_answers[i]:       # Pour chaque réponse dans le set,
            if a in correct_answers[i]: # Si la réponse est dans le set de bonnes réponses,
                score += 1              # on augmente
                score_malus += 1        # les 2 scores
            else:
                score_malus -= 1        # On pénalise uniquement le score malus pour les mauvaises réponses

    # Éviter une cote négative
    score_malus = max(0, score_malus)

    if comparatif or not malus: print(generate_box(f"Votre score est {str(score)}/{str(max_score)} (sans malus)"))
    if comparatif or malus: print(generate_box(f"Votre score est {str(score_malus)}/{str(max_score)} (avec malus)")) # FIRST COMMENT

    #first comment