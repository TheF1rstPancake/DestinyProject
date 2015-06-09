//#var plotDiv = "#testPlot svg"

var data = $.getJSON('datafiles/weapon_sums.json', function(test_data){
    var plotDiv = "#plot";
    var plotSvg = plotDiv + " svg";
    var margin = {top: 20, right: 10, bottom: 20, left: 10};
    nv.addGraph({
        generate: function() {
            var width = $(plotDiv).width() - margin.right - margin.left,
                height = ($(plotDiv).height()) - margin.top - margin.bottom;
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
              
                var width = $(plotDiv).width() - margin.right - margin.left,
                    height = ($(plotDiv).height()) - margin.top - margin.bottom;
                graph.width(width).height(height);

                d3.select(plotSv)
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .transition().duration(0)
                    .call(graph);

            });
        }
    });
});