//var plotDiv = "#testPlot svg"
var False = false;
var None = null;


var data = $.getJSON('datafiles/sniperRatioRate.json', function(test_data){
    var plotDiv = "#sniperRatioRate";
    var plotSvg = plotDiv + " svg";
    var margin = {top: 20, right: 50, bottom: 10, left: 50};

    nv.addGraph({
        generate: function() {   
            var width = $(plotDiv).width() - margin.right - margin.left,
                height = ($(plotDiv).height()*3) - margin.top - margin.bottom;

            var chart = nv.models.multiBarChart()
                .width(width)
                .height(height)
                .stacked(False)
                .reduceXTicks(False)   //If 'false', every single x-axis tick label will be rendered.
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