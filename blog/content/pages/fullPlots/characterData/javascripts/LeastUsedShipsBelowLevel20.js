

                data_LeastUsedShipsBelowLevel20=[{"values": [{"y": 2.835672763363108e-05, "x": "\"The Visible Hand\""}, {"y": 2.835672763363108e-05, "x": "\"The Teilhard War\""}, {"y": 5.671345526726216e-05, "x": "AFv1 Octavian"}, {"y": 0.0001417836381681554, "x": "NS66 High Water"}, {"y": 0.00022685382106904864, "x": "\"The Fermi Solution\""}, {"y": 0.0002552105487026797, "x": "EX21 Spindle Demon"}, {"y": 0.00034028073160357296, "x": "\"Chasing Infinity\""}, {"y": 0.00036863745923720404, "x": "AX19 Slipper Misfit"}, {"y": 0.00036863745923720404, "x": "NS22 Cloud Errant"}, {"y": 0.0004253509145044662, "x": "NS66 Cloud Errant"}], "key": "Most Used Ships", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_LeastUsedShipsBelowLevel20;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Ship');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.3%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#LeastUsedShipsBelowLevel20 svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


