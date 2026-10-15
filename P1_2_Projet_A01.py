import qcm
from random import shuffle

def generate_correct_answers(questions):
    """
    Génére la liste des bonnes réponses du questionnaire et calcule le score maximal

    `pre` - un questionnaire "questions"

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
    box += "╰" + "─" * (len(text)+2) + "╯\n"
    return box

def input_with_retry(question, valid, retry="Réessayez. "):
    """
    Demande une entrée de l'utilisateur et redemande si la réponse donnée n'est pas valide

    ---
    `pre`:
    
    - un string "question": la question à poser à l'utilisateur
    - une liste "valid": une fonction lambda qui retourne True si la réponse est valide
    - un string "retry" (optionnel): le texte à montrer à l'utilisateur lorsqu'il réessaye
    ---

    `post` - retourne la réponse valide donnée par l'utilisateur
    """
    answer = input(question)
    while not valid(answer):
        answer = input(retry)
    return answer

print(generate_box("PROGRAMME DE QCM (sans nom)")) # mettez un nom?

try:
    filename = input("Lire quel fichier ? ")
    q = qcm.build_questionnaire(filename)
    user_answers = []
except:
    print("Une erreur est survenue lors de la lecture du fichier.")
    print("Vérifiez que le fichier existe et que vous n'avez fait aucune faute de frappe.")
else:
    print("Lecture terminée sans erreurs.")
    print("")

    malus = input_with_retry("Calculer le score final avec (1) ou sans (2) malus ? ", lambda x: x in ("1", "2"))
    malus = not bool(int(malus)-1)

    comparatif = input_with_retry("Afficher le score final avec (1) ou sans (2) le mode comparatif ? ", lambda x: x in ("1", "2"))
    comparatif = not bool(int(comparatif)-1)

    print("")
    print(filename, "contient", str(len(q)), "questions.")
    print("Pour chaque question, tapez les lettres qui correspondent aux réponses qui vous semblent correctes, puis appuyez sur la touche ENTER.")

    # un premier passage dans le questionnaire
    line_length = 0
    for i in range(len(q)):
        # on détérmine la longueur des lignes à dessiner, en fonction de la longueur maximale des questions
        if (len(q[i][0]) + 4) > line_length:
            line_length = len(q[i][0]) + 4
            
        # !!! on met les réponses dans un ordre aléatoire avec la fonction shuffle dans random
        shuffle(q[i][1])

    correct_answers, max_score = generate_correct_answers(q)

    # on pose les questions à l'utilisateur
    for i, question in enumerate(q):
        a = question[1]
        print("─" * line_length)

        # affiche la question
        print(str(i+1), "|", question[0])

        # affiche les propositions
        for j, answer in enumerate(a):
            print("  " + chr(65 +j) + " | " + answer[0])
        
        print("")

        if (len(correct_answers[i]) > 1):
            print("Plusieurs réponses sont correctes.")

        valid_letters = [chr(65 + i) for i in range(len(a))]
        answer_string = input_with_retry(
            "Votre réponse: ",
            lambda x: all(letter.upper() in valid_letters for letter in x) and (len(correct_answers[i]) > 1 or len(x) == 1),
            "Réponse invalide.\nRéessayez : "
        )
        answer_set = parse_answer_string(answer_string, len(a))
        user_answers.append(answer_set)

    print("─" * line_length)

    score = 0
    for i in range(len(user_answers)):
        for a in user_answers[i]:
            if a in correct_answers[i]:
                score += 1
            elif malus:
                score -= 1

    # limiter à 0
    score = max(0, score)
    print(generate_box("Votre score est " + str(score)+"/"+str(max_score)))