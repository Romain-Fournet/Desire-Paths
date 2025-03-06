import pygame
import random

class Agent:
    def __init__(self, start, dest, moves, steps_taken, taille=10):
        self.x = start[0] * CELL_SIZE  # Position de l'agent sur l'axe X
        self.y = start[1] * CELL_SIZE  # Position de l'agent sur l'axe Y
        self.start = start
        self.dest = dest
        self.taille = taille  # Taille de l'agent (représenté comme un carré)
        self.moves = moves
        self.current_step = 0  # Pour suivre l'étape actuelle
        self.steps_taken = steps_taken  # Nombre de pas réellement utilisés
        

    def se_deplacer(self, move):
        x, y = move
        if(x == 1):
            self.x += CELL_SIZE
        if(x == -1):
            self.x -= CELL_SIZE
        if(y == 1):
            self.y += CELL_SIZE
        if(y == -1):
            self.y -= CELL_SIZE

    def afficher(self, fenetre):
        """Affiche l'agent sur la fenêtre."""
        pygame.draw.rect(fenetre, ROUGE, (self.x, self.y, self.taille, self.taille))
        
class InterestPoint:
    def __init__(self, access, taille = 10):
        self.x = access[0] * CELL_SIZE
        self.y = access[1] * CELL_SIZE
        self.access = access
        self.taille = taille

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, VERT, (self.x, self.y, self.taille, self.taille))


CELL_SIZE = 10
WIN_WIDTH = 150
WIN_HEIGHT = 100
 
# Définir la taille de la fenêtre
PX_WIDTH = WIN_WIDTH * CELL_SIZE
PX_HEIGHT= WIN_HEIGHT * CELL_SIZE
WINDOW = pygame.display.set_mode((PX_WIDTH, PX_HEIGHT))
pygame.display.set_caption("Simulation de Parc")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)


MOVES = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1)]
POP_SIZE = 1000
MAX_STEPS = 80
GENERATION = 100
MUTATION_RATE = 0.2
INTEREST_POINTS = [
    InterestPoint((100, 75)),
    InterestPoint((50, 50)),
    InterestPoint((50, 80))
]
SUB_POP_SIZE = POP_SIZE // (len(INTEREST_POINTS) * (len(INTEREST_POINTS) - 1))

def create_agent(start, dest):
    return Agent(start.access, dest.access, [random.choice(MOVES) for _ in range(MAX_STEPS)], MAX_STEPS)

def eval_agent(agent):
    start_x, start_y = agent.start
    dest_x, dest_y = agent.dest
    x, y = start_x, start_y
    
    score = 1000  # Score de base pour éviter d'avoir trop de zéros
    previous_dist = abs(dest_x - x) + abs(dest_y - y)
    steps_taken = 0
    visited = set()

    for move in agent.moves:
        steps_taken += 1
        dx, dy = move
        new_x, new_y = x + dx, y + dy

        # Vérification des limites de la fenêtre
        if not (0 <= new_x < WIN_WIDTH and 0 <= new_y < WIN_HEIGHT):
            score -= 200  # Forte pénalité pour sortie de zone
            continue  # L'agent ne bouge pas en dehors des limites

        # Mise à jour de la position
        x, y = new_x, new_y

        # Récompense si on atteint la destination
        if (x, y) == (dest_x, dest_y):
            print(steps_taken)
            score += 5000  # Grosse récompense pour atteindre la cible
            agent.steps_taken = steps_taken
            agent.moves = agent.moves[:steps_taken]
            break  # Stopper l'évaluation immédiatement
        
        # Calcul de la distance actuelle
        new_dist = abs(dest_x - x) + abs(dest_y - y)

        # Récompense si l'agent se rapproche de la destination
        if new_dist < previous_dist:
            score += 100  # Augmenter la récompense
        else:
            score -= 30  # Augmenter la pénalité pour les mauvais mouvements

        previous_dist = new_dist

        # Pénalité si l'agent repasse sur une case déjà visitée
        if (x, y) in visited:
            score -= 50  # Réduit le score pour éviter les boucles inutiles

        visited.add((x, y))

    # Pénalité pour le nombre d'étapes prises
    score -= steps_taken * 5  # Favoriser les chemins courts sans punir trop fort
    
    return max(score, 0)  # Éviter les scores négatifs

