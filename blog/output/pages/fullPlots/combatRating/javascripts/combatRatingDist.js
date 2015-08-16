

        data_combatRatingDist=[{"values": [{"y": 0.0486212884395128, "x": "(0,20.00)"}, {"y": 0.068011921329080405, "x": "[20.00, 40.00)"}, {"y": 0.11194103375657335, "x": "[40.00, 60.00)"}, {"y": 0.156695279498516, "x": "[60.00, 80.00)"}, {"y": 0.17592581189423515, "x": "[80.00, 100.00)"}, {"y": 0.15686769541496817, "x": "[100.00, 120.00)"}, {"y": 0.11646079385214103, "x": "[120.00, 140.00)"}, {"y": 0.075327282355694039, "x": "[140.00, 160.00)"}, {"y": 0.042506681116762521, "x": "[160.00, 180.00)"}, {"y": 0.023128363649798644, "x": "[180.00, 200.00)"}, {"y": 0.012333895737632238, "x": "[200.00, 220.00)"}, {"y": 0.012179952955085654, "x": "[220.00, Inf)"}], "key": "Distribution", "yAxis": "1"}];


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



