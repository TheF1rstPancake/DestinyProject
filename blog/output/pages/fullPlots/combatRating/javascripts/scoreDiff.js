

        data_scoreDiff=[{"values": [{"y": 0.1917139815471966, "x": "(0,1416.67)"}, {"y": 0.14762242725337119, "x": "[1416.67, 2833.33)"}, {"y": 0.14300922640170333, "x": "[2833.33, 4250.00)"}, {"y": 0.12837118523775728, "x": "[4250.00, 5666.67)"}, {"y": 0.10938608942512421, "x": "[5666.67, 7083.33)"}, {"y": 0.09244144783534422, "x": "[7083.33, 8500.00)"}, {"y": 0.068754435770049679, "x": "[8500.00, 9916.67)"}, {"y": 0.044357700496806249, "x": "[9916.67, 11333.33)"}, {"y": 0.032913413768630231, "x": "[11333.33, 12750.00)"}, {"y": 0.020138396025550037, "x": "[12750.00, 14166.67)"}, {"y": 0.012331440738112136, "x": "[14166.67, 15583.33)"}, {"y": 0.008960255500354862, "x": "[15583.33, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_scoreDiff;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-15)                .axisLabel('Score Difference');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#scoreDiff svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);


    chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
     });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
    });

    });



