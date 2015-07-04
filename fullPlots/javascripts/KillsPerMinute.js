

                data_KillsPerMinute=[{"values": [{"y": 18.504227077516017, "x": "Asylum"}, {"y": 11.119063657797238, "x": "Bastion"}, {"y": 14.674723192997355, "x": "Black Shield"}, {"y": 17.665189122077127, "x": "Blind Watch"}, {"y": 18.136910531510942, "x": "Firebase Delphi"}, {"y": 11.613985026549194, "x": "First Light"}, {"y": 15.354244099526236, "x": "Pantheon"}, {"y": 17.54350021513239, "x": "Rusted Lands"}, {"y": 16.727286365080051, "x": "Shores of Time"}, {"y": 13.529674003900809, "x": "Skyshock"}, {"y": 18.309516006112609, "x": "The Anomaly"}, {"y": 18.945200055645326, "x": "The Burning Shrine"}, {"y": 16.445414284267418, "x": "The Cauldron"}, {"y": 15.341141402550811, "x": "Thieves' Den"}, {"y": 17.513573875660313, "x": "Twilight Gap"}, {"y": 14.268308231054295, "x": "Widow's Court"}], "key": "Kills Per Minute", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 100, left: 60});

            var datum = data_KillsPerMinute;



                var width = $('#KillsPerMinute').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 100;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Map Name');
            chart.yAxis
                .axisLabel('Kills Per Minute')                .tickFormat(d3.format(',.3f'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#KillsPerMinute svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', (width + 60 + 60) )
            .attr('height', (height + 30 + 100))
            .call(chart);

    
        });