def select_bests(sous_population):
    scores = [(eval_agent(agent), agent) for agent in sous_population]
    scores.sort(reverse=True, key=lambda x: x[0])  # Trier du meilleur au pire

    elite_count = max(1, SUB_POP_SIZE // 10)  # Garder 10% de l'élite
    best_agents = [agent for _, agent in scores[:elite_count]]

    return best_agents

def crossover(parent1, parent2):
    most_steps_parent = max(parent1.steps_taken, parent2.steps_taken)
    cut_point = random.randint(1, max(1, most_steps_parent - 1))  # Point de coupure aléatoire
    child_moves = parent1.moves[:cut_point] + parent2.moves[cut_point:]

    return Agent(parent1.start, parent1.dest, child_moves, len(child_moves))

def mutate(agent):
    for i in range(agent.steps_taken):
        if random.random() < MUTATION_RATE:
            try:
                agent.moves[i] = random.choice(MOVES)
            except IndexError:
                print(f"Nombre de pas de l'agent : {agent.steps_taken}")
                print(f"Taille des pas de l'agent : {len(agent.moves)}")
                print(f"i posant probleme : {i}")
                print(f"Step taken de l'agent : {agent.steps_taken}")

# Démarre la simulation
def run_simulation(sous_population):
    global MUTATION_RATE
    MUTATION_RATE = 0.2
    font = pygame.font.Font(None, 30)
    # Boucle sur les générations
    for generation in range(GENERATION):
        text = font.render(f"Generation {generation + 1}", True, NOIR, BLANC)
        textRect = text.get_rect()
        textRect.topleft = (0, 0)

        # Sélectionner les meilleurs agents pour la génération suivante
        best_agents = select_bests(sous_population)

        # Appliquer le croisement et la mutation pour créer la nouvelle génération
        new_population = best_agents[:]
        while len(new_population) < SUB_POP_SIZE:
            parent1, parent2 = random.sample(best_agents, 2)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        sous_population = new_population[:SUB_POP_SIZE]  # Mettre à jour la population avec la nouvelle génération

        # Simulation pour cette génération
        running = False

        if generation % 10 == 0 or generation < 10:
            MUTATION_RATE = MUTATION_RATE * 0.85
            running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Remplir la fenêtre avec un fond blanc
            WINDOW.fill(BLANC)  
            WINDOW.blit(text, textRect)

            all_agents_done = True

            for interest_point in INTEREST_POINTS:
                interest_point.afficher(WINDOW)

            # Déplacer et afficher chaque agent
            for agent in sous_population:
                if agent.current_step < agent.steps_taken:
                    agent.se_deplacer(agent.moves[agent.current_step])
                    agent.afficher(WINDOW)
                    agent.current_step += 1  # Passer à l'étape suivante
                    all_agents_done = False  # Tant qu'il y a des agents qui se déplacent

            if all_agents_done:
                pygame.time.delay(500)
                running = False

            pygame.display.flip()  # Met à jour l'affichage

            pygame.time.delay(5)  # Pause pour ralentir un peu l'animation avant de passer à la prochaine génération

            



def main():
    population = {}
    if(SUB_POP_SIZE * 0.1 < 2):
        raise ValueError("SUB_POP_SIZE trop petit. Augmentez la population initiale.")

    pygame.init()
    
    for i in range(len(INTEREST_POINTS)):
        start = INTEREST_POINTS[i]
        for j in range(len(INTEREST_POINTS)):
            if i != j:
                dest = INTEREST_POINTS[j]
                key = (start, dest)
                population[key] = [create_agent(start, dest) for _ in range(SUB_POP_SIZE)]

    for key, sous_population in population.items():
        run_simulation(sous_population)
    
    pygame.quit()  # Fermer Pygame après avoir terminé toutes les générations

main()


