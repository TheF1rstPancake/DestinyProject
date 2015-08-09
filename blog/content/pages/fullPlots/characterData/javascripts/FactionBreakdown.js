

                data_FactionBreakdown=[{"values": [{"y": 0.18757757165957348, "x": "Dead Orbit"}, {"y": 0.084613306500554014, "x": "Future War Cult"}, {"y": 0.089468264626540173, "x": "New Monarchy"}], "key": "Distribution", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_FactionBreakdown;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Faction');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#FactionBreakdown svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


