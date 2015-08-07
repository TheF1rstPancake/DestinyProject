

                data_MostUsedShipsBelowLevel20=[{"values": [{"y": 0.009102509570395576, "x": "Kestrel Class AX"}, {"y": 0.00915922302566284, "x": "Regulus Class 55"}, {"y": 0.012703813979866724, "x": "Regulus Class 77"}, {"y": 0.012845597618034879, "x": "Regulus Class 99"}, {"y": 0.013299305260172976, "x": "Phaeton Class v1"}, {"y": 0.014547001276052744, "x": "Phaeton Class v2"}, {"y": 0.017779668226286686, "x": "Kestrel Class EX"}, {"y": 0.021976463916064087, "x": "\"Aspect of Glass\""}, {"y": 0.02552105487026797, "x": "Valkyrie-O5X"}, {"y": 0.6493123493548845, "x": "Arcadia Class Jumpship"}], "key": "Most Used Ships", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_MostUsedShipsBelowLevel20;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Ship');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#MostUsedShipsBelowLevel20 svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


