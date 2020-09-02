/**
 * Dependancies:
 *      components/chartBlockSlider.js
 *      components/statsBlock.js
 *      util.js
 */

/**
 * Updates the charts based on the usernames
 * @param {string[]} usernames 
 * 
 * TODO more than two users
 */
async function createComparisonCharts(usernames){

    updateTitle(`Loading comparison between ${usernames[0]} and ${usernames[1]}`);

    showElementsByIds(["stats-block-1-2", "stats-block-2-2", "stats-block-3-2"]);

    let statsPage = document.getElementById("stats-page");
    statsPage.classList.add("stats-page-double");
    statsPage.classList.remove("stats-page-single");

    // Aquire data
    let args = {"usernames": usernames};
    let response = await fetch("/ajax/compare", getFetchContext(args));

    // Parse to json format
    let data = await response.json();

    createChartBlockSlider("stats-chart-artists", data["artist_comparison"], " songs");
    chartBlockSliderLegend("stats-chart-artists", "Artist comparison", usernames);

    createChartBlockSlider("stats-chart-genres", data["genre_comparison"], " genres");
    chartBlockSliderLegend("stats-chart-genres", "Genre comparison", usernames);

    statsBlock("stats-block-1-1", data["shared_songs"], "Songs in common");
    
    statsBlock("stats-block-1-2", data["unique_songs"], "Unique songs");

    statsBlock("stats-block-2-1", data["shared_artists"], "Artists in common");
    
    statsBlock("stats-block-2-2", data["unique_artists"], "Unique artists");

    statsBlock("stats-block-3-1", data["shared_genres"], "Genres in common");

    statsBlock("stats-block-3-2", data["unique_genres"], "Unique genres");

    updateTitle(`Comparison between ${usernames[0]} and ${usernames[1]}`);
}
