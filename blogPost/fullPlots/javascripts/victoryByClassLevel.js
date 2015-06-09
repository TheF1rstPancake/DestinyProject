//var plotDiv = "#testPlot svg"
var False = false;
var None = null;


var data = $.getJSON('datafiles/victoryByClassLevel.json', function(test_data){
    var plotDiv = "#victoryByClassLevel";
    var plotSvg = plotDiv + " svg";
    var margin = {top: 20, right: 50, bottom: 10, left: 50};
    nv.addGraph({
        generate: function() {
            var width = $(plotDiv).width() - margin.right - margin.left,
                height = ($(plotDiv).height()*3) - margin.top - margin.bottom;
            
            var chart = nv.models.lineChart()
                .width(width)
                .height(height)
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
                ;

            chart.yAxis
                .tickFormat(d3.format(',.3f'));

            chart.xAxis.rotateLabels(-25);


            chart.dispatch.on('renderEnd', function(){
                console.log('Render Complete');
            });

            var svg = d3.select(plotSvg).datum(test_data);
            console.log('calling chart');
            svg.attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .transition().duration(0)
                    .call(chart);


            return chart;
        },
        callback: function(graph) {
           nv.utils.windowResize(function() {
                width = $(plotDiv).width() - margin.right - margin.left,
                height = ($(plotDiv).height()) - margin.top - margin.bottom;
                graph.width(width).height(height);

                d3.select(plotSvg)
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .transition().duration(0)
                    .call(graph);

            });
        }
    });
});