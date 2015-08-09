//var plotDiv = "#testPlot svg"
var False = false;
var None = null;

Array.prototype.contains = function(v) {
    for(var i = 0; i < this.length; i++) {
        if(this[i] === v) return true;
    }
    return false;
};

Array.prototype.unique = function() {
    var arr = [];
    for(var i = 0; i < this.length; i++) {
        if(!arr.contains(this[i])) {
            arr.push(this[i]);
        }
    }
    return arr; 
};

var data = $.getJSON('datafiles/weaponAndVictoryBreakdown.json', function(test_data){
    var plotDiv = "#weaponAndVictoryBreakdown";
    var plotSvg = plotDiv + " svg";
    var margin = {top: 20, right: 50, bottom: 10, left: 50};

    nv.addGraph({
        generate: function() {   
            var width = $(plotDiv).width() - margin.right - margin.left,
                height = ($(plotDiv).height()*3.5) - margin.top - margin.bottom;

            maps = [];
            weaponClasses = []

            /*get all of the unique weapon and map keys in the dataset*/
            for (i = 0; i < test_data.length; i++) {
                for (j = 0; j < test_data[i]['values'].length; j++) {
                    weaponClasses.push(test_data[i]['values'][j]['y']);
                }
            }
            for (i = 0; i < test_data[0]['values'].length; i++) {
                maps.push(test_data[0]['values'][i]['x']);
            }
            maps = maps.unique();
            weaponClasses = weaponClasses.unique();

            //build a list from 0 to maps.length and 0 to weaponClasses.length
            mapsIndex = [];
            weaponsIndex = [];
            for (var i = 0; i < maps.length; i++) {
                mapsIndex.push(i);
            }
            for (var i = 0; i < weaponClasses.length; i++) {
                weaponsIndex.push(i);
            }

            //create a map that takes the map and weapon keys (strings) and outputs an integer
            var xs = d3.scale.ordinal()
                .domain(maps)
                .range(mapsIndex);
            ys = d3.scale.ordinal()
                .domain(weaponClasses)
                .range(weaponsIndex);

            //build the chart
            var chart = nv.models.scatterChart()
                .showDistX(true)    //showDist, when true, will display those little distribution lines on the axis.
                .showDistY(true)
                .width(width)
                .height(height)
                .x(function(d,i){return xs(d['x']);})   //use the interger value when defining the x and y axes
                .y(function(d,i){return ys(d['y']);})
                ;

            //format tool tip
            chart.tooltipContent(function(key,x,y,e,graph) {
                console.log(graph);
                return '<h4>' + key + '</h4></br><p>'+d3.format('.3%')(graph.point.size)+'</p>';
            });

            //go back and replace the integer values with the strings
            chart.xAxis.tickFormat(function(d){
                return(maps[d]);
            });
            chart.yAxis.tickFormat(function(d){
                return(weaponClasses[d]);
            });

            //rotate labels
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
                var width = $(plotDiv).width() - margin.right - margin.left,
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