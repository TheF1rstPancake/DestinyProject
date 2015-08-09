

                data_LeastUsedShips=[{"values": [{"y": 0.00013417092688028514, "x": "AFv1 Octavian"}, {"y": 0.0002614612934077351, "x": "NS66 High Water"}, {"y": 0.0004025127806408554, "x": "EX21 Spindle Demon"}, {"y": 0.0006192504317551621, "x": "NS22 Cloud Errant"}, {"y": 0.0006192504317551621, "x": "Regulus Class 22a"}, {"y": 0.0006261309921079972, "x": "NS66 Cloud Errant"}, {"y": 0.0006605337938721729, "x": "Regulus Class 44b"}, {"y": 0.0009151145269270729, "x": "NS22 High Water"}, {"y": 0.000987360410631842, "x": "LRv3 Javelin"}, {"y": 0.000987360410631842, "x": "Phaeton Class v3.1"}], "key": "Most Used Ships", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_LeastUsedShips;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Ship');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',s'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#LeastUsedShips svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


