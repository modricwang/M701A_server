let __width, __height, __gradient;

function getGradient(ctx, chartArea) {
    const chartWidth = chartArea.right - chartArea.left;
    const chartHeight = chartArea.bottom - chartArea.top;
    if (__gradient === null || __width !== chartWidth || __height !== chartHeight) {
        // Create the gradient because this is either the first render
        // or the size of the chart has changed
        __width = chartWidth;
        __height = chartHeight;
        __gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        __gradient.addColorStop(0, 'rgb(27, 81, 235)');
        // __gradient.addColorStop(0.5, 'rgb(255, 90, 86)');
        __gradient.addColorStop(1, 'rgb(255, 50, 66)');
    }
    return __gradient;
}