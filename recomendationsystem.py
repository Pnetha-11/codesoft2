import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Optional

class BookRecommendationSystem:
    def __init__(self, similarity_threshold: float = 3.5):
        self.similarity_threshold = similarity_threshold
        self.model = None
        self.user_book_matrix = None
        self.df = None
    
    def load_data(self, data: Dict) -> None:
        self.df = pd.DataFrame(data)
        self.user_book_matrix = self.df.pivot_table(
            index='user', 
            columns='book', 
            values='rating'
        ).fillna(0)
        
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model.fit(self.user_book_matrix)
    
    def get_user_similarity_matrix(self) -> pd.DataFrame:
        similarity_matrix = cosine_similarity(self.user_book_matrix)
        return pd.DataFrame(
            similarity_matrix,
            index=self.user_book_matrix.index,
            columns=self.user_book_matrix.index
        )
    
    def get_similar_users(self, user: str, n_users: int = 3) -> List[Tuple[str, float]]:
        if user not in self.user_book_matrix.index:
            return []
        
        user_index = self.user_book_matrix.index.tolist().index(user)
        distances, indices = self.model.kneighbors(
            self.user_book_matrix.iloc[user_index, :].values.reshape(1, -1),
            n_neighbors=n_users + 1
        )
        
        similar_users = []
        for i, idx in enumerate(indices.flatten()[1:]):
            similar_user = self.user_book_matrix.index[idx]
            similarity = 1 - distances.flatten()[i + 1]
            similar_users.append((similar_user, similarity))
        
        return similar_users
    
    def recommend_books(self, user: str, n_recommendations: int = 3, 
                       show_details: bool = True) -> Optional[List[Tuple[str, float]]]:
        if user not in self.user_book_matrix.index:
            if show_details:
                print(f"  User '{user}' not found in dataset.")
                self._show_available_users()
            return None
        
        user_ratings = self.user_book_matrix.loc[user]
        read_books = user_ratings[user_ratings > 0].index.tolist()
        
        if show_details:
            print(f"\n User: {user}")
            print(f" Books already rated: {', '.join(read_books)}")
        
        similar_users = self.get_similar_users(user, n_users=3)
        
        if show_details:
            print(f" Most similar users:")
            for sim_user, similarity in similar_users:
                print(f"   - {sim_user} (similarity: {similarity:.3f})")
        
        recommendations = {}
        for sim_user, user_similarity in similar_users:
            sim_user_ratings = self.user_book_matrix.loc[sim_user]
            
            for book, rating in sim_user_ratings.items():
                if rating >= self.similarity_threshold and user_ratings[book] == 0:
                    weighted_score = rating * user_similarity
                    recommendations[book] = recommendations.get(book, 0) + weighted_score
        
        recommended_books = sorted(
            recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        if show_details:
            self._display_recommendations(user, recommended_books, n_recommendations)
        
        return recommended_books
    
    def _display_recommendations(self, user: str, recommendations: List[Tuple[str, float]], 
                               n_recommendations: int) -> None:
        print(f"\n Top {n_recommendations} Book Recommendations for {user}:")
        if recommendations:
            for i, (book, score) in enumerate(recommendations, 1):
                print(f"   {i}. {book} (score: {score:.2f})")
        else:
            print("   No new recommendations available based on current data.")
    
    def _show_available_users(self) -> None:
        users = list(self.user_book_matrix.index)
        print(f"Available users: {', '.join(users)}")
    
    def get_user_stats(self, user: str) -> Optional[Dict]:
        if user not in self.user_book_matrix.index:
            return None
        
        user_ratings = self.user_book_matrix.loc[user]
        rated_books = user_ratings[user_ratings > 0]
        
        return {
            'total_books_rated': len(rated_books),
            'average_rating': rated_books.mean(),
            'favorite_books': rated_books[rated_books == rated_books.max()].index.tolist(),
            'books_rated': dict(rated_books)
        }
    
    def display_dataset_overview(self) -> None:
        print("=" * 50)
        print("DATASET OVERVIEW")
        print("=" * 50)
        print(f"Total users: {len(self.user_book_matrix.index)}")
        print(f"Total books: {len(self.user_book_matrix.columns)}")
        print(f"Total ratings: {len(self.df)}")
        print(f"Rating range: {self.df['rating'].min()} - {self.df['rating'].max()}")
        print(f"Average rating: {self.df['rating'].mean():.2f}")
        
        print(f"\n Books in dataset:")
        for book in self.user_book_matrix.columns:
            avg_rating = self.df[self.df['book'] == book]['rating'].mean()
            rating_count = len(self.df[self.df['book'] == book])
            print(f"   - {book} (avg: {avg_rating:.1f}, {rating_count} ratings)")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    recommender = BookRecommendationSystem(similarity_threshold=3.5)

    # Collect data at runtime
    users, books, ratings = [], [], []
    print("Enter book ratings data. Type 'done' to finish.")
    while True:
        user = input("Enter user name (or 'done' to stop): ").strip()
        if user.lower() == 'done':
            break
        book = input("Enter book title: ").strip()
        try:
            rating = float(input("Enter rating (1-5): ").strip())
        except ValueError:
            print("Invalid rating. Skipping...")
            continue
        users.append(user)
        books.append(book)
        ratings.append(rating)

    data = {'user': users, 'book': books, 'rating': ratings}

    recommender.load_data(data)
    recommender.display_dataset_overview()

    while True:
        query_user = input("\nEnter user name for recommendations (or 'exit' to quit): ").strip()
        if query_user.lower() == 'exit':
            break
        recommender.recommend_books(query_user, n_recommendations=3)