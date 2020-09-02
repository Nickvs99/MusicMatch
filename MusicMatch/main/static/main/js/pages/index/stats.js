/**
 * Dependencies:
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
async function createSingleCharts(username){

    updateTitle("Reading stats for " + username);
    
    hideElementsByIds(["stats-block-1-2", "stats-block-2-2", "stats-block-3-2"]);

    let statsPage = document.getElementById("stats-page");
    statsPage.classList.remove("stats-page-double");
    statsPage.classList.add("stats-page-single");

    let args = {"username": username};
    let response = await fetch("/ajax/stats", getFetchContext(args));

    let data = await response.json()

    let artistCount = data["artist_count"];
    let genreCount = data["genre_count"];


    updateTitle("Stats for " + username);

    statsBlock("stats-block-1-1", data["total_songs"], "Songs");
    
    statsBlock("stats-block-2-1", data["total_artists"], "Artists");
    
    statsBlock("stats-block-3-1", data["total_genres"], "Genres");

    createChartBlockSlider("stats-chart-artists", artistCount, " songs");
    
    createChartBlockSlider("stats-chart-genres", genreCount, " genres");
}