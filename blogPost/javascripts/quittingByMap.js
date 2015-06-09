var data = $.getJSON('datafiles/quittingByMap.json', function(test_data){
    //var plotDiv = "#testPlot svg"
    var plotDiv = "#quittingByMap svg";
    var margin = {top: 20, right: 10, bottom: 20, left: 10};
    var width = 700 - margin.right - margin.left,
        height = 650 - margin.top - margin.bottom;
    var colors = ['#FF0000', '#0000FF']

    nv.addGraph({
        generate: function() {            
            var chart = nv.models.multiBarChart()
                .width(width)
                .height(height)
                .stacked(false)
                .reduceXTicks(false)   //If 'false', every single x-axis tick label will be rendered.
                .color(colors)
                ;

            chart.yAxis
                .tickFormat(d3.format(',.3f'));

            chart.xAxis.rotateLabels(-30);


            chart.dispatch.on('renderEnd', function(){
                console.log('Render Complete');
            });

            var svg = d3.select(plotDiv).datum(test_data);
            console.log('calling chart');
            svg.attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .transition().duration(0)
                .call(chart);


            return chart;
        },
        callback: function(graph) {
            nv.utils.windowResize(function() {
                graph.width(width).height(height);

                d3.select(plotDiv)
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .transition().duration(0)
                    .call(graph);

            });
        }
    });
});
