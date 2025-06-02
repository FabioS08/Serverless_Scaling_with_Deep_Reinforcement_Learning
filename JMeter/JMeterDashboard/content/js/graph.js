/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 23.0, "minX": 0.0, "maxY": 232.0, "series": [{"data": [[0.0, 23.0], [0.1, 23.0], [0.2, 23.0], [0.3, 23.0], [0.4, 23.0], [0.5, 23.0], [0.6, 23.0], [0.7, 23.0], [0.8, 23.0], [0.9, 23.0], [1.0, 23.0], [1.1, 23.0], [1.2, 23.0], [1.3, 23.0], [1.4, 25.0], [1.5, 25.0], [1.6, 25.0], [1.7, 25.0], [1.8, 25.0], [1.9, 25.0], [2.0, 25.0], [2.1, 25.0], [2.2, 25.0], [2.3, 25.0], [2.4, 25.0], [2.5, 25.0], [2.6, 25.0], [2.7, 25.0], [2.8, 25.0], [2.9, 25.0], [3.0, 25.0], [3.1, 25.0], [3.2, 25.0], [3.3, 25.0], [3.4, 25.0], [3.5, 25.0], [3.6, 25.0], [3.7, 25.0], [3.8, 25.0], [3.9, 25.0], [4.0, 26.0], [4.1, 26.0], [4.2, 26.0], [4.3, 26.0], [4.4, 26.0], [4.5, 26.0], [4.6, 26.0], [4.7, 26.0], [4.8, 26.0], [4.9, 26.0], [5.0, 26.0], [5.1, 26.0], [5.2, 26.0], [5.3, 26.0], [5.4, 26.0], [5.5, 26.0], [5.6, 26.0], [5.7, 26.0], [5.8, 26.0], [5.9, 26.0], [6.0, 26.0], [6.1, 26.0], [6.2, 26.0], [6.3, 26.0], [6.4, 26.0], [6.5, 26.0], [6.6, 26.0], [6.7, 26.0], [6.8, 26.0], [6.9, 26.0], [7.0, 26.0], [7.1, 26.0], [7.2, 26.0], [7.3, 26.0], [7.4, 26.0], [7.5, 26.0], [7.6, 26.0], [7.7, 26.0], [7.8, 26.0], [7.9, 27.0], [8.0, 27.0], [8.1, 27.0], [8.2, 27.0], [8.3, 27.0], [8.4, 27.0], [8.5, 27.0], [8.6, 27.0], [8.7, 27.0], [8.8, 27.0], [8.9, 27.0], [9.0, 27.0], [9.1, 27.0], [9.2, 27.0], [9.3, 27.0], [9.4, 27.0], [9.5, 27.0], [9.6, 27.0], [9.7, 27.0], [9.8, 27.0], [9.9, 27.0], [10.0, 27.0], [10.1, 27.0], [10.2, 27.0], [10.3, 27.0], [10.4, 27.0], [10.5, 27.0], [10.6, 35.0], [10.7, 35.0], [10.8, 35.0], [10.9, 35.0], [11.0, 35.0], [11.1, 35.0], [11.2, 35.0], [11.3, 35.0], [11.4, 35.0], [11.5, 35.0], [11.6, 35.0], [11.7, 35.0], [11.8, 35.0], [11.9, 39.0], [12.0, 39.0], [12.1, 39.0], [12.2, 39.0], [12.3, 39.0], [12.4, 39.0], [12.5, 39.0], [12.6, 39.0], [12.7, 39.0], [12.8, 39.0], [12.9, 39.0], [13.0, 39.0], [13.1, 39.0], [13.2, 48.0], [13.3, 48.0], [13.4, 48.0], [13.5, 48.0], [13.6, 48.0], [13.7, 48.0], [13.8, 48.0], [13.9, 48.0], [14.0, 48.0], [14.1, 48.0], [14.2, 48.0], [14.3, 48.0], [14.4, 48.0], [14.5, 48.0], [14.6, 48.0], [14.7, 48.0], [14.8, 48.0], [14.9, 48.0], [15.0, 48.0], [15.1, 48.0], [15.2, 48.0], [15.3, 48.0], [15.4, 48.0], [15.5, 48.0], [15.6, 48.0], [15.7, 48.0], [15.8, 48.0], [15.9, 48.0], [16.0, 48.0], [16.1, 48.0], [16.2, 48.0], [16.3, 48.0], [16.4, 48.0], [16.5, 48.0], [16.6, 48.0], [16.7, 48.0], [16.8, 48.0], [16.9, 48.0], [17.0, 48.0], [17.1, 48.0], [17.2, 48.0], [17.3, 48.0], [17.4, 48.0], [17.5, 48.0], [17.6, 48.0], [17.7, 48.0], [17.8, 48.0], [17.9, 48.0], [18.0, 48.0], [18.1, 48.0], [18.2, 48.0], [18.3, 48.0], [18.4, 48.0], [18.5, 49.0], [18.6, 49.0], [18.7, 49.0], [18.8, 49.0], [18.9, 49.0], [19.0, 49.0], [19.1, 49.0], [19.2, 49.0], [19.3, 49.0], [19.4, 49.0], [19.5, 49.0], [19.6, 49.0], [19.7, 49.0], [19.8, 49.0], [19.9, 49.0], [20.0, 49.0], [20.1, 49.0], [20.2, 49.0], [20.3, 49.0], [20.4, 49.0], [20.5, 49.0], [20.6, 49.0], [20.7, 49.0], [20.8, 49.0], [20.9, 49.0], [21.0, 49.0], [21.1, 49.0], [21.2, 49.0], [21.3, 49.0], [21.4, 49.0], [21.5, 49.0], [21.6, 49.0], [21.7, 49.0], [21.8, 49.0], [21.9, 49.0], [22.0, 49.0], [22.1, 49.0], [22.2, 49.0], [22.3, 49.0], [22.4, 50.0], [22.5, 50.0], [22.6, 50.0], [22.7, 50.0], [22.8, 50.0], [22.9, 50.0], [23.0, 50.0], [23.1, 50.0], [23.2, 50.0], [23.3, 50.0], [23.4, 50.0], [23.5, 50.0], [23.6, 50.0], [23.7, 50.0], [23.8, 50.0], [23.9, 50.0], [24.0, 50.0], [24.1, 50.0], [24.2, 50.0], [24.3, 50.0], [24.4, 50.0], [24.5, 50.0], [24.6, 50.0], [24.7, 50.0], [24.8, 50.0], [24.9, 50.0], [25.0, 50.0], [25.1, 50.0], [25.2, 50.0], [25.3, 50.0], [25.4, 50.0], [25.5, 50.0], [25.6, 50.0], [25.7, 50.0], [25.8, 50.0], [25.9, 50.0], [26.0, 50.0], [26.1, 50.0], [26.2, 50.0], [26.3, 50.0], [26.4, 50.0], [26.5, 50.0], [26.6, 50.0], [26.7, 50.0], [26.8, 50.0], [26.9, 50.0], [27.0, 50.0], [27.1, 50.0], [27.2, 50.0], [27.3, 50.0], [27.4, 50.0], [27.5, 50.0], [27.6, 50.0], [27.7, 50.0], [27.8, 50.0], [27.9, 50.0], [28.0, 50.0], [28.1, 50.0], [28.2, 50.0], [28.3, 50.0], [28.4, 50.0], [28.5, 50.0], [28.6, 50.0], [28.7, 50.0], [28.8, 50.0], [28.9, 50.0], [29.0, 51.0], [29.1, 51.0], [29.2, 51.0], [29.3, 51.0], [29.4, 51.0], [29.5, 51.0], [29.6, 51.0], [29.7, 51.0], [29.8, 51.0], [29.9, 51.0], [30.0, 51.0], [30.1, 51.0], [30.2, 51.0], [30.3, 51.0], [30.4, 51.0], [30.5, 51.0], [30.6, 51.0], [30.7, 51.0], [30.8, 51.0], [30.9, 51.0], [31.0, 51.0], [31.1, 51.0], [31.2, 51.0], [31.3, 51.0], [31.4, 51.0], [31.5, 51.0], [31.6, 51.0], [31.7, 51.0], [31.8, 51.0], [31.9, 51.0], [32.0, 51.0], [32.1, 51.0], [32.2, 51.0], [32.3, 51.0], [32.4, 51.0], [32.5, 51.0], [32.6, 51.0], [32.7, 51.0], [32.8, 51.0], [32.9, 51.0], [33.0, 51.0], [33.1, 51.0], [33.2, 51.0], [33.3, 51.0], [33.4, 51.0], [33.5, 51.0], [33.6, 51.0], [33.7, 51.0], [33.8, 51.0], [33.9, 51.0], [34.0, 51.0], [34.1, 51.0], [34.2, 51.0], [34.3, 52.0], [34.4, 52.0], [34.5, 52.0], [34.6, 52.0], [34.7, 52.0], [34.8, 52.0], [34.9, 52.0], [35.0, 52.0], [35.1, 52.0], [35.2, 52.0], [35.3, 52.0], [35.4, 52.0], [35.5, 52.0], [35.6, 52.0], [35.7, 52.0], [35.8, 52.0], [35.9, 52.0], [36.0, 52.0], [36.1, 52.0], [36.2, 52.0], [36.3, 52.0], [36.4, 52.0], [36.5, 52.0], [36.6, 52.0], [36.7, 52.0], [36.8, 52.0], [36.9, 52.0], [37.0, 52.0], [37.1, 52.0], [37.2, 52.0], [37.3, 52.0], [37.4, 52.0], [37.5, 52.0], [37.6, 52.0], [37.7, 52.0], [37.8, 52.0], [37.9, 52.0], [38.0, 52.0], [38.1, 52.0], [38.2, 52.0], [38.3, 52.0], [38.4, 52.0], [38.5, 52.0], [38.6, 52.0], [38.7, 52.0], [38.8, 52.0], [38.9, 52.0], [39.0, 52.0], [39.1, 52.0], [39.2, 52.0], [39.3, 52.0], [39.4, 52.0], [39.5, 53.0], [39.6, 53.0], [39.7, 53.0], [39.8, 53.0], [39.9, 53.0], [40.0, 53.0], [40.1, 53.0], [40.2, 53.0], [40.3, 53.0], [40.4, 53.0], [40.5, 53.0], [40.6, 53.0], [40.7, 53.0], [40.8, 53.0], [40.9, 53.0], [41.0, 53.0], [41.1, 53.0], [41.2, 53.0], [41.3, 53.0], [41.4, 53.0], [41.5, 53.0], [41.6, 53.0], [41.7, 53.0], [41.8, 53.0], [41.9, 53.0], [42.0, 53.0], [42.1, 53.0], [42.2, 53.0], [42.3, 53.0], [42.4, 53.0], [42.5, 53.0], [42.6, 53.0], [42.7, 53.0], [42.8, 53.0], [42.9, 53.0], [43.0, 53.0], [43.1, 53.0], [43.2, 53.0], [43.3, 53.0], [43.4, 53.0], [43.5, 53.0], [43.6, 53.0], [43.7, 53.0], [43.8, 53.0], [43.9, 53.0], [44.0, 53.0], [44.1, 53.0], [44.2, 53.0], [44.3, 53.0], [44.4, 53.0], [44.5, 53.0], [44.6, 53.0], [44.7, 53.0], [44.8, 54.0], [44.9, 54.0], [45.0, 54.0], [45.1, 54.0], [45.2, 54.0], [45.3, 54.0], [45.4, 54.0], [45.5, 54.0], [45.6, 54.0], [45.7, 54.0], [45.8, 54.0], [45.9, 54.0], [46.0, 54.0], [46.1, 54.0], [46.2, 54.0], [46.3, 54.0], [46.4, 54.0], [46.5, 54.0], [46.6, 54.0], [46.7, 54.0], [46.8, 54.0], [46.9, 54.0], [47.0, 54.0], [47.1, 54.0], [47.2, 54.0], [47.3, 54.0], [47.4, 55.0], [47.5, 55.0], [47.6, 55.0], [47.7, 55.0], [47.8, 55.0], [47.9, 55.0], [48.0, 55.0], [48.1, 55.0], [48.2, 55.0], [48.3, 55.0], [48.4, 55.0], [48.5, 55.0], [48.6, 55.0], [48.7, 55.0], [48.8, 55.0], [48.9, 55.0], [49.0, 55.0], [49.1, 55.0], [49.2, 55.0], [49.3, 55.0], [49.4, 55.0], [49.5, 55.0], [49.6, 55.0], [49.7, 55.0], [49.8, 55.0], [49.9, 55.0], [50.0, 55.0], [50.1, 55.0], [50.2, 55.0], [50.3, 55.0], [50.4, 55.0], [50.5, 55.0], [50.6, 55.0], [50.7, 55.0], [50.8, 55.0], [50.9, 55.0], [51.0, 55.0], [51.1, 55.0], [51.2, 55.0], [51.3, 55.0], [51.4, 56.0], [51.5, 56.0], [51.6, 56.0], [51.7, 56.0], [51.8, 56.0], [51.9, 56.0], [52.0, 56.0], [52.1, 56.0], [52.2, 56.0], [52.3, 56.0], [52.4, 56.0], [52.5, 56.0], [52.6, 56.0], [52.7, 56.0], [52.8, 56.0], [52.9, 56.0], [53.0, 56.0], [53.1, 56.0], [53.2, 56.0], [53.3, 56.0], [53.4, 56.0], [53.5, 56.0], [53.6, 56.0], [53.7, 56.0], [53.8, 56.0], [53.9, 56.0], [54.0, 56.0], [54.1, 56.0], [54.2, 56.0], [54.3, 56.0], [54.4, 56.0], [54.5, 56.0], [54.6, 56.0], [54.7, 56.0], [54.8, 56.0], [54.9, 56.0], [55.0, 56.0], [55.1, 56.0], [55.2, 56.0], [55.3, 57.0], [55.4, 57.0], [55.5, 57.0], [55.6, 57.0], [55.7, 57.0], [55.8, 57.0], [55.9, 57.0], [56.0, 57.0], [56.1, 57.0], [56.2, 57.0], [56.3, 57.0], [56.4, 57.0], [56.5, 57.0], [56.6, 57.0], [56.7, 57.0], [56.8, 57.0], [56.9, 57.0], [57.0, 57.0], [57.1, 57.0], [57.2, 57.0], [57.3, 57.0], [57.4, 57.0], [57.5, 57.0], [57.6, 57.0], [57.7, 57.0], [57.8, 57.0], [57.9, 57.0], [58.0, 57.0], [58.1, 57.0], [58.2, 57.0], [58.3, 57.0], [58.4, 57.0], [58.5, 57.0], [58.6, 57.0], [58.7, 57.0], [58.8, 57.0], [58.9, 57.0], [59.0, 57.0], [59.1, 57.0], [59.2, 57.0], [59.3, 57.0], [59.4, 57.0], [59.5, 57.0], [59.6, 57.0], [59.7, 57.0], [59.8, 57.0], [59.9, 57.0], [60.0, 57.0], [60.1, 57.0], [60.2, 57.0], [60.3, 57.0], [60.4, 57.0], [60.5, 57.0], [60.6, 58.0], [60.7, 58.0], [60.8, 58.0], [60.9, 58.0], [61.0, 58.0], [61.1, 58.0], [61.2, 58.0], [61.3, 58.0], [61.4, 58.0], [61.5, 58.0], [61.6, 58.0], [61.7, 58.0], [61.8, 58.0], [61.9, 58.0], [62.0, 58.0], [62.1, 58.0], [62.2, 58.0], [62.3, 58.0], [62.4, 58.0], [62.5, 58.0], [62.6, 58.0], [62.7, 58.0], [62.8, 58.0], [62.9, 58.0], [63.0, 58.0], [63.1, 58.0], [63.2, 58.0], [63.3, 58.0], [63.4, 58.0], [63.5, 58.0], [63.6, 58.0], [63.7, 58.0], [63.8, 58.0], [63.9, 58.0], [64.0, 58.0], [64.1, 58.0], [64.2, 58.0], [64.3, 58.0], [64.4, 58.0], [64.5, 59.0], [64.6, 59.0], [64.7, 59.0], [64.8, 59.0], [64.9, 59.0], [65.0, 59.0], [65.1, 59.0], [65.2, 59.0], [65.3, 59.0], [65.4, 59.0], [65.5, 59.0], [65.6, 59.0], [65.7, 59.0], [65.8, 59.0], [65.9, 59.0], [66.0, 59.0], [66.1, 59.0], [66.2, 59.0], [66.3, 59.0], [66.4, 59.0], [66.5, 59.0], [66.6, 59.0], [66.7, 59.0], [66.8, 59.0], [66.9, 59.0], [67.0, 59.0], [67.1, 59.0], [67.2, 60.0], [67.3, 60.0], [67.4, 60.0], [67.5, 60.0], [67.6, 60.0], [67.7, 60.0], [67.8, 60.0], [67.9, 60.0], [68.0, 60.0], [68.1, 60.0], [68.2, 60.0], [68.3, 60.0], [68.4, 60.0], [68.5, 60.0], [68.6, 60.0], [68.7, 60.0], [68.8, 60.0], [68.9, 60.0], [69.0, 60.0], [69.1, 60.0], [69.2, 60.0], [69.3, 60.0], [69.4, 60.0], [69.5, 60.0], [69.6, 60.0], [69.7, 60.0], [69.8, 61.0], [69.9, 61.0], [70.0, 61.0], [70.1, 61.0], [70.2, 61.0], [70.3, 61.0], [70.4, 61.0], [70.5, 61.0], [70.6, 61.0], [70.7, 61.0], [70.8, 61.0], [70.9, 61.0], [71.0, 61.0], [71.1, 61.0], [71.2, 61.0], [71.3, 61.0], [71.4, 61.0], [71.5, 61.0], [71.6, 61.0], [71.7, 61.0], [71.8, 61.0], [71.9, 61.0], [72.0, 61.0], [72.1, 61.0], [72.2, 61.0], [72.3, 61.0], [72.4, 61.0], [72.5, 61.0], [72.6, 61.0], [72.7, 61.0], [72.8, 61.0], [72.9, 61.0], [73.0, 61.0], [73.1, 61.0], [73.2, 61.0], [73.3, 61.0], [73.4, 61.0], [73.5, 61.0], [73.6, 61.0], [73.7, 61.0], [73.8, 61.0], [73.9, 61.0], [74.0, 61.0], [74.1, 61.0], [74.2, 61.0], [74.3, 61.0], [74.4, 61.0], [74.5, 61.0], [74.6, 61.0], [74.7, 61.0], [74.8, 61.0], [74.9, 61.0], [75.0, 62.0], [75.1, 62.0], [75.2, 62.0], [75.3, 62.0], [75.4, 62.0], [75.5, 62.0], [75.6, 62.0], [75.7, 62.0], [75.8, 62.0], [75.9, 62.0], [76.0, 62.0], [76.1, 62.0], [76.2, 62.0], [76.3, 62.0], [76.4, 64.0], [76.5, 64.0], [76.6, 64.0], [76.7, 64.0], [76.8, 64.0], [76.9, 64.0], [77.0, 64.0], [77.1, 64.0], [77.2, 64.0], [77.3, 64.0], [77.4, 64.0], [77.5, 64.0], [77.6, 64.0], [77.7, 64.0], [77.8, 64.0], [77.9, 64.0], [78.0, 64.0], [78.1, 64.0], [78.2, 64.0], [78.3, 64.0], [78.4, 64.0], [78.5, 64.0], [78.6, 64.0], [78.7, 64.0], [78.8, 64.0], [78.9, 64.0], [79.0, 65.0], [79.1, 65.0], [79.2, 65.0], [79.3, 65.0], [79.4, 65.0], [79.5, 65.0], [79.6, 65.0], [79.7, 65.0], [79.8, 65.0], [79.9, 65.0], [80.0, 65.0], [80.1, 65.0], [80.2, 65.0], [80.3, 66.0], [80.4, 66.0], [80.5, 66.0], [80.6, 66.0], [80.7, 66.0], [80.8, 66.0], [80.9, 66.0], [81.0, 66.0], [81.1, 66.0], [81.2, 66.0], [81.3, 66.0], [81.4, 66.0], [81.5, 66.0], [81.6, 67.0], [81.7, 67.0], [81.8, 67.0], [81.9, 67.0], [82.0, 67.0], [82.1, 67.0], [82.2, 67.0], [82.3, 67.0], [82.4, 67.0], [82.5, 67.0], [82.6, 67.0], [82.7, 67.0], [82.8, 67.0], [82.9, 73.0], [83.0, 73.0], [83.1, 73.0], [83.2, 73.0], [83.3, 73.0], [83.4, 73.0], [83.5, 73.0], [83.6, 73.0], [83.7, 73.0], [83.8, 73.0], [83.9, 73.0], [84.0, 73.0], [84.1, 73.0], [84.2, 73.0], [84.3, 81.0], [84.4, 81.0], [84.5, 81.0], [84.6, 81.0], [84.7, 81.0], [84.8, 81.0], [84.9, 81.0], [85.0, 81.0], [85.1, 81.0], [85.2, 81.0], [85.3, 81.0], [85.4, 81.0], [85.5, 81.0], [85.6, 86.0], [85.7, 86.0], [85.8, 86.0], [85.9, 86.0], [86.0, 86.0], [86.1, 86.0], [86.2, 86.0], [86.3, 86.0], [86.4, 86.0], [86.5, 86.0], [86.6, 86.0], [86.7, 86.0], [86.8, 86.0], [86.9, 87.0], [87.0, 87.0], [87.1, 87.0], [87.2, 87.0], [87.3, 87.0], [87.4, 87.0], [87.5, 87.0], [87.6, 87.0], [87.7, 87.0], [87.8, 87.0], [87.9, 87.0], [88.0, 87.0], [88.1, 87.0], [88.2, 91.0], [88.3, 91.0], [88.4, 91.0], [88.5, 91.0], [88.6, 91.0], [88.7, 91.0], [88.8, 91.0], [88.9, 91.0], [89.0, 91.0], [89.1, 91.0], [89.2, 91.0], [89.3, 91.0], [89.4, 91.0], [89.5, 96.0], [89.6, 96.0], [89.7, 96.0], [89.8, 96.0], [89.9, 96.0], [90.0, 96.0], [90.1, 96.0], [90.2, 96.0], [90.3, 96.0], [90.4, 96.0], [90.5, 96.0], [90.6, 96.0], [90.7, 96.0], [90.8, 100.0], [90.9, 100.0], [91.0, 100.0], [91.1, 100.0], [91.2, 100.0], [91.3, 100.0], [91.4, 100.0], [91.5, 100.0], [91.6, 100.0], [91.7, 100.0], [91.8, 100.0], [91.9, 100.0], [92.0, 100.0], [92.1, 100.0], [92.2, 100.0], [92.3, 100.0], [92.4, 100.0], [92.5, 100.0], [92.6, 100.0], [92.7, 100.0], [92.8, 100.0], [92.9, 100.0], [93.0, 100.0], [93.1, 100.0], [93.2, 100.0], [93.3, 100.0], [93.4, 100.0], [93.5, 121.0], [93.6, 121.0], [93.7, 121.0], [93.8, 121.0], [93.9, 121.0], [94.0, 121.0], [94.1, 121.0], [94.2, 121.0], [94.3, 121.0], [94.4, 121.0], [94.5, 121.0], [94.6, 121.0], [94.7, 121.0], [94.8, 122.0], [94.9, 122.0], [95.0, 122.0], [95.1, 122.0], [95.2, 122.0], [95.3, 122.0], [95.4, 122.0], [95.5, 122.0], [95.6, 122.0], [95.7, 122.0], [95.8, 122.0], [95.9, 122.0], [96.0, 122.0], [96.1, 127.0], [96.2, 127.0], [96.3, 127.0], [96.4, 127.0], [96.5, 127.0], [96.6, 127.0], [96.7, 127.0], [96.8, 127.0], [96.9, 127.0], [97.0, 127.0], [97.1, 127.0], [97.2, 127.0], [97.3, 127.0], [97.4, 165.0], [97.5, 165.0], [97.6, 165.0], [97.7, 165.0], [97.8, 165.0], [97.9, 165.0], [98.0, 165.0], [98.1, 165.0], [98.2, 165.0], [98.3, 165.0], [98.4, 165.0], [98.5, 165.0], [98.6, 165.0], [98.7, 232.0], [98.8, 232.0], [98.9, 232.0], [99.0, 232.0], [99.1, 232.0], [99.2, 232.0], [99.3, 232.0], [99.4, 232.0], [99.5, 232.0], [99.6, 232.0], [99.7, 232.0], [99.8, 232.0], [99.9, 232.0]], "isOverall": false, "label": "Matrix Multiply - HTTP Request", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 0.0, "maxY": 69.0, "series": [{"data": [[0.0, 69.0], [100.0, 6.0], [200.0, 1.0]], "isOverall": false, "label": "Matrix Multiply - HTTP Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 200.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 76.0, "minX": 0.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1.500ms"], [2, "Requests having \nresponse time > 1.500ms"], [3, "Requests in error"]], "maxY": 76.0, "series": [{"data": [[0.0, 76.0]], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1.500ms", "isController": false}, {"data": [], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1.500ms", "isController": false}, {"data": [], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 4.9E-324, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 49.0, "minX": 1.74746562E12, "maxY": 50.0, "series": [{"data": [[1.7474673E12, 50.0], [1.74746634E12, 50.0], [1.747467E12, 50.0], [1.74746592E12, 50.0], [1.74746562E12, 50.0], [1.74746688E12, 50.0], [1.74746628E12, 50.0], [1.74746598E12, 50.0], [1.74746724E12, 50.0], [1.74746586E12, 50.0], [1.74746622E12, 50.0], [1.74746748E12, 49.0], [1.7474664E12, 50.0]], "isOverall": false, "label": "Concurrency Thread Group-ThreadStarter", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.74746748E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 60.7837837837838, "minX": 48.0, "maxY": 127.0, "series": [{"data": [[49.0, 61.0], [48.0, 127.0], [50.0, 60.7837837837838]], "isOverall": false, "label": "Matrix Multiply - HTTP Request", "isController": false}, {"data": [[49.96052631578947, 61.65789473684212]], "isOverall": false, "label": "Matrix Multiply - HTTP Request-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 50.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 9.716666666666667, "minX": 1.74746562E12, "maxY": 104355.56666666667, "series": [{"data": [[1.7474673E12, 19.416666666666668], [1.74746634E12, 165.06666666666666], [1.747467E12, 9.716666666666667], [1.74746592E12, 77.73333333333333], [1.74746562E12, 194.23333333333332], [1.74746688E12, 9.716666666666667], [1.74746628E12, 19.433333333333334], [1.74746598E12, 106.86666666666666], [1.74746724E12, 19.433333333333334], [1.74746586E12, 29.15], [1.74746622E12, 48.56666666666667], [1.74746748E12, 29.133333333333333], [1.7474664E12, 9.716666666666667]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.7474673E12, 10434.383333333333], [1.74746634E12, 88692.8], [1.747467E12, 5218.716666666666], [1.74746592E12, 41748.75], [1.74746562E12, 104355.56666666667], [1.74746688E12, 5215.666666666667], [1.74746628E12, 10437.95], [1.74746598E12, 57399.833333333336], [1.74746724E12, 10434.9], [1.74746586E12, 15653.616666666667], [1.74746622E12, 26088.516666666666], [1.74746748E12, 15650.05], [1.7474664E12, 5219.233333333334]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.74746748E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 45.54545454545455, "minX": 1.74746562E12, "maxY": 91.33333333333333, "series": [{"data": [[1.7474673E12, 63.0], [1.74746634E12, 47.29411764705882], [1.747467E12, 50.0], [1.74746592E12, 63.0], [1.74746562E12, 76.19999999999999], [1.74746688E12, 48.0], [1.74746628E12, 53.5], [1.74746598E12, 45.54545454545455], [1.74746724E12, 89.0], [1.74746586E12, 58.333333333333336], [1.74746622E12, 68.2], [1.74746748E12, 91.33333333333333], [1.7474664E12, 54.0]], "isOverall": false, "label": "Matrix Multiply - HTTP Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.74746748E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 45.54545454545455, "minX": 1.74746562E12, "maxY": 91.0, "series": [{"data": [[1.7474673E12, 62.5], [1.74746634E12, 47.235294117647065], [1.747467E12, 50.0], [1.74746592E12, 63.0], [1.74746562E12, 76.0], [1.74746688E12, 47.0], [1.74746628E12, 53.0], [1.74746598E12, 45.54545454545455], [1.74746724E12, 89.0], [1.74746586E12, 58.0], [1.74746622E12, 68.2], [1.74746748E12, 91.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "Matrix Multiply - HTTP Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.74746748E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 1.2727272727272727, "minX": 1.74746562E12, "maxY": 25.5, "series": [{"data": [[1.7474673E12, 25.5], [1.74746634E12, 5.470588235294118], [1.747467E12, 5.0], [1.74746592E12, 9.25], [1.74746562E12, 13.700000000000001], [1.74746688E12, 12.0], [1.74746628E12, 6.0], [1.74746598E12, 1.2727272727272727], [1.74746724E12, 6.5], [1.74746586E12, 19.666666666666664], [1.74746622E12, 9.6], [1.74746748E12, 24.0], [1.7474664E12, 6.0]], "isOverall": false, "label": "Matrix Multiply - HTTP Request", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.74746748E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 23.0, "minX": 1.74746562E12, "maxY": 232.0, "series": [{"data": [[1.7474673E12, 87.0], [1.74746634E12, 59.0], [1.747467E12, 50.0], [1.74746592E12, 100.0], [1.74746562E12, 232.0], [1.74746688E12, 48.0], [1.74746628E12, 54.0], [1.74746598E12, 56.0], [1.74746724E12, 121.0], [1.74746586E12, 60.0], [1.74746622E12, 100.0], [1.74746748E12, 127.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.7474673E12, 39.0], [1.74746634E12, 26.0], [1.747467E12, 50.0], [1.74746592E12, 25.0], [1.74746562E12, 26.0], [1.74746688E12, 48.0], [1.74746628E12, 53.0], [1.74746598E12, 23.0], [1.74746724E12, 57.0], [1.74746586E12, 56.0], [1.74746622E12, 50.0], [1.74746748E12, 61.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.7474673E12, 87.0], [1.74746634E12, 55.8], [1.747467E12, 50.0], [1.74746592E12, 100.0], [1.74746562E12, 160.7000000000001], [1.74746688E12, 48.0], [1.74746628E12, 54.0], [1.74746598E12, 55.400000000000006], [1.74746724E12, 121.0], [1.74746586E12, 60.0], [1.74746622E12, 100.0], [1.74746748E12, 127.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.7474673E12, 87.0], [1.74746634E12, 59.0], [1.747467E12, 50.0], [1.74746592E12, 100.0], [1.74746562E12, 232.0], [1.74746688E12, 48.0], [1.74746628E12, 54.0], [1.74746598E12, 56.0], [1.74746724E12, 121.0], [1.74746586E12, 60.0], [1.74746622E12, 100.0], [1.74746748E12, 127.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.7474673E12, 63.0], [1.74746634E12, 52.0], [1.747467E12, 50.0], [1.74746592E12, 54.5], [1.74746562E12, 61.0], [1.74746688E12, 48.0], [1.74746628E12, 53.5], [1.74746598E12, 49.0], [1.74746724E12, 89.0], [1.74746586E12, 59.0], [1.74746622E12, 66.0], [1.74746748E12, 86.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "Median", "isController": false}, {"data": [[1.7474673E12, 87.0], [1.74746634E12, 59.0], [1.747467E12, 50.0], [1.74746592E12, 100.0], [1.74746562E12, 228.64999999999995], [1.74746688E12, 48.0], [1.74746628E12, 54.0], [1.74746598E12, 56.0], [1.74746724E12, 121.0], [1.74746586E12, 60.0], [1.74746622E12, 100.0], [1.74746748E12, 127.0], [1.7474664E12, 54.0]], "isOverall": false, "label": "95th percentile", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.74746748E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 55.0, "minX": 1.0, "maxY": 76.5, "series": [{"data": [[1.0, 55.0], [2.0, 76.5]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 2.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 54.5, "minX": 1.0, "maxY": 76.5, "series": [{"data": [[1.0, 54.5], [2.0, 76.5]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 2.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.74746562E12, "maxY": 0.3333333333333333, "series": [{"data": [[1.7474673E12, 0.03333333333333333], [1.74746634E12, 0.2833333333333333], [1.747467E12, 0.016666666666666666], [1.74746592E12, 0.11666666666666667], [1.74746562E12, 0.3333333333333333], [1.74746688E12, 0.016666666666666666], [1.74746628E12, 0.03333333333333333], [1.74746598E12, 0.18333333333333332], [1.74746724E12, 0.03333333333333333], [1.74746586E12, 0.06666666666666667], [1.74746622E12, 0.08333333333333333], [1.74746748E12, 0.05], [1.7474664E12, 0.016666666666666666]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.74746748E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.74746562E12, "maxY": 0.3333333333333333, "series": [{"data": [[1.7474673E12, 0.03333333333333333], [1.74746634E12, 0.2833333333333333], [1.747467E12, 0.016666666666666666], [1.74746592E12, 0.13333333333333333], [1.74746562E12, 0.3333333333333333], [1.74746688E12, 0.016666666666666666], [1.74746628E12, 0.03333333333333333], [1.74746598E12, 0.18333333333333332], [1.74746724E12, 0.03333333333333333], [1.74746586E12, 0.05], [1.74746622E12, 0.08333333333333333], [1.74746748E12, 0.05], [1.7474664E12, 0.016666666666666666]], "isOverall": false, "label": "200", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.74746748E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.74746562E12, "maxY": 0.3333333333333333, "series": [{"data": [[1.7474673E12, 0.03333333333333333], [1.74746634E12, 0.2833333333333333], [1.747467E12, 0.016666666666666666], [1.74746592E12, 0.13333333333333333], [1.74746562E12, 0.3333333333333333], [1.74746688E12, 0.016666666666666666], [1.74746628E12, 0.03333333333333333], [1.74746598E12, 0.18333333333333332], [1.74746724E12, 0.03333333333333333], [1.74746586E12, 0.05], [1.74746622E12, 0.08333333333333333], [1.74746748E12, 0.05], [1.7474664E12, 0.016666666666666666]], "isOverall": false, "label": "Matrix Multiply - HTTP Request-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.74746748E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.74746562E12, "maxY": 0.3333333333333333, "series": [{"data": [[1.7474673E12, 0.03333333333333333], [1.74746634E12, 0.2833333333333333], [1.747467E12, 0.016666666666666666], [1.74746592E12, 0.13333333333333333], [1.74746562E12, 0.3333333333333333], [1.74746688E12, 0.016666666666666666], [1.74746628E12, 0.03333333333333333], [1.74746598E12, 0.18333333333333332], [1.74746724E12, 0.03333333333333333], [1.74746586E12, 0.05], [1.74746622E12, 0.08333333333333333], [1.74746748E12, 0.05], [1.7474664E12, 0.016666666666666666]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.74746748E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 7200000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

