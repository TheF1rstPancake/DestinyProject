

            data_quitRateByKillsPerMinute=[{"values": [{"y": 0.19779353821907009, "x": 11.119063657797238}, {"y": 0.16680161943319838, "x": 11.613985026549194}, {"y": 0.14900086880973062, "x": 13.529674003900809}, {"y": 0.11875392013380726, "x": 14.268308231054295}, {"y": 0.12606085696543157, "x": 14.674723192997355}, {"y": 0.11762225969645868, "x": 15.341141402550811}, {"y": 0.13957577755797346, "x": 15.354244099526236}, {"y": 0.12202493388741975, "x": 16.445414284267418}, {"y": 0.12350953895071537, "x": 16.727286365080051}, {"y": 0.11968185240963858, "x": 17.513573875660313}, {"y": 0.13381770145310434, "x": 17.54350021513239}, {"y": 0.12963232088359256, "x": 17.665189122077127}, {"y": 0.12938187976291282, "x": 18.136910531510942}, {"y": 0.12605107443164121, "x": 18.309516006112609}, {"y": 0.12400241432499493, "x": 18.504227077516017}, {"y": 0.11640318875827593, "x": 18.945200055645326}], "key": "Quit Rate", "yAxis": "1"}];


            nv.addGraph(function() {
            var chart = nv.models.lineChart();

            chart.margin({top: 30, right: 60, bottom: 100, left: 60});

            var datum = data_quitRateByKillsPerMinute;


            var xOrdinal = {18.945200055645326: 'The Burning Shrine', 16.727286365080051: 'Shores of Time', 18.309516006112609: 'The Anomaly', 11.119063657797238: 'Bastion', 18.136910531510942: 'Firebase Delphi', 14.268308231054295: "Widow's Court", 15.354244099526236: 'Pantheon', 17.513573875660313: 'Twilight Gap', 17.54350021513239: 'Rusted Lands', 16.445414284267418: 'The Cauldron', 17.665189122077127: 'Blind Watch', 15.341141402550811: "Thieves' Den", 13.529674003900809: 'Skyshock', 18.504227077516017: 'Asylum', 11.613985026549194: 'First Light', 14.674723192997355: 'Black Shield'};

                var width = $('#quitRateByKillsPerMinute').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 100;
                chart.height(height);




                chart.xAxis
                .rotateLabels(-25)                .axisLabel('Kills Per Minute')                .tickValues([11.119063657797238, 11.613985026549194, 13.529674003900809, 14.268308231054295, 14.674723192997355, 15.341141402550811, 15.354244099526236, 16.445414284267418, 16.727286365080051, 17.513573875660313, 17.54350021513239, 17.665189122077127, 18.136910531510942, 18.309516006112609, 18.504227077516017, 18.945200055645326])                .tickFormat(function(d){return xOrdinal[d];});
            chart.yAxis
                .axisLabel('Quit Rate')                .tickFormat(d3.format(',.3f'));



          chart.showLegend(true);


    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#quitRateByKillsPerMinute svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', (width + 60 + 60) )
            .attr('height', (height + 30 + 100))
            .call(chart);


        });


