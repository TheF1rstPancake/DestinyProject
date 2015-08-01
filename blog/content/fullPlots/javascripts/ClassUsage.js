

                data_ClassUsage=[{"values": [{"y": 0.3150746997593367, "x": "Warlock"}, {"y": 0.28147010538579675, "x": "Titan"}, {"y": 0.40345519485486653, "x": "Hunter"}], "key": "Serie 1", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_ClassUsage;



                var width = $('#ClassUsage').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .axisLabel('Class');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#ClassUsage svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#ClassUsage').width())
            .attr('height', 450)
            .call(chart);

    
        });


