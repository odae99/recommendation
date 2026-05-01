import random
from data_loader import load_all_data

POOL_SIZE = 8
EVOLUTION_STEPS = 10
GROUP_SIZE = 6

# تحميل البيانات مرة واحدة
users, products_df, ratings, behavior = load_all_data()

products_list = products_df["product_id"].tolist()


# إنشاء فرد (حل)
def create_individual():
    return random.sample(products_list, GROUP_SIZE)


# التقييم (Fitness Function)
def fitness_function(solution, user_id):

    # توحيد النوع لحل مشكلة عدم التطابق
    user_data = behavior[
        behavior["user_id"].astype(str) == str(user_id)
    ]

    ratings_data = ratings[
        ratings["user_id"].astype(str) == str(user_id)
    ]

    score = 0

    for p in solution:

        # سلوك المستخدم
        rows = user_data[user_data["product_id"] == p]

        for _, r in rows.iterrows():
            score += r["viewed"] * 1
            score += r["clicked"] * 2
            score += r["purchased"] * 5

        # التقييمات
        r2 = ratings_data[ratings_data["product_id"] == p]

        for _, r in r2.iterrows():
            score += r["rating"] * 2

    return score


# التزاوج
def crossover(parent1, parent2):

    cut = random.randint(1, GROUP_SIZE - 1)
    child = parent1[:cut] + parent2[cut:]

    # إزالة التكرار
    return list(set(child))


# الطفرة
def mutation(solution):

    if random.random() < 0.3:
        solution[random.randint(0, len(solution)-1)] = random.choice(products_list)

    return solution


# تشغيل الخوارزمية
def evolve_population(user_id):

    population = [create_individual() for _ in range(POOL_SIZE)]

    for _ in range(EVOLUTION_STEPS):

        population = sorted(
            population,
            key=lambda x: fitness_function(x, user_id),
            reverse=True
        )

        new_population = population[:3]

        while len(new_population) < POOL_SIZE:

            p1 = random.choice(population[:4])
            p2 = random.choice(population[:4])

            child = crossover(p1, p2)
            child = mutation(child)

            new_population.append(child)

        population = new_population

    return population[0]