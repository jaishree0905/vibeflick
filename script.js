// VibeFlick - Interactive Movie Recommendation Frontend

// Mood Selection Handler
const moodCards = document.querySelectorAll('.mood-card');
const languageSelect = document.getElementById('language');
const durationSelect = document.getElementById('duration');
const currentMoodDisplay = document.getElementById('current-mood');
const currentLangDisplay = document.getElementById('current-lang');
const currentTimeDisplay = document.getElementById('current-time');
const findMovieBtn = document.getElementById('find-movie');
const surpriseMeBtn = document.getElementById('surprise-me');

let selectedMood = null;

// Mood Card Selection
moodCards.forEach(card => {
    card.addEventListener('click', () => {
        // Remove active class from all cards
        moodCards.forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked card
        card.classList.add('active');
        
        // Store selected mood
        selectedMood = card.dataset.mood;
        
        // Update display
        currentMoodDisplay.textContent = selectedMood;
        
        // Add animation
        card.style.animation = 'none';
        setTimeout(() => {
            card.style.animation = '';
        }, 10);
    });
});

// Language Selection Handler
languageSelect.addEventListener('change', function() {
    const selected = this.options[this.selectedIndex].text;
    currentLangDisplay.textContent = selected.split(' ')[0];
});

// Duration Selection Handler
durationSelect.addEventListener('change', function() {
    const selected = this.options[this.selectedIndex].text;
    const duration = selected.split(' ')[0];
    currentTimeDisplay.textContent = duration;
});

// Find Movie Button Handler
findMovieBtn.addEventListener('click', () => {
    if (!selectedMood) {
        alert('Please select a mood first! 🎭');
        return;
    }
    
    showLoading();
    
    // Simulate API call delay
    setTimeout(() => {
        showMovieResult();
    }, 2000);
});

// Surprise Me Button Handler
surpriseMeBtn.addEventListener('click', () => {
    // Select random mood
    const randomMood = moodCards[Math.floor(Math.random() * moodCards.length)];
    randomMood.click();
    
    // Set random language
    const langs = languageSelect.options;
    languageSelect.selectedIndex = Math.floor(Math.random() * langs.length);
    languageSelect.dispatchEvent(new Event('change'));
    
    // Set random duration
    const durations = durationSelect.options;
    durationSelect.selectedIndex = Math.floor(Math.random() * durations.length);
    durationSelect.dispatchEvent(new Event('change'));
    
    // Show loading
    showLoading();
    
    // Show result after delay
    setTimeout(() => {
        showMovieResult();
    }, 2000);
});

// Show Loading State
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('movie-card').classList.add('hidden');
    document.getElementById('error-message').classList.add('hidden');
}

// Show Movie Result
function showMovieResult() {
    // Sample movie data based on mood
    const movies = {
        'Happy': {
            title: 'The Grand Budapest Hotel',
            poster: 'https://via.placeholder.com/350x450?text=The+Grand+Budapest+Hotel',
            description: 'A whimsical comedy adventure that\'ll make your heart sing! Perfect for when you\'re feeling upbeat and want to celebrate life\'s beautiful moments.'
        },
        'Sad': {
            title: 'The Shawshank Redemption',
            poster: 'https://via.placeholder.com/350x450?text=The+Shawshank+Redemption',
            description: 'A deeply moving story of hope and friendship that will touch your soul. Sometimes we need to feel our emotions fully to heal.'
        },
        'Romantic': {
            title: 'La La Land',
            poster: 'https://via.placeholder.com/350x450?text=La+La+Land',
            description: 'A mesmerizing journey of love, dreams, and passion. Let this musical romance sweep you away on a tide of emotion and artistry.'
        },
        'Bored': {
            title: 'Mad Max: Fury Road',
            poster: 'https://via.placeholder.com/350x450?text=Mad+Max+Fury+Road',
            description: 'Non-stop adrenaline-pumping action that\'ll keep you on the edge of your seat. Pure cinematic spectacle and thrilling adventure!'
        },
        'Stressed': {
            title: 'Spirited Away',
            poster: 'https://via.placeholder.com/350x450?text=Spirited+Away',
            description: 'Escape into a magical, ethereal world. This stunning animated film is therapeutic and will help you find inner peace.'
        },
        'Lonely': {
            title: 'WALL-E',
            poster: 'https://via.placeholder.com/350x450?text=WALL-E',
            description: 'A heartwarming tale of connection and belonging. This adorable film reminds us about love and companionship.'
        },
        'Excited': {
            title: 'Avengers: Endgame',
            poster: 'https://via.placeholder.com/350x450?text=Avengers+Endgame',
            description: 'Epic superhero action that matches your energy! Buckle up for an unforgettable ride of heroism and triumph.'
        }
    };
    
    const movie = movies[selectedMood] || movies['Happy'];
    
    document.getElementById('movie-poster').src = movie.poster;
    document.getElementById('movie-poster').alt = movie.title;
    document.getElementById('movie-title').textContent = movie.title;
    document.getElementById('movie-desc').textContent = movie.description;
    
    // Update tags
    document.getElementById('tag-mood').textContent = `Mood: ${selectedMood}`;
    document.getElementById('tag-lang').textContent = `Lang: ${languageSelect.options[languageSelect.selectedIndex].text.split(' ')[0]}`;
    document.getElementById('tag-dur').textContent = `Duration: ${durationSelect.options[durationSelect.selectedIndex].text.split(' ')[0]}`;
    
    // Hide loading and error, show movie
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('movie-card').classList.remove('hidden');
    document.getElementById('error-message').classList.add('hidden');
}

// Scroll animation on load
window.addEventListener('load', () => {
    const elements = document.querySelectorAll('.mood-card, .stat-item, .controls-container');
    elements.forEach((el, index) => {
        el.style.animation = `fadeInDown 0.6s ease forwards`;
        el.style.animationDelay = `${index * 0.1}s`;
    });
});

console.log('VibeFlick loaded successfully! 🍿');
const apiKey = "YOUR_API_KEY";
const container = document.getElementById("movie-container");

fetch(`https://www.omdbapi.com/?s=avengers&apikey=${apiKey}`)
  .then(res => res.json())
  .then(data => {
    container.innerHTML = "";

    data.Search.forEach(movie => {
      const card = document.createElement("div");
      card.classList.add("movie-card");

      card.innerHTML = `
        <img src="${movie.Poster}" />
        <h4>${movie.Title}</h4>
      `;

      container.appendChild(card);
    });
  });