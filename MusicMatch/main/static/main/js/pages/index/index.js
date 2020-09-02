/**
 * Dependancies:
 * 		auth.js
 * 		index/compare.js
 * 		index/stats.js
 * 		index/userField.js
 * 		util.js
 */

 document.addEventListener('DOMContentLoaded', () => {

	document.getElementById("formUsernames").onsubmit = async () => {

		event.preventDefault();
		event.stopPropagation();

        clearMessages();
        
		let usernames = getUserNames();

        if(usernames.length == 0) {
            createMessage('danger', 'No input found');
            return false;
        }

		if(! await processingUsernames(usernames, false)){
			return false;
        }
        
		let ids = ["benefits-list", "stats-page", "input-create-playlist"]
        hideElementsByIds(ids);
        
        showElementById("stats-page");

		if(usernames.length == 1){
			createSingleCharts(usernames[0]);
		}
		else {
            showElementById("input-create-playlist");

			createComparisonCharts(usernames);
		}
		return false;
    };
});
