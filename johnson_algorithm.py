def johnson_algorithm(M1, M2):
    # Vérifier que les matrices M1 et M2 ont la même longueur
    if len(M1) != len(M2):
        raise ValueError("Les matrices M1 et M2 doivent avoir le même nombre de jobs.")

    # Nombre de jobs
    n = len(M1)

    # Initialiser les listes pour les jobs à traiter
    u = []  # Jobs à traiter en premier sur Machine 1
    v = []  # Jobs à traiter en premier sur Machine 2

    # Étape 1 : Séparer les jobs selon les délais
    for i in range(n):
        if M1[i] < M2[i]:
            u.append(i + 1)  # Ajouter à l'ensemble u (indexé à partir de 1)
        else:
            v.append(i + 1)  # Ajouter à l'ensemble v (indexé à partir de 1)

    # Étape 2 : Classer les jobs u par ordre croissant et v par ordre décroissant
    u_sorted = sorted(u, key=lambda x: M1[x - 1])  # Tri croissant pour u
    v_sorted = sorted(v, key=lambda x: M2[x - 1], reverse=True)  # Tri décroissant pour v

    # Étape 3 : Concaténer les résultats
    schedule = u_sorted + v_sorted  # Ordre final des jobs

    # Retourner le résultat (la séquence des jobs)
    return schedule
# Exemples de délais sur Machine 1 et Machine 2
M1 = [7, 6, 7, 11,11,13,11,10]  # Délais pour les jobs sur Machine 1
M2 = [5, 6, 9, 9,5,16,14,5]  # Délais pour les jobs sur Machine 2

sequence = johnson_algorithm(M1, M2)
print("La séquence optimale des jobs est :", sequence)
