from sklearn.metrics.pairwise import cosine_similarity

m1 = [[1, 2, 3, 4], [1, 2, 5, 6]]
m2 = [[0, 1, 2, 3, 4], [1, 0, 1, 5, 2]]

user_similarity = cosine_similarity(m2)
print user_similarity

