const searchMovies = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/movies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: 'Inception',
            year: '2010',
            genre: '28' // アクション
        }),
    });

    const data = await response.json();
    console.log(data);
};

searchMovies();