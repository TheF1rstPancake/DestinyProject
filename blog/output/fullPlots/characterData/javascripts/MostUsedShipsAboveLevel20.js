

                data_MostUsedShipsAboveLevel20=[{"values": [{"y": 0.02070013194523294, "x": "\"Gloriole Jump\""}, {"y": 0.02074711541096829, "x": "\"Ketch Me If You Can\""}, {"y": 0.02411426378866837, "x": "\"Little Light\""}, {"y": 0.029442971860819313, "x": "Arcadia Class Jumpship"}, {"y": 0.0367371549162324, "x": "\"Bane of Dark Gods\""}, {"y": 0.04195623490166752, "x": "Ceres Galliot"}, {"y": 0.04450508791781026, "x": "\"Light in the Abyss\""}, {"y": 0.045930253045115874, "x": "\"Draught of Nectar\""}, {"y": 0.07915147860881958, "x": "\"Aspect of Glass\""}, {"y": 0.15787619073720974, "x": "Hildian Seeker"}], "key": "Most Used Ships", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_MostUsedShipsAboveLevel20;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Ship');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#MostUsedShipsAboveLevel20 svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


