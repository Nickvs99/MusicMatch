document.addEventListener('DOMContentLoaded', () => {

    horizontalBarChart('artistChart', artists, user1_artist_count, user2_artist_count, "Most in common artists");
    horizontalBarChart('genreChart', genres, user1_genre_count, user2_genre_count, "Most in common genres"); 

});

// Creates a horizontal bar chart with two datasets.
function horizontalBarChart(id, labels, data1, data2, title){

    // Checks if element exists
    var element = document.getElementById(id);
    if (!element){
        return;
    }
    
    var ctx = element.getContext('2d');
    var myGenreChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels,
            datasets: [{
                label: username1,
                data: data1,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,

            },{
                label: username2,
                data: data2,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
            }],
        },
        options: {
            scales: {
                xAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                    }
                }]
            },
            title: {
                display: true,
                text: title,
              }
        }
    });
}