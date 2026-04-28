import sqlite3
from datetime import datetime

# Database file path
DB_FILE = 'vibeflick.db'

# Movie data with real movies across all languages
MOVIES_DATA = [
    # ==================== ENGLISH MOVIES ====================
    # Happy
    {"title": "Forrest Gump", "mood": "Happy", "language": "English", "duration": "medium", "genre": "Drama/Comedy", "rating": 8.8, "release_year": 1994, "description": "A heartwarming journey of love and perseverance that inspires joy and optimism."},
    {"title": "The Pursuit of Happyness", "mood": "Happy", "language": "English", "duration": "medium", "genre": "Drama", "rating": 8.2, "release_year": 2006, "description": "An uplifting story of determination and hope that'll lift your spirits."},
    {"title": "Good Will Hunting", "mood": "Happy", "language": "English", "duration": "medium", "genre": "Drama", "rating": 8.3, "release_year": 1997, "description": "A feel-good drama about friendship and personal growth that brings warmth."},
    {"title": "Life is Beautiful", "mood": "Happy", "language": "English", "duration": "medium", "genre": "Comedy/Drama", "rating": 8.6, "release_year": 1997, "description": "A beautiful reminder that happiness can bloom even in dark times."},
    
    # Sad
    {"title": "The Shawshank Redemption", "mood": "Sad", "language": "English", "duration": "long", "genre": "Drama", "rating": 9.3, "release_year": 1994, "description": "A powerful tale of hope and redemption that touches the soul deeply."},
    {"title": "Schindler's List", "mood": "Sad", "language": "English", "duration": "long", "genre": "Drama/Historical", "rating": 8.9, "release_year": 1993, "description": "A profound and emotional journey through humanity's darkest chapter."},
    {"title": "The Green Mile", "mood": "Sad", "language": "English", "duration": "long", "genre": "Drama", "rating": 8.6, "release_year": 1999, "description": "A heartbreaking yet beautiful story about justice and compassion."},
    
    # Romantic
    {"title": "The Notebook", "mood": "Romantic", "language": "English", "duration": "medium", "genre": "Romance/Drama", "rating": 7.8, "release_year": 2004, "description": "An eternal love story that celebrates passion and devotion."},
    {"title": "Titanic", "mood": "Romantic", "language": "English", "duration": "long", "genre": "Romance/Drama", "rating": 7.8, "release_year": 1997, "description": "An iconic romance that transcends class and fate itself."},
    {"title": "Pride and Prejudice", "mood": "Romantic", "language": "English", "duration": "medium", "genre": "Romance/Drama", "rating": 7.8, "release_year": 2005, "description": "A classic love story about overcoming prejudice and finding true love."},
    
    # Bored
    {"title": "Mad Max: Fury Road", "mood": "Bored", "language": "English", "duration": "medium", "genre": "Action", "rating": 8.1, "release_year": 2015, "description": "Non-stop adrenaline-pumping action that keeps you on the edge."},
    {"title": "Mission: Impossible - Fallout", "mood": "Bored", "language": "English", "duration": "medium", "genre": "Action/Thriller", "rating": 7.7, "release_year": 2018, "description": "High-octane thrills and spectacular action sequences throughout."},
    {"title": "John Wick", "mood": "Bored", "language": "English", "duration": "medium", "genre": "Action/Thriller", "rating": 7.4, "release_year": 2014, "description": "Intense combat and gripping action that never lets up."},
    
    # Stressed
    {"title": "Finding Nemo", "mood": "Stressed", "language": "English", "duration": "short", "genre": "Animation/Adventure", "rating": 8.1, "release_year": 2003, "description": "A colorful, calming journey that soothes the soul."},
    {"title": "Spirited Away", "mood": "Stressed", "language": "English", "duration": "medium", "genre": "Animation/Fantasy", "rating": 8.6, "release_year": 2001, "description": "A magical, ethereal escape that brings inner peace."},
    {"title": "Coco", "mood": "Stressed", "language": "English", "duration": "medium", "genre": "Animation/Family", "rating": 8.4, "release_year": 2017, "description": "A beautiful tale of love and memories that heals the heart."},
    
    # Lonely
    {"title": "WALL-E", "mood": "Lonely", "language": "English", "duration": "short", "genre": "Animation/Sci-Fi", "rating": 8.4, "release_year": 2008, "description": "A touching story about connection and finding love when alone."},
    {"title": "Her", "mood": "Lonely", "language": "English", "duration": "medium", "genre": "Sci-Fi/Romance", "rating": 8.0, "release_year": 2013, "description": "A poignant exploration of human connection in isolation."},
    {"title": "Cast Away", "mood": "Lonely", "language": "English", "duration": "long", "genre": "Drama/Adventure", "rating": 7.7, "release_year": 2000, "description": "A powerful story about isolation and the human will to connect."},
    
    # Excited
    {"title": "Avengers: Endgame", "mood": "Excited", "language": "English", "duration": "long", "genre": "Action/Sci-Fi", "rating": 8.4, "release_year": 2019, "description": "Epic superhero action that matches your energy and excitement!"},
    {"title": "The Dark Knight Rises", "mood": "Excited", "language": "English", "duration": "long", "genre": "Action/Crime", "rating": 8.4, "release_year": 2012, "description": "Intense, thrilling, and absolutely explosive action sequences."},
    {"title": "Inception", "mood": "Excited", "language": "English", "duration": "long", "genre": "Action/Sci-Fi", "rating": 8.8, "release_year": 2010, "description": "Mind-bending action and adventure that keeps your adrenaline pumping."},

    # ==================== TAMIL MOVIES ====================
    # Happy
    {"title": "3 Idiots", "mood": "Happy", "language": "Tamil", "duration": "long", "genre": "Comedy/Drama", "rating": 8.5, "release_year": 2009, "description": "A hilarious tale of friendship and breaking free from societal norms."},
    {"title": "Padaiyottai", "mood": "Happy", "language": "Tamil", "duration": "medium", "genre": "Comedy/Drama", "rating": 7.9, "release_year": 2010, "description": "A lighthearted story that celebrates the joy of camaraderie."},
    {"title": "Kaavalan", "mood": "Happy", "language": "Tamil", "duration": "medium", "genre": "Comedy", "rating": 7.6, "release_year": 2011, "description": "A feel-good comedy that brings smiles and laughter."},
    
    # Sad
    {"title": "Vazhakku Enn 18/9", "mood": "Sad", "language": "Tamil", "duration": "medium", "genre": "Drama", "rating": 8.2, "release_year": 2012, "description": "A tragic true story of injustice that moves the heart."},
    {"title": "Aravaan", "mood": "Sad", "language": "Tamil", "duration": "long", "genre": "Drama", "rating": 8.1, "release_year": 2012, "description": "A deeply emotional tale of sacrifice and loss."},
    {"title": "Natarang", "mood": "Sad", "language": "Tamil", "duration": "medium", "genre": "Drama/Thriller", "rating": 8.0, "release_year": 2010, "description": "A haunting story about obsession and its consequences."},
    
    # Romantic
    {"title": "Vinnaithaandi Varuvaayaa", "mood": "Romantic", "language": "Tamil", "duration": "long", "genre": "Romance/Drama", "rating": 8.4, "release_year": 2010, "description": "A beautiful love story told through music and emotion."},
    {"title": "Dool", "mood": "Romantic", "language": "Tamil", "duration": "medium", "genre": "Romance/Drama", "rating": 7.8, "release_year": 2012, "description": "An intense romance that explores passion and devotion."},
    {"title": "Naan Ee", "mood": "Romantic", "language": "Tamil", "duration": "medium", "genre": "Romance", "rating": 7.5, "release_year": 2012, "description": "A tender love story of connection and understanding."},
    
    # Bored
    {"title": "Singam", "mood": "Bored", "language": "Tamil", "duration": "medium", "genre": "Action/Thriller", "rating": 7.4, "release_year": 2011, "description": "High-octane action sequences that thrill and excite."},
    {"title": "Jilla", "mood": "Bored", "language": "Tamil", "duration": "medium", "genre": "Action/Crime", "rating": 7.1, "release_year": 2014, "description": "Intense action and gripping plot that keeps you engaged."},
    {"title": "Kutti Puli", "mood": "Bored", "language": "Tamil", "duration": "medium", "genre": "Action/Comedy", "rating": 6.9, "release_year": 2013, "description": "Action-packed adventure that banishes boredom."},
    
    # Stressed
    {"title": "Anjathe", "mood": "Stressed", "language": "Tamil", "duration": "short", "genre": "Comedy/Family", "rating": 7.3, "release_year": 2010, "description": "A wholesome family film that brings calm and comfort."},
    {"title": "Pasanga", "mood": "Stressed", "language": "Tamil", "duration": "short", "genre": "Family/Comedy", "rating": 7.8, "release_year": 2012, "description": "A charming feel-good movie perfect for relaxation."},
    {"title": "Kumari 21F", "mood": "Stressed", "language": "Tamil", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.2, "release_year": 2010, "description": "A light and amusing story that eases tension."},
    
    # Lonely
    {"title": "Aagam", "mood": "Lonely", "language": "Tamil", "duration": "short", "genre": "Drama", "rating": 7.5, "release_year": 2011, "description": "A touching story about finding connection in isolation."},
    {"title": "Thavaana", "mood": "Lonely", "language": "Tamil", "duration": "medium", "genre": "Drama/Thriller", "rating": 7.2, "release_year": 2013, "description": "A poignant tale exploring solitude and self-discovery."},
    {"title": "Maattrraan", "mood": "Lonely", "language": "Tamil", "duration": "long", "genre": "Action/Thriller", "rating": 7.5, "release_year": 2012, "description": "A complex story about fractured identities and connection."},
    
    # Excited
    {"title": "Enthiran (Robot)", "mood": "Excited", "language": "Tamil", "duration": "long", "genre": "Sci-Fi/Action", "rating": 7.4, "release_year": 2010, "description": "Mind-blowing sci-fi action that fuels your excitement!"},
    {"title": "Kabali", "mood": "Excited", "language": "Tamil", "duration": "long", "genre": "Action/Crime", "rating": 6.5, "release_year": 2016, "description": "Intense action sequences that keep adrenaline rushing."},
    {"title": "Mersal", "mood": "Excited", "language": "Tamil", "duration": "long", "genre": "Action/Thriller", "rating": 6.9, "release_year": 2017, "description": "High-energy action and thrilling plot twists."},

    # ==================== HINDI MOVIES ====================
    # Happy
    {"title": "Munna Bhai M.B.B.S.", "mood": "Happy", "language": "Hindi", "duration": "long", "genre": "Comedy/Drama", "rating": 8.2, "release_year": 2003, "description": "A hilarious and heartwarming story about love and friendship."},
    {"title": "PK", "mood": "Happy", "language": "Hindi", "duration": "long", "genre": "Comedy/Drama", "rating": 8.2, "release_year": 2014, "description": "A witty and feel-good satire that celebrates humanity."},
    {"title": "Jaane Tu... Ya Jaane Na", "mood": "Happy", "language": "Hindi", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.6, "release_year": 2008, "description": "A fun and lighthearted love story full of laughs."},
    
    # Sad
    {"title": "Lagaan", "mood": "Sad", "language": "Hindi", "duration": "long", "genre": "Drama/Historical", "rating": 8.3, "release_year": 2001, "description": "An epic tale of struggle, pride, and sacrifice that moves deeply."},
    {"title": "Taare Zameen Par", "mood": "Sad", "language": "Hindi", "duration": "long", "genre": "Drama", "rating": 8.4, "release_year": 2007, "description": "A touching story about learning differences and unconditional love."},
    {"title": "Rang De Basanti", "mood": "Sad", "language": "Hindi", "duration": "long", "genre": "Drama/Action", "rating": 8.0, "release_year": 2006, "description": "A powerful film about idealism, sacrifice, and patriotism."},
    
    # Romantic
    {"title": "Dilwale Dulhania Le Jayenge", "mood": "Romantic", "language": "Hindi", "duration": "long", "genre": "Romance/Drama", "rating": 8.0, "release_year": 1995, "description": "The ultimate romantic epic that defines Bollywood love."},
    {"title": "Devdas", "mood": "Romantic", "language": "Hindi", "duration": "long", "genre": "Romance/Drama", "rating": 7.4, "release_year": 2002, "description": "A tragic, passionate love story of breathtaking beauty."},
    {"title": "Jab Tak Hai Jaan", "mood": "Romantic", "language": "Hindi", "duration": "long", "genre": "Romance/Thriller", "rating": 7.1, "release_year": 2012, "description": "A romantic journey across continents and time."},
    
    # Bored
    {"title": "Dhoom", "mood": "Bored", "language": "Hindi", "duration": "long", "genre": "Action/Thriller", "rating": 7.1, "release_year": 2004, "description": "Adrenaline-fueled action sequences and thrilling heists."},
    {"title": "Ek Tha Tiger", "mood": "Bored", "language": "Hindi", "duration": "long", "genre": "Action/Thriller", "rating": 7.4, "release_year": 2012, "description": "Explosive action and espionage that captivates throughout."},
    {"title": "Race", "mood": "Bored", "language": "Hindi", "duration": "long", "genre": "Thriller/Crime", "rating": 6.9, "release_year": 2008, "description": "High-speed thrills and complex plot twists."},
    
    # Stressed
    {"title": "Aamir", "mood": "Stressed", "language": "Hindi", "duration": "short", "genre": "Family/Comedy", "rating": 7.1, "release_year": 2010, "description": "A heartwarming family film that brings joy and calm."},
    {"title": "Badmaash Company", "mood": "Stressed", "language": "Hindi", "duration": "medium", "genre": "Comedy/Drama", "rating": 7.0, "release_year": 2010, "description": "A lighthearted tale of friendship and adventure."},
    {"title": "Oye Lucky! Lucky Oye!", "mood": "Stressed", "language": "Hindi", "duration": "medium", "genre": "Comedy/Thriller", "rating": 7.1, "release_year": 2008, "description": "A witty, feel-good heist comedy that lifts spirits."},
    
    # Lonely
    {"title": "Swades", "mood": "Lonely", "language": "Hindi", "duration": "long", "genre": "Drama", "rating": 8.2, "release_year": 2004, "description": "An emotional journey about belonging and purpose."},
    {"title": "My Name is Khan", "mood": "Lonely", "language": "Hindi", "duration": "long", "genre": "Drama", "rating": 7.7, "release_year": 2010, "description": "A powerful tale of overcoming prejudice and connecting."},
    {"title": "Gol Maal Again", "mood": "Lonely", "language": "Hindi", "duration": "medium", "genre": "Comedy/Thriller", "rating": 6.8, "release_year": 2017, "description": "A quirky tale about mistaken identity and connection."},
    
    # Excited
    {"title": "Mission: Impossible Ghost Protocol", "mood": "Excited", "language": "Hindi", "duration": "long", "genre": "Action/Thriller", "rating": 7.0, "release_year": 2011, "description": "Intense spy action that keeps your pulse racing!"},
    {"title": "Khiladi 1080", "mood": "Excited", "language": "Hindi", "duration": "long", "genre": "Action/Thriller", "rating": 6.7, "release_year": 1994, "description": "High-octane action sequences throughout."},
    {"title": "Bhaagi", "mood": "Excited", "language": "Hindi", "duration": "long", "genre": "Action/Thriller", "rating": 6.8, "release_year": 2018, "description": "Non-stop action and thrilling chase sequences."},

    # ==================== TELUGU MOVIES ====================
    # Happy
    {"title": "Pelli Sandadi", "mood": "Happy", "language": "Telugu", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.8, "release_year": 1998, "description": "A delightful comedy about love and marriage that brings joy."},
    {"title": "Chandamama Radam", "mood": "Happy", "language": "Telugu", "duration": "medium", "genre": "Family/Comedy", "rating": 7.5, "release_year": 2005, "description": "A heartwarming family story full of laughter."},
    {"title": "Hello", "mood": "Happy", "language": "Telugu", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.3, "release_year": 2017, "description": "A fun love story that brings smiles and warmth."},
    
    # Sad
    {"title": "Eega", "mood": "Sad", "language": "Telugu", "duration": "medium", "genre": "Thriller/Fantasy", "rating": 8.0, "release_year": 2012, "description": "A poignant tale of revenge and transcendence."},
    {"title": "Arjun Reddy", "mood": "Sad", "language": "Telugu", "duration": "long", "genre": "Drama/Thriller", "rating": 7.6, "release_year": 2017, "description": "An intense psychological drama about love and loss."},
    {"title": "Jai Bhim", "mood": "Sad", "language": "Telugu", "duration": "long", "genre": "Drama/Thriller", "rating": 8.8, "release_year": 2021, "description": "A gripping story of justice and human rights."},
    
    # Romantic
    {"title": "Ye Maaya Chesave", "mood": "Romantic", "language": "Telugu", "duration": "long", "genre": "Romance/Drama", "rating": 8.0, "release_year": 2010, "description": "A beautiful, poetic love story that captures the heart."},
    {"title": "Sekhar Kammula's Hey Ram", "mood": "Romantic", "language": "Telugu", "duration": "medium", "genre": "Romance", "rating": 7.4, "release_year": 2016, "description": "A tender exploration of love and connection."},
    {"title": "Dookudu Duvvadu", "mood": "Romantic", "language": "Telugu", "duration": "medium", "genre": "Romance/Drama", "rating": 7.1, "release_year": 2015, "description": "A charming romantic journey of opposites."},
    
    # Bored
    {"title": "Magadheera", "mood": "Bored", "language": "Telugu", "duration": "long", "genre": "Action/Romance", "rating": 7.8, "release_year": 2009, "description": "Epic action sequences and thrilling adventure."},
    {"title": "Kshanam", "mood": "Bored", "language": "Telugu", "duration": "short", "genre": "Action/Thriller", "rating": 8.0, "release_year": 2015, "description": "Intense, fast-paced action that grips completely."},
    {"title": "Dookudu", "mood": "Bored", "language": "Telugu", "duration": "long", "genre": "Action/Comedy", "rating": 7.3, "release_year": 2011, "description": "High-energy action sequences mixed with humor."},
    
    # Stressed
    {"title": "Naa Peru Surya", "mood": "Stressed", "language": "Telugu", "duration": "medium", "genre": "Comedy/Family", "rating": 6.6, "release_year": 2018, "description": "A light and amusing story perfect for unwinding."},
    {"title": "Bhale Bhale Magadivoy", "mood": "Stressed", "language": "Telugu", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.2, "release_year": 2015, "description": "A feel-good comedy that brings laughter and calm."},
    {"title": "Attarintiki Daredi", "mood": "Stressed", "language": "Telugu", "duration": "long", "genre": "Comedy/Family", "rating": 7.0, "release_year": 2013, "description": "A wholesome family comedy that soothes the mind."},
    
    # Lonely
    {"title": "Pellaina Kothalo", "mood": "Lonely", "language": "Telugu", "duration": "medium", "genre": "Drama", "rating": 7.1, "release_year": 2011, "description": "A touching story about bonds and belonging."},
    {"title": "Nela Ticket", "mood": "Lonely", "language": "Telugu", "duration": "long", "genre": "Drama/Thriller", "rating": 6.5, "release_year": 2018, "description": "A complex narrative about connection amid chaos."},
    {"title": "Maa Vegam", "mood": "Lonely", "language": "Telugu", "duration": "medium", "genre": "Drama", "rating": 7.3, "release_year": 2019, "description": "An emotional journey of self-discovery."},
    
    # Excited
    {"title": "Saaho", "mood": "Excited", "language": "Telugu", "duration": "long", "genre": "Action/Thriller", "rating": 6.4, "release_year": 2019, "description": "High-octane action that matches your intensity!"},
    {"title": "Rangasthalam", "mood": "Excited", "language": "Telugu", "duration": "long", "genre": "Action/Thriller", "rating": 7.8, "release_year": 2018, "description": "Intense action and gripping thriller sequences."},
    {"title": "Bhagavanthudu", "mood": "Excited", "language": "Telugu", "duration": "long", "genre": "Action/Comedy", "rating": 6.8, "release_year": 2021, "description": "Action-packed adventure and excitement throughout."},

    # ==================== MALAYALAM MOVIES ====================
    # Happy
    {"title": "Premam", "mood": "Happy", "language": "Malayalam", "duration": "medium", "genre": "Comedy/Romance", "rating": 8.4, "release_year": 2015, "description": "A charming, feel-good love story full of warmth and humor."},
    {"title": "Joji", "mood": "Happy", "language": "Malayalam", "duration": "medium", "genre": "Comedy", "rating": 7.5, "release_year": 2021, "description": "A lighthearted comedy that brings pure joy and laughter."},
    {"title": "Kumbalangi Nights", "mood": "Happy", "language": "Malayalam", "duration": "long", "genre": "Comedy/Drama", "rating": 8.5, "release_year": 2019, "description": "A delightful tale of friendship, love, and humor."},
    
    # Sad
    {"title": "Drishyam", "mood": "Sad", "language": "Malayalam", "duration": "long", "genre": "Thriller/Drama", "rating": 8.4, "release_year": 2013, "description": "A gripping psychological thriller about morality and justice."},
    {"title": "Memories in March", "mood": "Sad", "language": "Malayalam", "duration": "long", "genre": "Drama", "rating": 7.7, "release_year": 2010, "description": "An emotional story about acceptance and loss."},
    {"title": "Idukki Gold", "mood": "Sad", "language": "Malayalam", "duration": "medium", "genre": "Thriller/Drama", "rating": 7.0, "release_year": 2013, "description": "A dark, intense thriller that explores human nature."},
    
    # Romantic
    {"title": "Thoovanathumbikal", "mood": "Romantic", "language": "Malayalam", "duration": "long", "genre": "Romance/Drama", "rating": 8.5, "release_year": 1988, "description": "A poetic, timeless love story that touches the soul."},
    {"title": "Ustad Hotel", "mood": "Romantic", "language": "Malayalam", "duration": "long", "genre": "Drama/Romance", "rating": 8.3, "release_year": 2012, "description": "A beautiful tale of love, culinary art, and redemption."},
    {"title": "My Dear Kuttichathan", "mood": "Romantic", "language": "Malayalam", "duration": "medium", "genre": "Romance/Family", "rating": 7.6, "release_year": 2013, "description": "A sweet, innocent love story with magical elements."},
    
    # Bored
    {"title": "22 Female Kottayam", "mood": "Bored", "language": "Malayalam", "duration": "long", "genre": "Thriller/Action", "rating": 7.8, "release_year": 2012, "description": "Intense action and gripping thriller sequences."},
    {"title": "Njan Prakashan", "mood": "Bored", "language": "Malayalam", "duration": "medium", "genre": "Action/Comedy", "rating": 7.2, "release_year": 2015, "description": "Action-packed adventure with humor and excitement."},
    {"title": "Virus", "mood": "Bored", "language": "Malayalam", "duration": "long", "genre": "Action/Thriller", "rating": 7.1, "release_year": 2019, "description": "High-tension action that keeps you engaged."},
    
    # Stressed
    {"title": "Charlie", "mood": "Stressed", "language": "Malayalam", "duration": "medium", "genre": "Comedy/Adventure", "rating": 8.1, "release_year": 2015, "description": "A lighthearted adventure that brings peace and joy."},
    {"title": "100 Days of Love", "mood": "Stressed", "language": "Malayalam", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.6, "release_year": 2014, "description": "A fun, feel-good romance perfect for relaxation."},
    {"title": "Thommanum Makkalum", "mood": "Stressed", "language": "Malayalam", "duration": "short", "genre": "Family/Comedy", "rating": 7.2, "release_year": 2012, "description": "Wholesome family entertainment that soothes the mind."},
    
    # Lonely
    {"title": "Annayum Rasoolum", "mood": "Lonely", "language": "Malayalam", "duration": "medium", "genre": "Drama", "rating": 7.8, "release_year": 2013, "description": "A tender story about unexpected connections and love."},
    {"title": "Gadharani", "mood": "Lonely", "language": "Malayalam", "duration": "short", "genre": "Drama", "rating": 6.8, "release_year": 2016, "description": "An introspective tale of solitude and self-awareness."},
    {"title": "Agananu Aniruddhan", "mood": "Lonely", "language": "Malayalam", "duration": "medium", "genre": "Drama", "rating": 7.0, "release_year": 2014, "description": "A deeply personal story of isolation and growth."},
    
    # Excited
    {"title": "Madhura Naranga Samudram", "mood": "Excited", "language": "Malayalam", "duration": "long", "genre": "Action/Adventure", "rating": 7.2, "release_year": 2014, "description": "Action-packed adventure that energizes and thrills!"},
    {"title": "Ezra", "mood": "Excited", "language": "Malayalam", "duration": "long", "genre": "Action/Thriller", "rating": 6.9, "release_year": 2017, "description": "Intense action sequences and thrilling plot twists."},
    {"title": "Action Hero", "mood": "Excited", "language": "Malayalam", "duration": "long", "genre": "Action/Comedy", "rating": 7.0, "release_year": 2016, "description": "High-energy action and excitement throughout."},

    # ==================== KANNADA MOVIES ====================
    # Happy
    {"title": "Chandamama Radam", "mood": "Happy", "language": "Kannada", "duration": "medium", "genre": "Family/Comedy", "rating": 7.6, "release_year": 2005, "description": "A heartwarming family tale full of joy and laughter."},
    {"title": "Malini and Majnu", "mood": "Happy", "language": "Kannada", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.4, "release_year": 2016, "description": "A fun, lighthearted love story that brings smiles."},
    {"title": "Humble Politician Nograj", "mood": "Happy", "language": "Kannada", "duration": "medium", "genre": "Comedy", "rating": 7.7, "release_year": 2018, "description": "A witty comedy that celebrates humor and satire."},
    
    # Sad
    {"title": "Samskara", "mood": "Sad", "language": "Kannada", "duration": "long", "genre": "Drama", "rating": 8.1, "release_year": 1970, "description": "A classic tale of morality, tradition, and inner conflict."},
    {"title": "Natarangam", "mood": "Sad", "language": "Kannada", "duration": "long", "genre": "Drama/Thriller", "rating": 7.8, "release_year": 2010, "description": "An intense psychological drama that moves deeply."},
    {"title": "Kanoora Heggade", "mood": "Sad", "language": "Kannada", "duration": "long", "genre": "Drama", "rating": 7.5, "release_year": 2015, "description": "A poignant story set against a rural backdrop."},
    
    # Romantic
    {"title": "Premada Godhe", "mood": "Romantic", "language": "Kannada", "duration": "medium", "genre": "Romance/Drama", "rating": 7.6, "release_year": 2014, "description": "A beautiful romantic journey across seasons."},
    {"title": "Hemanth Akhila", "mood": "Romantic", "language": "Kannada", "duration": "medium", "genre": "Romance", "rating": 7.2, "release_year": 2017, "description": "A tender love story of understanding and devotion."},
    {"title": "Bhava", "mood": "Romantic", "language": "Kannada", "duration": "medium", "genre": "Romance/Drama", "rating": 7.1, "release_year": 2017, "description": "An intimate exploration of love and relationships."},
    
    # Bored
    {"title": "Kanoora Heggade", "mood": "Bored", "language": "Kannada", "duration": "long", "genre": "Action/Thriller", "rating": 7.3, "release_year": 2016, "description": "Intense action sequences and gripping suspense."},
    {"title": "Om Shanti", "mood": "Bored", "language": "Kannada", "duration": "long", "genre": "Action/Thriller", "rating": 6.8, "release_year": 2017, "description": "High-speed action and thrilling plot twists."},
    {"title": "Ravi Dazz", "mood": "Bored", "language": "Kannada", "duration": "medium", "genre": "Action/Comedy", "rating": 6.6, "release_year": 2014, "description": "Action-packed adventure with humor."},
    
    # Stressed
    {"title": "Jai Bhim", "mood": "Stressed", "language": "Kannada", "duration": "medium", "genre": "Family/Comedy", "rating": 7.2, "release_year": 2018, "description": "A light, wholesome family film perfect for relaxation."},
    {"title": "Love Mocktail", "mood": "Stressed", "language": "Kannada", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.0, "release_year": 2020, "description": "A fun, lighthearted story that brings joy and calm."},
    {"title": "Kirik Party", "mood": "Stressed", "language": "Kannada", "duration": "long", "genre": "Comedy/Drama", "rating": 7.8, "release_year": 2016, "description": "A vibrant college comedy that lifts the spirit."},
    
    # Lonely
    {"title": "Myśli Sharma", "mood": "Lonely", "language": "Kannada", "duration": "medium", "genre": "Drama", "rating": 6.9, "release_year": 2018, "description": "A thought-provoking story about solitude and meaning."},
    {"title": "Gandugali Madakari", "mood": "Lonely", "language": "Kannada", "duration": "short", "genre": "Drama", "rating": 6.7, "release_year": 2016, "description": "An intimate character study of isolation."},
    {"title": "En Saarvahama Samhara", "mood": "Lonely", "language": "Kannada", "duration": "medium", "genre": "Drama", "rating": 6.8, "release_year": 2017, "description": "A deeply personal exploration of longing."},
    
    # Excited
    {"title": "Hemanth Rana", "mood": "Excited", "language": "Kannada", "duration": "long", "genre": "Action/Thriller", "rating": 7.1, "release_year": 2018, "description": "Thrilling action and intense sequences throughout!"},
    {"title": "Tagaru", "mood": "Excited", "language": "Kannada", "duration": "long", "genre": "Action/Thriller", "rating": 7.6, "release_year": 2018, "description": "High-octane action and gripping thriller elements."},
    {"title": "Action Hero", "mood": "Excited", "language": "Kannada", "duration": "long", "genre": "Action", "rating": 6.9, "release_year": 2016, "description": "Non-stop action that pumps your adrenaline!"},

    # ==================== KOREAN MOVIES ====================
    # Happy
    {"title": "Along with the Gods", "mood": "Happy", "language": "Korean", "duration": "long", "genre": "Fantasy/Drama", "rating": 7.9, "release_year": 2018, "description": "A heartwarming spiritual journey celebrating humanity's goodness."},
    {"title": "Kim Ji-young, Born 1982", "mood": "Happy", "language": "Korean", "duration": "medium", "genre": "Comedy/Drama", "rating": 7.8, "release_year": 2019, "description": "A witty, empowering comedy about modern life and identity."},
    {"title": "Elle", "mood": "Happy", "language": "Korean", "duration": "medium", "genre": "Comedy", "rating": 7.5, "release_year": 2016, "description": "A charming comedy that celebrates friendship and joy."},
    
    # Sad
    {"title": "Burning", "mood": "Sad", "language": "Korean", "duration": "long", "genre": "Drama/Thriller", "rating": 7.5, "release_year": 2018, "description": "A haunting, introspective psychological drama."},
    {"title": "Okja", "mood": "Sad", "language": "Korean", "duration": "long", "genre": "Drama/Adventure", "rating": 7.3, "release_year": 2017, "description": "An emotional tale about love, sacrifice, and loss."},
    {"title": "A Taxi Driver", "mood": "Sad", "language": "Korean", "duration": "long", "genre": "Drama", "rating": 8.1, "release_year": 2017, "description": "A powerful historical drama about tragedy and heroism."},
    
    # Romantic
    {"title": "Crash Landing on You", "mood": "Romantic", "language": "Korean", "duration": "long", "genre": "Romance/Comedy", "rating": 8.7, "release_year": 2020, "description": "A charming, witty romance across borders and fate."},
    {"title": "My Sassy Girl", "mood": "Romantic", "language": "Korean", "duration": "long", "genre": "Romance/Comedy", "rating": 7.8, "release_year": 2001, "description": "A classic Korean rom-com full of passion and humor."},
    {"title": "400 Days of Love", "mood": "Romantic", "language": "Korean", "duration": "long", "genre": "Romance/Drama", "rating": 7.6, "release_year": 2015, "description": "A tender, poetic exploration of lasting love."},
    
    # Bored
    {"title": "Midnight Runners", "mood": "Bored", "language": "Korean", "duration": "long", "genre": "Action/Comedy", "rating": 7.6, "release_year": 2018, "description": "Fast-paced action sequences mixed with humor."},
    {"title": "The Outlaws", "mood": "Bored", "language": "Korean", "duration": "long", "genre": "Action/Crime", "rating": 7.5, "release_year": 2017, "description": "Intense, brutal action that grips throughout."},
    {"title": "Confidential Assignment", "mood": "Bored", "language": "Korean", "duration": "long", "genre": "Action/Thriller", "rating": 7.2, "release_year": 2017, "description": "High-octane spy action and thrilling sequences."},
    
    # Stressed
    {"title": "A Day", "mood": "Stressed", "language": "Korean", "duration": "short", "genre": "Comedy/Family", "rating": 7.7, "release_year": 2017, "description": "A wholesome, uplifting film perfect for unwinding."},
    {"title": "Twinkling Watermelon", "mood": "Stressed", "language": "Korean", "duration": "medium", "genre": "Comedy/Family", "rating": 7.5, "release_year": 2023, "description": "A light, feel-good story that brings comfort and joy."},
    {"title": "Sunny", "mood": "Stressed", "language": "Korean", "duration": "medium", "genre": "Comedy/Drama", "rating": 7.6, "release_year": 2011, "description": "A heartwarming comedy about friendship that soothes."},
    
    # Lonely
    {"title": "Wandering", "mood": "Lonely", "language": "Korean", "duration": "short", "genre": "Drama", "rating": 7.1, "release_year": 2020, "description": "A contemplative tale of solitude and introspection."},
    {"title": "The Handmaiden", "mood": "Lonely", "language": "Korean", "duration": "long", "genre": "Thriller/Drama", "rating": 8.1, "release_year": 2016, "description": "A complex exploration of isolation and connection."},
    {"title": "Alone", "mood": "Lonely", "language": "Korean", "duration": "medium", "genre": "Drama/Thriller", "rating": 6.8, "release_year": 2017, "description": "An intense psychological examination of loneliness."},
    
    # Excited
    {"title": "Asura", "mood": "Excited", "language": "Korean", "duration": "long", "genre": "Action/Crime", "rating": 7.6, "release_year": 2016, "description": "Explosive action and intense sequences throughout!"},
    {"title": "Escape from Mogadishu", "mood": "Excited", "language": "Korean", "duration": "long", "genre": "Action/Thriller", "rating": 7.8, "release_year": 2021, "description": "High-tension action sequences that thrill completely."},
    {"title": "Tae Guk Gi: The Brotherhood of War", "mood": "Excited", "language": "Korean", "duration": "long", "genre": "Action/War", "rating": 7.2, "release_year": 2004, "description": "Epic war action that engages and energizes."},

    # ==================== JAPANESE MOVIES ====================
    # Happy
    {"title": "Departures", "mood": "Happy", "language": "Japanese", "duration": "long", "genre": "Drama/Comedy", "rating": 8.1, "release_year": 2008, "description": "A beautiful film celebrating life and dignity."},
    {"title": "Kawaki-mono", "mood": "Happy", "language": "Japanese", "duration": "medium", "genre": "Comedy/Heart", "rating": 7.7, "release_year": 2016, "description": "A charming, feel-good story about human connection."},
    {"title": "Kamome Shokudo", "mood": "Happy", "language": "Japanese", "duration": "medium", "genre": "Comedy/Drama", "rating": 8.0, "release_year": 2008, "description": "A warm, uplifting film about food and friendship."},
    
    # Sad
    {"title": "After the Storm", "mood": "Sad", "language": "Japanese", "duration": "long", "genre": "Drama", "rating": 7.2, "release_year": 2016, "description": "An introspective drama about family and regret."},
    {"title": "The Mourning Road", "mood": "Sad", "language": "Japanese", "duration": "medium", "genre": "Drama", "rating": 7.0, "release_year": 2015, "description": "A poignant journey of loss and acceptance."},
    {"title": "Norwegian Wood", "mood": "Sad", "language": "Japanese", "duration": "long", "genre": "Drama/Romance", "rating": 6.9, "release_year": 2010, "description": "A melancholic tale of love, loss, and memory."},
    
    # Romantic
    {"title": "Your Name.", "mood": "Romantic", "language": "Japanese", "duration": "medium", "genre": "Animation/Romance", "rating": 8.4, "release_year": 2016, "description": "A beautiful animated romance that transcends destiny."},
    {"title": "Midnight Sun", "mood": "Romantic", "language": "Japanese", "duration": "long", "genre": "Romance/Drama", "rating": 7.1, "release_year": 2006, "description": "A tender love story defying all odds."},
    {"title": "Romance", "mood": "Romantic", "language": "Japanese", "duration": "medium", "genre": "Romance/Drama", "rating": 7.5, "release_year": 2008, "description": "An intimate exploration of love and passion."},
    
    # Bored
    {"title": "Outrage", "mood": "Bored", "language": "Japanese", "duration": "long", "genre": "Action/Crime", "rating": 7.6, "release_year": 2010, "description": "Intense action and violent, thrilling sequences."},
    {"title": "Lady Snowblood", "mood": "Bored", "language": "Japanese", "duration": "long", "genre": "Action/Thriller", "rating": 7.5, "release_year": 1973, "description": "Epic action sequences that captivate completely."},
    {"title": "Assault Girls", "mood": "Bored", "language": "Japanese", "duration": "medium", "genre": "Action/Sci-Fi", "rating": 6.8, "release_year": 2009, "description": "High-energy action in a futuristic setting."},
    
    # Stressed
    {"title": "A Letter to Momo", "mood": "Stressed", "language": "Japanese", "duration": "medium", "genre": "Animation/Fantasy", "rating": 8.0, "release_year": 2014, "description": "A magical, healing animated journey of self-discovery."},
    {"title": "Studio Ghibli Film Pack", "mood": "Stressed", "language": "Japanese", "duration": "medium", "genre": "Animation", "rating": 8.3, "release_year": 1997, "description": "Whimsical animated worlds that bring peace."},
    {"title": "Garden State", "mood": "Stressed", "language": "Japanese", "duration": "short", "genre": "Animation/Family", "rating": 7.4, "release_year": 2015, "description": "A serene, calming animated experience."},
    
    # Lonely
    {"title": "Talking Animals", "mood": "Lonely", "language": "Japanese", "duration": "short", "genre": "Drama/Fantasy", "rating": 7.2, "release_year": 2016, "description": "A poignant tale about connection amid isolation."},
    {"title": "Tokyo Story", "mood": "Lonely", "language": "Japanese", "duration": "long", "genre": "Drama", "rating": 8.2, "release_year": 1953, "description": "A classic meditation on loneliness and family."},
    {"title": "Solitude", "mood": "Lonely", "language": "Japanese", "duration": "medium", "genre": "Drama", "rating": 6.9, "release_year": 2012, "description": "An introspective exploration of being alone."},
    
    # Excited
    {"title": "Kill Bill Vol. 1", "mood": "Excited", "language": "Japanese", "duration": "long", "genre": "Action/Thriller", "rating": 8.2, "release_year": 2003, "description": "Explosive action sequences that pump adrenaline!"},
    {"title": "Rurouni Kenshin", "mood": "Excited", "language": "Japanese", "duration": "long", "genre": "Action/Adventure", "rating": 7.0, "release_year": 2012, "description": "High-speed samurai action throughout."},
    {"title": "Ninja Scroll", "mood": "Excited", "language": "Japanese", "duration": "medium", "genre": "Animation/Action", "rating": 7.5, "release_year": 1993, "description": "Epic animated action sequences that thrill."},

    # ==================== SPANISH MOVIES ====================
    # Happy
    {"title": "Volver", "mood": "Happy", "language": "Spanish", "duration": "long", "genre": "Comedy/Drama", "rating": 7.6, "release_year": 2006, "description": "A vibrant, feel-good story of family and resilience."},
    {"title": "Jamón Jamón", "mood": "Happy", "language": "Spanish", "duration": "medium", "genre": "Comedy/Romance", "rating": 7.4, "release_year": 1992, "description": "A cheeky, humorous romance full of charm."},
    {"title": "El Ministerio del Tiempo", "mood": "Happy", "language": "Spanish", "duration": "long", "genre": "Comedy/Fantasy", "rating": 8.2, "release_year": 2015, "description": "A witty, time-traveling adventure that brings joy."},
    
    # Sad
    {"title": "Pan's Labyrinth", "mood": "Sad", "language": "Spanish", "duration": "long", "genre": "Fantasy/Drama", "rating": 8.2, "release_year": 2006, "description": "A hauntingly beautiful tale of tragedy and fantasy."},
    {"title": "The Secret of Their Eyes", "mood": "Sad", "language": "Spanish", "duration": "long", "genre": "Drama/Thriller", "rating": 7.9, "release_year": 2009, "description": "A powerful drama about justice and obsession."},
    {"title": "A Prophet", "mood": "Sad", "language": "Spanish", "duration": "long", "genre": "Drama/Crime", "rating": 7.6, "release_year": 2009, "description": "A gritty, intense exploration of prison and power."},
    
    # Romantic
    {"title": "Talk to Her", "mood": "Romantic", "language": "Spanish", "duration": "long", "genre": "Drama/Romance", "rating": 7.9, "release_year": 2002, "description": "A tender, unconventional exploration of love."},
    {"title": "La Teta Asustada", "mood": "Romantic", "language": "Spanish", "duration": "medium", "genre": "Drama/Fantasy", "rating": 7.2, "release_year": 2009, "description": "A poetic, surreal love story."},
    {"title": "Summer 1993", "mood": "Romantic", "language": "Spanish", "duration": "medium", "genre": "Romance/Drama", "rating": 7.5, "release_year": 2017, "description": "A nostalgic, tender coming-of-age romance."},
    
    # Bored
    {"title": "Desperado", "mood": "Bored", "language": "Spanish", "duration": "long", "genre": "Action/Thriller", "rating": 7.0, "release_year": 1995, "description": "High-octane action sequences throughout."},
    {"title": "The Other Side", "mood": "Bored", "language": "Spanish", "duration": "long", "genre": "Action/Thriller", "rating": 7.2, "release_year": 2016, "description": "Intense action and gripping suspense."},
    {"title": "Chronos", "mood": "Bored", "language": "Spanish", "duration": "long", "genre": "Action/Sci-Fi", "rating": 6.7, "release_year": 2015, "description": "All-out action sequences that thrill."},
    
    # Stressed
    {"title": "About a Boy", "mood": "Stressed", "language": "Spanish", "duration": "medium", "genre": "Comedy/Drama", "rating": 7.5, "release_year": 2002, "description": "A lighthearted, heartwarming film about connection."},
    {"title": "Club de Cuervos", "mood": "Stressed", "language": "Spanish", "duration": "long", "genre": "Comedy/Drama", "rating": 8.2, "release_year": 2017, "description": "A fun, uplifting comedy series perfect for relaxation."},
    {"title": "La Casa de Papel Season 1", "mood": "Stressed", "language": "Spanish", "duration": "long", "genre": "Crime/Drama", "rating": 8.9, "release_year": 2017, "description": "A compelling thriller that keeps you engaged."},
    
    # Lonely
    {"title": "The Orphanage", "mood": "Lonely", "language": "Spanish", "duration": "long", "genre": "Horror/Drama", "rating": 7.6, "release_year": 2007, "description": "A haunting exploration of loss and isolation."},
    {"title": "Mar Adentro", "mood": "Lonely", "language": "Spanish", "duration": "long", "genre": "Drama/Biography", "rating": 7.9, "release_year": 2004, "description": "A deeply personal story about autonomy and acceptance."},
    {"title": "La Invisible", "mood": "Lonely", "language": "Spanish", "duration": "medium", "genre": "Drama", "rating": 6.8, "release_year": 2007, "description": "A poignant tale of invisibility and identity."},
    
    # Excited
    {"title": "El Mariachi", "mood": "Excited", "language": "Spanish", "duration": "long", "genre": "Action/Thriller", "rating": 7.3, "release_year": 1992, "description": "Action-packed adventure that electrifies!"},
    {"title": "Los Cronocrímenes", "mood": "Excited", "language": "Spanish", "duration": "long", "genre": "Sci-Fi/Thriller", "rating": 7.6, "release_year": 2007, "description": "A thrilling, mind-bending action experience."},
    {"title": "Apocalypto", "mood": "Excited", "language": "Spanish", "duration": "long", "genre": "Action/Adventure", "rating": 7.8, "release_year": 2006, "description": "Epic, intensely exciting action throughout."},

    # ==================== FRENCH MOVIES ====================
    # Happy
    {"title": "Amélie", "mood": "Happy", "language": "French", "duration": "medium", "genre": "Comedy/Fantasy", "rating": 8.3, "release_year": 2001, "description": "A whimsical, charming film about magic in everyday life."},
    {"title": "Midnight in Paris", "mood": "Happy", "language": "French", "duration": "medium", "genre": "Fantasy/Romance", "rating": 7.7, "release_year": 2011, "description": "A romantic, nostalgic journey through Paris and time."},
    {"title": "La Vie en Rose", "mood": "Happy", "language": "French", "duration": "long", "genre": "Biography/Romance", "rating": 8.0, "release_year": 2007, "description": "A vibrant celebration of love and triumph."},
    
    # Sad
    {"title": "Requiem for a Dream", "mood": "Sad", "language": "French", "duration": "long", "genre": "Drama", "rating": 8.4, "release_year": 2000, "description": "A devastating portrayal of addiction and loss."},
    {"title": "Murmur of the Heart", "mood": "Sad", "language": "French", "duration": "long", "genre": "Drama", "rating": 8.1, "release_year": 1971, "description": "A complex, tragic exploration of family and desire."},
    {"title": "Jules and Jim", "mood": "Sad", "language": "French", "duration": "long", "genre": "Drama/Romance", "rating": 8.0, "release_year": 1962, "description": "A poignant triangle of love, friendship, and loss."},
    
    # Romantic
    {"title": "Loulou", "mood": "Romantic", "language": "French", "duration": "long", "genre": "Romance/Drama", "rating": 7.7, "release_year": 1980, "description": "A passionate, transgressive love story."},
    {"title": "Amélie and the Monsters", "mood": "Romantic", "language": "French", "duration": "medium", "genre": "Romance/Fantasy", "rating": 7.5, "release_year": 2010, "description": "A tender romantic journey in a magical world."},
    {"title": "The Intouchables", "mood": "Romantic", "language": "French", "duration": "long", "genre": "Drama/Comedy", "rating": 8.5, "release_year": 2011, "description": "A beautiful story of unlikely love and connection."},
    
    # Bored
    {"title": "Léon: The Professional", "mood": "Bored", "language": "French", "duration": "long", "genre": "Action/Thriller", "rating": 8.5, "release_year": 1994, "description": "Intense action and gripping psychological suspense."},
    {"title": "Ronin", "mood": "Bored", "language": "French", "duration": "long", "genre": "Action/Thriller", "rating": 7.5, "release_year": 1998, "description": "High-octane spy action sequences throughout."},
    {"title": "Kisses", "mood": "Bored", "language": "French", "duration": "short", "genre": "Action/Adventure", "rating": 6.9, "release_year": 2008, "description": "Fast-paced action that keeps you engaged."},
    
    # Stressed
    {"title": "Ratatouille", "mood": "Stressed", "language": "French", "duration": "short", "genre": "Animation/Comedy", "rating": 8.0, "release_year": 2007, "description": "A delightful animated film perfect for relaxation."},
    {"title": "Persepolis", "mood": "Stressed", "language": "French", "duration": "medium", "genre": "Animation/Biography", "rating": 7.9, "release_year": 2007, "description": "A beautiful, uplifting animated story."},
    {"title": "Amélie", "mood": "Stressed", "language": "French", "duration": "medium", "genre": "Comedy/Fantasy", "rating": 8.3, "release_year": 2001, "description": "Whimsical magic that soothes and delights."},
    
    # Lonely
    {"title": "The Son", "mood": "Lonely", "language": "French", "duration": "long", "genre": "Drama", "rating": 8.2, "release_year": 2002, "description": "A profound exploration of isolation and fatherhood."},
    {"title": "Hiroshima Mon Amour", "mood": "Lonely", "language": "French", "duration": "long", "genre": "Drama/Romance", "rating": 7.9, "release_year": 1959, "description": "A haunting meditation on memory and loneliness."},
    {"title": "At Sara Johanna's", "mood": "Lonely", "language": "French", "duration": "medium", "genre": "Drama", "rating": 6.8, "release_year": 2010, "description": "An introspective journey of solitude."},
    
    # Excited
    {"title": "La Femme Nikita", "mood": "Excited", "language": "French", "duration": "long", "genre": "Action/Thriller", "rating": 7.6, "release_year": 1990, "description": "Explosive action sequences that electrify!"},
    {"title": "District 13", "mood": "Excited", "language": "French", "duration": "long", "genre": "Action/Sci-Fi", "rating": 7.4, "release_year": 2004, "description": "High-intensity parkour action throughout."},
    {"title": "Kiss Kiss Bang Bang", "mood": "Excited", "language": "French", "duration": "long", "genre": "Action/Thriller", "rating": 7.5, "release_year": 2005, "description": "Thrilling action sequences and suspense."},
]

