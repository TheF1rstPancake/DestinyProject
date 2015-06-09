var plotDiv = "#testPlot svg"
//var plotDiv = "#sniperRatioVictoryPlot svg";
var data = $.getJSON('datafiles/characterClassVictory.json', function(test_data){
    nv.addGraph({
        generate: function() {
            var width = nv.utils.windowSize().width,
                height = nv.utils.windowSize().height;
            /*var width = 700,
                height = 600;*/
            
            var chart = nv.models.multiBarChart()
                .width(width)
                .height(height)
                .stacked(true)
                .reduceXTicks(false)   //If 'false', every single x-axis tick label will be rendered.
                ;

            chart.yAxis
                .tickFormat(d3.format(',.3f'));

            chart.xAxis.rotateLabels(-30);


            chart.dispatch.on('renderEnd', function(){
                console.log('Render Complete');
            });

            var svg = d3.select(plotDiv).datum(test_data);
            console.log('calling chart');
            svg.attr('width', width).attr('height', height).transition().duration(0).call(chart);


            return chart;
        },
        callback: function(graph) {
            nv.utils.windowResize(function() {
                /*var width = 700,
                height = 600;*/
                var width = nv.utils.windowSize().width,
                height = nv.utils.windowSize().height;

                graph.width(width).height(height);

                d3.select(plotDiv)
                    .attr('width', width)
                    .attr('height', height)
                    .transition().duration(0)
                    .call(graph);

            });
        }
    });
});