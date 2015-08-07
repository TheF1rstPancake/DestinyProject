

                data_LeastUsedShipsAboveLevel20=[{"values": [{"y": 0.00014486568601732906, "x": "AFv1 Octavian"}, {"y": 0.00027798550560082067, "x": "NS66 High Water"}, {"y": 0.0004228511916181497, "x": "EX21 Spindle Demon"}, {"y": 0.0004620040797309414, "x": "Regulus Class 22a"}, {"y": 0.0005912086105031537, "x": "Regulus Class 44b"}, {"y": 0.0006538532314836204, "x": "NS22 Cloud Errant"}, {"y": 0.0006538532314836204, "x": "NS66 Cloud Errant"}, {"y": 0.0009435846035182786, "x": "NS22 High Water"}, {"y": 0.0009474998923295577, "x": "Phaeton Class v3.1"}, {"y": 0.001002313935687466, "x": "Regulus Class 66c"}], "key": "Most Used Ships", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_LeastUsedShipsAboveLevel20;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Ship');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.3%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#LeastUsedShipsAboveLevel20 svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


