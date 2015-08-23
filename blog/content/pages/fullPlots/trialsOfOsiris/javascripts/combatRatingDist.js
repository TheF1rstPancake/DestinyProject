

        data_combatRatingDist=[{"values": [{"y": 0.0, "x": "(0,30.00)"}, {"y": 0.00029831452294535872, "x": "[30.00, 60.00)"}, {"y": 0.0035797742753443046, "x": "[60.00, 90.00)"}, {"y": 0.12027047183413712, "x": "[90.00, 120.00)"}, {"y": 0.0041764033212350225, "x": "[120.00, 150.00)"}, {"y": 0.1120171033659822, "x": "[150.00, 180.00)"}, {"y": 0.0080047730323671261, "x": "[180.00, 210.00)"}, {"y": 0.098592949833441051, "x": "[210.00, 240.00)"}, {"y": 0.083229751901755078, "x": "[240.00, 270.00)"}, {"y": 0.0046735941928106196, "x": "[270.00, 300.00)"}, {"y": 0.0058668522845920553, "x": "[300.00, 330.00)"}, {"y": 0.083726942773330676, "x": "[330.00, 360.00)"}, {"y": 0.097896882613235217, "x": "[360.00, 390.00)"}, {"y": 0.008750559339730523, "x": "[390.00, 420.00)"}, {"y": 0.11097300253567345, "x": "[420.00, 450.00)"}, {"y": 0.0064634813304827723, "x": "[450.00, 480.00)"}, {"y": 0.1173370456918411, "x": "[480.00, 510.00)"}, {"y": 0.0030825834037687067, "x": "[510.00, 540.00)"}, {"y": 0.0031820215780838262, "x": "[540.00, 570.00)"}, {"y": 0.12787749216924377, "x": "[570.00, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_combatRatingDist;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Combat Rating');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#combatRatingDist svg')
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



