/**
 * Dependancies:
 *      util.js
 */

/**
 * Create the artist chart.
 * @param {string} id
 * @param {dict} artistCount 
 */
async function createChartBlockSlider(id, dict, valueSuffix) {

    let chartElement = document.getElementById(id);

    removeChildren(chartElement);
    
    console.log("START: ", Date.now())
    
    let keys = Object.keys(dict);
    let values = Object.values(dict);

    let length = keys.length;

    const batchSize = 25;

    for(let i = 0; i < Math.ceil(keys.length/batchSize); i++) {

        let position_end = Math.min(length, (i + 1) * batchSize)
        createChartBlockBatch(chartElement, i * batchSize, position_end, keys, values, valueSuffix);

        console.log(valueSuffix + ", " + i + ", " + Date.now())
        // NOTE It took ~15 sec to scroll through 876 blocks
        // Thus it takes ~17 ms to scroll pased a block

        // Let the browser breath, this stops the site from becoming unresponsive on lower specs (mobile)
        await timeout(500);
    }

    console.log("END", Date.now())
}

function createChartBlockBatch(parent, position_start, position_end, keys, values, valueSuffix) {

    for(let i = position_start; i < position_end; i++) {

        createChartBlock(parent, i + 1, keys[i], values[i], valueSuffix);
    }

}

/**
 * Created a chart block which is used as a legend and thus has no #position
 * @param {string} id The id of the chart
 * @param {string} title The title displayed on the created chart block
 * @param {string[]} legendItems The legend items on the created chart block
 */

function chartBlockSliderLegend(id, title, legendItems) {
    
    let chartElement = document.getElementById(id);

    let chartBlock = createChartBlock(chartElement, null, title, legendItems);

    chartElement.insertBefore(chartBlock, chartElement.firstChild);
}

function createChartBlock(parent, position, key, values, valueSuffix="") {

    let newElement = createElement(parent, "chart-block");

    let positionElement = createElement(newElement, "chart-position-label", `#${position}`); 
    if(!position) {
        positionElement.style.visibility = "hidden";
    }
    
    createElement(newElement, "chart-key-label", capitalize(`${key}`));  
    
    if(Array.isArray(values)) {

        newElement.classList.add("chart-block-height-2");
        for(let value of values) {
            createElement(newElement, "chart-value-label", value + valueSuffix);
        }
    }
    else {
        newElement.classList.add("chart-block-height-1");

        createElement(newElement, "chart-value-label", values + valueSuffix);
    }

    return newElement;
}

function timeout( ms) {
    return new Promise(res => setTimeout(res, ms));
}