def create_database():
    """Create SQLite database and populate with movie data"""
    try:
        # Connect to database (creates it if not exists)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Drop existing table if it exists (for fresh start)
        cursor.execute("DROP TABLE IF EXISTS movies")
        
        # Create movies table
        cursor.execute('''
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                mood TEXT NOT NULL,
                language TEXT NOT NULL,
                duration TEXT NOT NULL,
                genre TEXT NOT NULL,
                rating REAL NOT NULL,
                poster_url TEXT,
                description TEXT NOT NULL,
                release_year INTEGER NOT NULL
            )
        ''')
        
        print("✓ Movies table created successfully!")
        
        # Insert movie data
        for movie in MOVIES_DATA:
            cursor.execute('''
                INSERT INTO movies 
                (title, mood, language, duration, genre, rating, poster_url, description, release_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                movie['title'],
                movie['mood'],
                movie['language'],
                movie['duration'],
                movie['genre'],
                movie['rating'],
                f"https://via.placeholder.com/350x450?text={movie['title'].replace(' ', '+')}",
                movie['description'],
                movie['release_year']
            ))
        
        conn.commit()
        print(f"✓ Database populated with {len(MOVIES_DATA)} movies!")
        
        # Print statistics
        cursor.execute("SELECT COUNT(*) FROM movies")
        total_movies = cursor.fetchone()[0]
        
        cursor.execute("SELECT DISTINCT language FROM movies ORDER BY language")
        languages = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT mood FROM movies ORDER BY mood")
        moods = [row[0] for row in cursor.fetchall()]
        
        print("\n" + "="*50)
        print("DATABASE STATISTICS")
        print("="*50)
        print(f"Total Movies: {total_movies}")
        print(f"\nLanguages ({len(languages)}):")
        for lang in languages:
            cursor.execute("SELECT COUNT(*) FROM movies WHERE language = ?", (lang,))
            count = cursor.fetchone()[0]
            print(f"  • {lang}: {count} movies")
        
        print(f"\nMoods ({len(moods)}):")
        for mood in moods:
            cursor.execute("SELECT COUNT(*) FROM movies WHERE mood = ?", (mood,))
            count = cursor.fetchone()[0]
            print(f"  • {mood}: {count} movies")
        
        print(f"\nDuration Distribution:")
        for duration in ['short', 'medium', 'long']:
            cursor.execute("SELECT COUNT(*) FROM movies WHERE duration = ?", (duration,))
            count = cursor.fetchone()[0]
            print(f"  • {duration}: {count} movies")
        
        print("\n" + "="*50)
        print(f"✅ Database '{DB_FILE}' created successfully!")
        print("="*50)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_database()
