import sqlite3
import re

DB_FILE = 'vibeflick.db'

movies_raw = [
    ("Titanic", "English", "3h 14m", "Romance / Tragedy", "Romantic", "Romance/Drama", 1997),
    ("Avatar", "English", "2h 42m", "Adventure / Sci-fi", "Excited", "Adventure/Sci-fi", 2009),
    ("Forrest Gump", "English", "2h 22m", "Hope / Drama", "Happy", "Drama", 1994),
    ("The Dark Knight", "English", "2h 32m", "Action / Crime", "Bored", "Action/Crime", 2008),
    ("Good Will Hunting", "English", "2h 22m", "Inspirational", "Happy", "Drama", 1997),
    ("Inception", "English", "2h 28m", "Mind-bending / Thriller", "Bored", "Sci-fi/Thriller", 2010),
    ("Interstellar", "English", "2h 49m", "Sci-fi / Emotional", "Sad", "Sci-fi/Drama", 2014),
    ("The Lion King", "English", "1h 28m", "Family / Emotional", "Happy", "Animation/Family", 1994),
    ("Aladdin", "English", "1h 42m", "Family / Musical", "Happy", "Animation/Musical", 1992),
    ("Joker", "English", "2h 2m", "Psychological / Dark", "Sad", "Psychological/Drama", 2019),
    ("Baahubali: The Beginning", "Telugu", "2h 39m", "Epic / Action", "Excited", "Action/Epic", 2015),
    ("Baahubali: The Conclusion", "Telugu", "2h 47m", "Epic / Revenge", "Excited", "Action/Epic", 2017),
    ("RRR", "Telugu", "3h 7m", "Action / Patriotism", "Excited", "Action/Drama", 2022),
    ("3 Idiots", "Hindi", "2h 50m", "Comedy / Motivation", "Happy", "Comedy/Drama", 2009),
    ("Dangal", "Hindi", "2h 41m", "Sports / Inspiration", "Happy", "Sports/Drama", 2016),
    ("PK", "Hindi", "2h 33m", "Comedy / Social", "Happy", "Comedy/Sci-fi", 2014),
    ("Lagaan", "Hindi", "3h 44m", "Sports / Patriotism", "Excited", "Sports/Drama", 2001),
    ("Kabhi Khushi Kabhie Gham", "Hindi", "3h 30m", "Family / Drama", "Stressed", "Family/Drama", 2001),
    ("Dilwale Dulhania Le Jayenge", "Hindi", "3h 9m", "Romance", "Romantic", "Romance/Drama", 1995),
    ("Taare Zameen Par", "Hindi", "2h 45m", "Emotional / Education", "Sad", "Drama", 2007),
    ("Enthiran", "Tamil", "2h 57m", "Sci-fi / Action", "Excited", "Sci-fi/Action", 2010),
    ("Vikram", "Tamil", "2h 53m", "Action / Thriller", "Bored", "Action/Thriller", 2022),
    ("Leo", "Tamil", "2h 59m", "Action", "Excited", "Action/Thriller", 2023),
    ("Jai Bhim", "Tamil", "2h 44m", "Court / Emotional", "Sad", "Courtroom/Drama", 2021),
    ("96", "Tamil", "2h 38m", "Love / Nostalgia", "Romantic", "Romance", 2018),
    ("Super Deluxe", "Tamil", "2h 40m", "Philosophical", "Lonely", "Drama/Thriller", 2019),
    ("Vada Chennai", "Tamil", "3h 8m", "Action / Social", "Bored", "Action/Crime", 2018),
    ("Kaithi", "Tamil", "2h 25m", "Action / Thriller", "Excited", "Action/Thriller", 2019),
    ("Soorarai Pottru", "Tamil", "2h 33m", "Inspirational", "Happy", "Drama", 2020),
    ("Ratsasan", "Tamil", "1h 58m", "Crime / Dark", "Bored", "Crime/Thriller", 2018),
    ("Parasite", "Korean", "2h 12m", "Thriller / Social", "Bored", "Thriller/Drama", 2019),
    ("Train to Busan", "Korean", "1h 58m", "Horror / Emotional", "Excited", "Horror/Thriller", 2016),
    ("Oldboy", "Korean", "2h 0m", "Revenge / Dark", "Bored", "Action/Thriller", 2003),
    ("The Handmaiden", "Korean", "2h 25m", "Drama / Romance", "Romantic", "Romance/Drama", 2016),
    ("A Taxi Driver", "Korean", "2h 17m", "Historical / Emotional", "Sad", "Historical/Drama", 2017),
    ("Your Name", "Japanese", "1h 46m", "Romance / Fantasy", "Romantic", "Animation/Romance", 2016),
    ("Spirited Away", "Japanese", "2h 5m", "Fantasy", "Stressed", "Animation/Fantasy", 2001),
    ("Grave of the Fireflies", "Japanese", "1h 29m", "Tragedy", "Sad", "Animation/Drama", 1988),
    ("Weathering with You", "Japanese", "1h 52m", "Romance", "Romantic", "Animation/Romance", 2019),
    ("Akira", "Japanese", "2h 4m", "Sci-fi", "Bored", "Animation/Sci-fi", 1988),
    ("The Avengers", "English", "2h 23m", "Superhero", "Excited", "Action/Sci-fi", 2012),
    ("Avengers: Endgame", "English", "3h 1m", "Epic / Emotional", "Excited", "Action/Sci-fi", 2019),
    ("Gladiator", "English", "2h 35m", "War / Revenge", "Excited", "Action/Drama", 2000),
    ("The Matrix", "English", "2h 16m", "Sci-fi", "Bored", "Sci-fi/Action", 1999),
    ("Fight Club", "English", "2h 19m", "Psychological", "Bored", "Drama/Thriller", 1999),
    ("The Godfather", "English", "2h 55m", "Crime / Family", "Bored", "Crime/Drama", 1972),
    ("The Godfather Part II", "English", "3h 22m", "Crime", "Bored", "Crime/Drama", 1974),
    ("Rocky", "English", "2h 0m", "Sports / Motivation", "Happy", "Sports/Drama", 1976),
    ("Dead Poets Society", "English", "1h 57m", "Inspirational", "Happy", "Drama", 1989),
    ("Life of Pi", "English", "2h 7m", "Survival / Spiritual", "Lonely", "Adventure/Drama", 2012),
    ("Slumdog Millionaire", "Hindi", "2h 0m", "Drama", "Happy", "Drama", 2008),
    ("Black Panther", "English", "2h 14m", "Superhero", "Excited", "Action/Sci-fi", 2018),
    ("Harry Potter and the Sorcerer's Stone", "English", "1h 55m", "Fantasy", "Stressed", "Fantasy/Adventure", 2001),
    ("Spider-Man: No Way Home", "English", "2h 28m", "Superhero", "Excited", "Action/Sci-fi", 2021),
    ("Die Hard", "English", "2h 11m", "Action", "Excited", "Action/Thriller", 1988),
    ("The Notebook", "English", "2h 3m", "Romance", "Romantic", "Romance/Drama", 2004),
    ("La La Land", "English", "2h 8m", "Musical / Love", "Romantic", "Musical/Romance", 2016),
    ("Eternal Sunshine of the Spotless Mind", "English", "2h 6m", "Romantic Sci-fi", "Romantic", "Sci-fi/Romance", 2004),
    ("Cast Away", "English", "2h 23m", "Survival", "Lonely", "Adventure/Drama", 2000),
    ("The Martian", "English", "2h 24m", "Sci-fi / Survival", "Lonely", "Sci-fi/Adventure", 2015),
    ("Drishyam", "Hindi", "2h 43m", "Thriller", "Bored", "Thriller/Drama", 2015),
    ("Kahaani", "Hindi", "2h 20m", "Mystery", "Bored", "Mystery/Thriller", 2012),
    ("Pushpa: The Rise", "Telugu", "2h 59m", "Action", "Excited", "Action/Crime", 2021),
    ("Arjun Reddy", "Telugu", "3h 6m", "Intense Romance", "Romantic", "Romance/Drama", 2017),
    ("Kantara", "Kannada", "2h 30m", "Myth / Thriller", "Excited", "Mystery/Thriller", 2022),
    ("Toy Story", "English", "1h 21m", "Friendship", "Stressed", "Animation/Family", 1995),
    ("Inside Out", "English", "1h 43m", "Emotional", "Happy", "Animation/Family", 2015),
    ("Finding Nemo", "English", "1h 40m", "Family", "Stressed", "Animation/Family", 2003),
    ("Up", "English", "1h 36m", "Adventure / Emotional", "Happy", "Animation/Family", 2009),
    ("Coco", "English", "1h 45m", "Family / Culture", "Stressed", "Animation/Family", 2017),
    ("John Wick", "English", "2h 0m", "Action", "Bored", "Action/Thriller", 2014),
    ("Taken", "English", "1h 41m", "Action", "Bored", "Action/Thriller", 2008),
    ("John Wick: Chapter 4", "English", "2h 49m", "Action", "Bored", "Action/Thriller", 2023),
    ("Mission: Impossible - Fallout", "English", "2h 27m", "Spy Action", "Excited", "Action/Spy", 2018),
    ("Edge of Tomorrow", "English", "1h 53m", "Sci-fi Action", "Excited", "Sci-fi/Action", 2014),
    ("Superbad", "English", "1h 40m", "Comedy", "Happy", "Comedy", 2007),
    ("Knives Out", "English", "2h 10m", "Mystery", "Bored", "Mystery/Comedy", 2019),
    ("Gone Girl", "English", "2h 19m", "Mystery", "Lonely", "Mystery/Thriller", 2014),
    ("A Quiet Place", "English", "1h 30m", "Horror", "Excited", "Horror/Sci-fi", 2018),
    ("Get Out", "English", "1h 44m", "Horror / Social", "Bored", "Horror/Thriller", 2017),
    ("The Conjuring", "English", "1h 52m", "Horror", "Excited", "Horror/Thriller", 2013),
    ("Halloween", "English", "1h 39m", "Horror", "Excited", "Horror/Slasher", 1978),
    ("It", "English", "2h 15m", "Horror", "Excited", "Horror/Thriller", 2017),
    ("The Shining", "English", "2h 2m", "Horror", "Sad", "Horror/Thriller", 1980),
    ("Black Swan", "English", "1h 43m", "Psychological", "Lonely", "Psychological/Thriller", 2010),
    ("Green Book", "English", "2h 6m", "Inspirational", "Happy", "Drama/Comedy", 2018),
    ("The Pursuit of Happyness", "English", "2h 8m", "Motivational", "Happy", "Drama", 2006),
    ("Whiplash", "English", "1h 47m", "Intense Drama", "Bored", "Drama/Music", 2014),
    ("Oppenheimer", "English", "3h 0m", "Biography", "Sad", "Biography/Drama", 2023),
    ("1917", "English", "1h 59m", "War", "Excited", "War/Drama", 2019),
    ("Dunkirk", "English", "1h 46m", "War", "Excited", "War/Action", 2017),
    ("Saving Private Ryan", "English", "2h 49m", "War", "Sad", "War/Drama", 1998),
    ("The Silence of the Lambs", "English", "1h 58m", "Thriller", "Bored", "Thriller/Crime", 1991),
    ("Se7en", "English", "2h 7m", "Crime Thriller", "Bored", "Crime/Mystery", 1995),
    ("Zodiac", "English", "2h 37m", "Crime Mystery", "Bored", "Crime/Mystery", 2007),
    ("The Green Mile", "English", "3h 9m", "Emotional", "Sad", "Drama/Fantasy", 1999),
    ("Schindler's List", "English", "3h 15m", "Historical / Emotional", "Sad", "Biography/Drama", 1993),
    ("The Pianist", "English", "2h 30m", "War Drama", "Sad", "War/Biography", 2002),
    ("The Wolf of Wall Street", "English", "3h 0m", "Biography", "Bored", "Biography/Comedy", 2013),
    ("Braveheart", "English", "3h 0m", "Historical Drama", "Excited", "Biography/Drama", 1995),
]

def parse_duration(duration_str):
    hours = 0
    minutes = 0
    h_match = re.search(r'(\d+)h', duration_str)
    m_match = re.search(r'(\d+)m', duration_str)
    
    if h_match:
        hours = int(h_match.group(1))
    if m_match:
        minutes = int(m_match.group(1))
        
    total_minutes = hours * 60 + minutes
    
    if total_minutes < 90:
        return 'short'
    elif total_minutes <= 120:
        return 'medium'
    else:
        return 'long'

def main():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        inserted = 0
        for m in movies_raw:
            title, lang, dur_str, theme, mood, genre, year = m
            duration = parse_duration(dur_str)
            desc = f"A {dur_str} movie about {theme} that will make you feel {mood}."
            poster = f"https://via.placeholder.com/350x450?text={title.replace(' ', '+')}"
            
            cursor.execute('''
                INSERT INTO movies 
                (title, mood, language, duration, genre, rating, poster_url, description, release_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, mood, lang, duration, genre, 8.0, poster, desc, year))
            inserted += 1
            
        conn.commit()
        print(f"Successfully inserted {inserted} new movies based on the user's emotion list!")
        conn.close()
    except Exception as e:
        print(f"Error inserting movies: {e}")

if __name__ == "__main__":
    main()
