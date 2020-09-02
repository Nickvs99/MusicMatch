/**
 * Dependancies:
 *      util.js
 */

/**
 * Create the artist chart.
 * @param {string} id
 * @param {dict} artistCount 
 */
function createChartBlockSlider(id, dict, valueSuffix) {

    let chartElement = document.getElementById(id);

    removeChildren(chartElement);
    
    let position = 1;
    for (const [key, values] of Object.entries(dict)) {
        
        let valuesSuffix = appendSuffix(values, valueSuffix);

        createChartBlock(chartElement, position, key, valuesSuffix);

        position += 1;
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

function createChartBlock(parent, position, key, values) {

    let newElement = createElement(parent, "chart-block");

    let positionElement = createElement(newElement, "chart-position-label", `#${position}`); 
    if(!position) {
        positionElement.style.visibility = "hidden";
    }
    
    createElement(newElement, "chart-key-label", capitalize(`${key}`));  
    
    if(Array.isArray(values)) {

        newElement.classList.add("chart-block-height-2");
        for(let value of values) {
            createElement(newElement, "chart-value-label", value);
        }
    }
    else {
        newElement.classList.add("chart-block-height-1");

        createElement(newElement, "chart-value-label", values);
    }

    return newElement;
}