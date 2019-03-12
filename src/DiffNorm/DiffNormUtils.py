from math import log2, sqrt


log_factorial = [0.0, 0.0, 1.0, 2.58496250072, 4.58496250072, 6.90689059561, 9.49185309633, 12.2992080184,
                 15.2992080184, 18.4691330198, 21.7910611147, 25.2504927334, 28.8354552341, 32.5358949522,
                 36.3432498743, 40.2501404699, 44.2501404699, 48.3376033111, 52.5075283126, 56.755455826,
                 61.0773839209, 65.4697013437, 69.9291329623, 74.4526949184, 79.0376574191, 83.6815136089,
                 88.381953327, 93.1368408292, 97.9441957512, 102.802176746, 107.709067342, 112.663263652,
                 117.663263652, 122.707657772, 127.795120613, 132.92440363, 138.094328631, 143.303781997,
                 148.55170951, 153.837111729, 159.159039824, 164.516591829, 169.908909252, 175.335174006,
                 180.794605625, 186.286458721, 191.810020677, 197.364609529, 202.94957203, 208.564281874,
                 214.208138064, 219.880563406, 225.581003124, 231.308923578, 237.06381108, 242.845170794,
                 248.652525716, 254.48541573, 260.343396725, 266.226039775, 272.13293037, 278.063667708,
                 284.017864018, 289.995143942, 295.995143942, 302.017511755, 308.061905874, 314.127995065,
                 320.215457906, 326.323982363, 332.45326538, 338.603012499, 344.7729375, 350.962762059,
                 357.172215425, 363.401034115, 369.648961629, 375.91574817, 382.201150388, 388.504931137,
                 394.826859232, 401.166709234, 407.524261239, 413.89930067, 420.291618093, 426.701009029,
                 433.127273784, 439.57021728, 446.029648899, 452.505382329, 458.997235426, 465.505030066,
                 472.028592022, 478.567750833, 485.122339685, 491.692195293, 498.277157794, 504.877070636,
                 511.49178048, 518.1211371, 524.76499329, 531.423204773, 538.095630115, 544.782130642,
                 551.48257036, 558.196815878, 564.924736332, 571.666203319, 578.421090821, 585.189275146,
                 591.970634859, 598.765050726, 605.572405648, 612.39258461, 619.225474624, 626.070964675,
                 632.92894567, 639.79931039, 646.681953439, 653.576771203, 660.483661798, 667.402525035,
                 674.333262373, 681.275776878, 688.229973189, 695.195757473, 702.173037397, 709.161722084,
                 716.161722084, 723.172949339, 730.195317152, 737.228740154, 744.273134273, 751.328416708,
                 758.394505899, 765.471321496, 772.558784337, 779.65681642, 786.765340877, 793.88428195,
                 801.013564967, 808.153116319, 815.302863439, 822.462734775, 829.632659777, 836.812568867,
                 844.002393426, 851.20206577, 858.411519136, 865.630687657, 872.859506347, 880.097911086,
                 887.3458386, 894.603226443, 901.870012983, 909.146137389, 916.431539607, 923.726160356,
                 931.029941104, 938.34282406, 945.664752155, 952.995669033, 960.335519036, 967.68424719,
                 975.041799194, 982.408121409, 989.78316084, 997.166865133, 1004.55918256, 1011.96006199,
                 1019.36945293, 1026.78730544, 1034.2135702, 1041.64819842, 1049.09114192, 1056.54235303,
                 1064.00178465, 1071.4693902, 1078.94512363, 1086.42893941, 1093.92079251, 1101.42063839,
                 1108.92843303, 1116.44413287, 1123.96769483, 1131.49907629, 1139.0382351, 1146.58512956,
                 1154.13971841, 1161.70196083, 1169.27181644, 1176.84924527, 1184.43420777, 1192.02666481,
                 1199.62657765, 1207.23390797, 1214.84861781, 1222.47066963, 1230.10002625, 1237.73665087,
                 1245.38050706, 1253.03155875, 1260.68977023, 1268.35510615, 1276.02753149, 1283.70701159,
                 1291.39351212, 1299.08699908, 1306.78743879, 1314.49479793, 1322.20904344, 1329.93014263,
                 1337.65806309, 1345.39277271, 1353.13423969, 1360.88243254, 1368.63732005, 1376.39887128,
                 1384.1670556, 1391.94184266, 1399.72320238, 1407.51110494, 1415.3055208, 1423.1064207,
                 1430.91377562, 1438.72755682, 1446.54773578, 1454.37428427, 1462.20717428, 1470.04637807,
                 1477.89186812, 1485.74361716, 1493.60159815, 1501.4657843, 1509.33614902, 1517.21266597,
                 1525.09530901, 1532.98405226, 1540.87887003, 1548.77973684, 1556.68662743, 1564.59951677,
                 1572.51838, 1580.44319251, 1588.37392985, 1596.31056778, 1604.25308229, 1612.20144952,
                 1620.15564583, 1628.11564776, 1636.08143205, 1644.0529756, 1652.03025553, 1660.0132491,
                 1668.00193379, 1675.99628722, 1683.99628722, 1692.00191177, 1700.01313903, 1708.02994732,
                 1716.05231513, 1724.08022113, 1732.11364413, 1740.15256312, 1748.19695724, 1756.24680579,
                 1764.30208822, 1772.36278415, 1780.42887334, 1788.50033571, 1796.5771513, 1804.65930034,
                 1812.74676319, 1820.83952033, 1828.93755241, 1837.04084022, 1845.14936467, 1853.26310684,
                 1861.38204791, 1869.50616923, 1877.63545224, 1885.76987856, 1893.90942991, 1902.05408816,
                 1910.20383528, 1918.35865339, 1926.51852472, 1934.68343165, 1942.85335665, 1951.02828233,
                 1959.20819142, 1967.39306677, 1975.58289133, 1983.77764818, 1991.97732052, 2000.18189167,
                 2008.39134503, 2016.60566416, 2024.82483268, 2033.04883435, 2041.27765304]

log_double_factorial = [0, 0, 1.58496, 1.58496, 3.90689, 3.90689, 6.71424, 6.71425, 9.88417, 9.88417,
                        13.3436, 13.3436, 17.044, 17.044, 20.9509, 20.9509, 25.0384, 25.0384, 29.2863,
                        29.2863, 33.6786, 33.6786, 38.2022, 38.2022, 42.8461, 42.8461, 47.6009, 47.6009,
                        52.4589, 52.4589, 57.4131, 57.4131, 62.4575, 62.4575, 67.5868, 67.5868, 72.7963,
                        72.7963, 78.0817, 78.0817, 83.4392, 83.4392, 88.8655, 88.8655, 94.3573, 94.3573,
                        99.9119, 99.9119, 105.527, 105.527, 111.199, 111.199, 116.927, 116.927, 122.708,
                        122.708, 128.541, 128.541, 134.424, 134.424, 140.355, 140.355, 146.332, 146.332,
                        152.354, 152.354, 158.42, 158.42, 164.529, 164.529, 170.679, 170.679, 176.868,
                        176.868, 183.097, 183.097, 189.364, 189.364, 195.668, 195.668, 202.008, 202.008,
                        208.383, 208.383, 214.792, 214.792, 221.235, 221.235, 227.711, 227.711, 234.219,
                        234.219, 240.758, 240.758, 247.328, 247.328, 253.928, 253.928, 260.557, 260.557,
                        267.215, 267.215, 273.902, 273.902, 280.616, 280.616, 287.357, 287.357, 294.125,
                        294.125, 300.92, 300.92, 307.74, 307.74, 314.586, 314.586, 321.456, 321.456,
                        328.351, 328.351, 335.27, 335.27, 342.212, 342.212, 349.178, 349.178, 356.167,
                        356.167, 363.178, 363.178, 370.211, 370.211, 377.267, 377.267, 384.343, 384.343,
                        391.441, 391.441, 398.56, 398.56, 405.7, 405.7, 412.86, 412.86, 420.04, 420.04,
                        427.239, 427.239, 434.458, 434.458, 441.697, 441.697, 448.954, 448.954, 456.23, 456.23,
                        463.525, 463.525, 470.838, 470.838, 478.169, 478.169, 485.518, 485.518, 492.884, 492.884,
                        500.268, 500.268, 507.668, 507.668, 515.086, 515.086, 522.521, 522.521, 529.972, 529.972,
                        537.44, 537.44, 544.924, 544.924, 552.423, 552.423, 559.939, 559.939, 567.47, 567.47,
                        575.017, 575.017, 582.58, 582.58, 590.157, 590.157, 597.749, 597.75, 605.357, 605.357,
                        612.979, 612.979, 620.616, 620.615, 628.267, 628.267, 635.932, 635.932, 643.611, 643.611,
                        651.305, 651.305, 659.012, 659.012, 666.733, 666.733, 674.468, 674.468, 682.216, 682.216,
                        689.978, 689.978, 697.753, 697.753, 705.54, 705.54, 713.341, 713.341, 721.155, 721.155,
                        728.982, 728.982, 736.821, 736.821, 744.673, 744.673, 752.537, 752.537, 760.413, 760.413,
                        768.302, 768.302, 776.203, 776.203, 784.116, 784.116, 792.041, 792.041, 799.977, 799.977,
                        807.926, 807.926, 815.886, 815.886, 823.857, 823.857, 831.84, 831.84, 839.835, 839.835,
                        847.84, 847.84, 855.857, 855.857, 863.885, 863.885, 871.924, 871.924, 879.974, 879.974,
                        888.034, 888.034, 896.106, 896.106, 904.188, 904.188, 912.281, 912.281, 920.384, 920.384,
                        928.498, 928.498, 936.622, 936.622, 944.756, 944.756, 952.901, 952.901, 961.056, 961.056,
                        969.221, 969.221, 977.396, 977.396, 985.581, 985.581, 993.775, 993.775, 1001.98, 1001.98,
                        1010.19, 1010.19, 1018.42, 1018.42, 1159.9, 1160.35, 1169.03, 1169.47, 1178.17, 1178.61,
                        1187.32, 1187.76, 1196.47, 1196.92, 1205.64, 1206.08, 1214.82, 1215.26, 1224, 1224.44,
                        1233.19, 1233.64, 1242.4, 1242.84, 1251.61, 1252.05, 1260.83, 1261.27, 1270.06, 1270.5,
                        1279.3, 1279.74, 1288.54, 1288.99, 1297.8, 1298.24, 1307.07, 1307.51, 1316.34, 1316.78,
                        1325.62, 1326.06, 1334.91, 1335.35, 1344.21, 1344.65, 1353.52, 1353.96, 1362.83, 1363.28,
                        1372.16, 1372.6, 1381.49, 1381.93, 1390.83, 1391.27, 1400.18, 1400.62, 1409.54, 1409.98,
                        1418.9, 1419.34, 1428.28, 1428.72, 1437.66, 1438.1, 1447.05, 1447.49, 1456.44, 1456.89,
                        1465.85, 1466.29, 1475.26, 1475.7, 1484.68, 1485.12, 1494.11, 1494.55, 1503.55, 1503.99,
                        1512.99, 1513.43, 1522.44, 1522.88, 1531.9, 1532.34, 1541.37, 1541.81, 1550.84, 1551.28,
                        1560.32, 1560.77, 1569.81, 1570.25, 1579.31, 1579.75, 1588.81, 1589.25, 1598.32, 1598.77,
                        1607.84, 1608.28, 1617.37, 1617.81, 1626.9, 1627.34, 1636.44, 1636.88, 1645.99, 1646.43,
                        1655.54, 1655.98, 1665.1, 1665.55, 1674.67, 1675.11, 1684.25, 1684.69, 1693.83, 1694.27,
                        1703.42, 1703.86, 1713.01, 1713.46, 1722.62, 1723.06, 1732.23, 1732.67, 1741.84, 1742.29,
                        1751.47, 1751.91, 1761.1, 1761.54, 1770.73, 1771.18, 1780.38, 1780.82, 1790.03, 1790.47,
                        1799.69, 1800.13, 1809.35, 1809.79, 1819.02, 1819.46, 1828.7, 1829.14, 1838.38, 1838.82,
                        1848.07, 1848.51, 1857.76, 1858.21, 1867.47, 1867.91, 1877.18, 1877.62, 1886.89, 1887.33,
                        1896.61, 1897.05, 1906.34, 1906.78, 1916.07, 1916.52, 1925.81, 1926.26, 1935.56, 1936,
                        1945.31, 1945.76, 1955.07, 1955.51, 1964.84, 1965.28, 1974.61, 1975.05, 1984.38, 1984.83,
                        1994.17, 1994.61, 2003.96, 2004.4, 2013.75, 2014.2, 2023.55, 2024, 2033.36, 2033.8, 2043.17,
                        2043.62, 2052.99, 2053.44, 2062.82, 2063.26, 2072.65, 2073.09, 2082.49, 2082.93, 2092.33,
                        2092.77, 2102.18, 2102.62, 2112.03, 2112.47, 2121.89, 2122.33, 2131.76, 2132.2, 2141.63,
                        2142.07, 2151.5, 2151.95, 2161.39, 2161.83, 2171.28, 2171.72, 2181.17, 2181.61, 2191.07,
                        2191.51, 2200.97, 2201.42, 2210.88, 2211.33, 2220.8, 2221.24, 2230.72, 2231.16, 2240.65,
                        2241.09, 2250.58, 2251.02, 2260.52, 2260.96, 2270.46, 2270.9, 2280.41, 2280.85, 2290.37,
                        2290.81, 2300.32, 2300.77, 2310.29, 2310.73, 2320.26, 2320.7, 2330.24, 2330.68, 2340.22,
                        40.66, 2350.2, 2350.64, 2360.19, 2360.64, 2370.19, 2370.63, 2380.19, 2380.63, 2390.2,
                        2390.64, 2400.21, 2400.65, 2410.23, 2410.67, 2420.25, 2420.69, 2430.28, 2430.72, 2440.31,
                        2440.75, 2450.35, 2450.79, 2460.39, 2460.83, 2470.44, 2470.88, 2480.49, 2480.93, 2490.55,
                        2490.99, 2500.61, 2501.05, 2510.68, 2511.12, 2520.75, 2521.2, 2530.83, 2531.27, 2540.91,
                        2541.36, 2551, 2551.44, 2561.09, 2561.54, 2571.19, 2571.63, 2581.29, 2581.73, 2591.4,
                        2591.84, 2601.51, 2601.95, 2611.63]

universal_code = [1.51857, 1.51857, 2.51857, 3.10353, 4.51857, 5.05582, 5.47367, 5.81513, 6.10353, 6.35294, 6.57252,
                  6.76853, 6.94549, 7.1067, 7.25471, 7.39148, 8.51857, 8.65957, 8.79117, 8.91452, 9.03056, 9.14009,
                  9.24379, 9.34223, 9.43592, 9.52526, 9.61065, 9.69241, 9.77083, 9.84616, 9.91864, 9.98847, 10.0558,
                  10.1209, 10.1838, 10.2446, 10.3036, 10.3608, 10.4163, 10.4702, 10.5226, 10.5736, 10.6233, 10.6716,
                  10.7188, 10.7648, 10.8097, 10.8535, 10.8963, 10.9382, 10.9791, 11.0192, 11.0584, 11.0968, 11.1344,
                  11.1713, 11.2074, 11.2429, 11.2777, 11.3118, 11.3454, 11.3783, 11.4106, 11.4424, 11.4737, 11.5044,
                  11.5346, 11.5644, 11.5936, 11.6224, 11.6508, 11.6787, 11.7062, 11.7333, 11.76, 11.7863, 11.8123,
                  11.8378, 11.8631, 11.8879, 11.9125, 11.9367, 11.9606, 11.9842, 12.0075, 12.0305, 12.0532, 12.0756,
                  12.0978, 12.1197, 12.1413, 12.1626, 12.1838, 12.2046, 12.2253, 12.2457, 12.2659, 12.2858, 12.3056,
                  12.3251, 12.3444, 12.3635, 12.3824, 12.4012, 12.4197, 12.438, 12.4562, 12.4741, 12.4919, 12.5095,
                  12.527, 12.5443, 12.5614, 12.5783, 12.5951, 12.6118, 12.6283, 12.6446, 12.6608, 12.6768, 12.6927,
                  12.7085, 12.7241, 12.7396, 12.755, 12.7702, 12.7853, 12.8003, 12.8151, 12.8299, 12.8445, 12.859,
                  12.8733, 12.8876, 12.9017, 12.9158, 12.9297, 12.9435, 12.9572, 12.9708, 12.9843, 12.9977, 13.011,
                  13.0242, 13.0373, 13.0503, 13.0633, 13.0761, 13.0888, 13.1015, 13.114, 13.1265, 13.1389, 13.1511,
                  13.1634, 13.1755, 13.1875, 13.1995, 13.2114, 13.2232, 13.2349, 13.2465, 13.2581, 13.2696, 13.281,
                  13.2924, 13.3037, 13.3149, 13.326, 13.3371, 13.3481, 13.359, 13.3699, 13.3807, 13.3914, 13.4021,
                  13.4127, 13.4232, 13.4337, 13.4441, 13.4544, 13.4647, 13.475, 13.4851, 13.4953, 13.5053, 13.5153,
                  13.5253, 13.5352, 13.545, 13.5548, 13.5645, 13.5742, 13.5838, 13.5934, 13.6029, 13.6124, 13.6218,
                  13.6312, 13.6405, 13.6497, 13.659, 13.6681, 13.6773, 13.6863, 13.6954, 13.7044, 13.7133, 13.7222,
                  13.731, 13.7398, 13.7486, 13.7573, 13.766, 13.7746, 13.7832, 13.7918, 13.8003, 13.8087, 13.8172,
                  13.8256, 13.8339, 13.8422, 13.8505, 13.8587, 13.8669, 13.875, 13.8832, 13.8912, 13.8993, 13.9073,
                  13.9153, 13.9232, 13.9311, 13.9389, 13.9468, 13.9546, 13.9623, 13.97, 13.9777, 13.9854, 13.993,
                  14.0006, 14.0082, 14.0157, 14.0232, 14.0306, 14.0381, 14.0455, 14.0528, 14.0602, 14.0675, 14.0747,
                  14.082, 14.0892, 14.0964, 14.1035, 14.1107, 14.1178, 14.1248, 14.1319, 14.1389, 14.1459, 14.1528,
                  14.1597, 14.1666, 14.1735, 14.1804, 14.1872, 14.194, 14.2007, 14.2075, 14.2142, 14.2209, 14.2276,
                  14.2342, 14.2408, 14.2474, 14.254, 14.2605, 14.267, 14.2735, 14.28, 14.2864, 14.2928, 14.2992,
                  14.3056, 14.312, 14.3183, 14.3246, 14.3309, 14.3371, 14.3434, 14.3496, 14.3558, 14.3619, 14.3681,
                  14.3742, 14.3803, 14.3864, 14.3925, 14.3985, 14.4045, 14.4105, 14.4165, 14.4225, 14.4284, 14.4343,
                  14.4402, 14.4461, 14.452, 14.4578, 14.4636, 14.4694, 14.4752, 14.481, 14.4867, 14.4924, 14.4981,
                  14.5038, 14.5095, 14.5151, 14.5208, 14.5264, 14.532, 14.5376, 14.5431, 14.5487, 14.5542, 14.5597,
                  14.5652, 14.5707, 14.5761, 14.5815, 14.587, 14.5924, 14.5978, 14.6031, 14.6085, 14.6138, 14.6191,
                  14.6244, 14.6297, 14.635, 14.6403, 14.6455, 14.6507, 14.6559, 14.6611, 14.6663, 14.6715, 14.6766,
                  14.6818, 14.6869, 14.692, 14.6971, 14.7021, 14.7072, 14.7122, 14.7173, 14.7223, 14.7273, 14.7323,
                  14.7372, 14.7422, 14.7471, 14.7521, 14.757, 14.7619, 14.7668, 14.7716, 14.7765, 14.7813, 14.7862,
                  14.791, 14.7958, 14.8006, 14.8054, 14.8101, 14.8149, 14.8196, 14.8243, 14.8291, 14.8338, 14.8385,
                  14.8431, 14.8478, 14.8524, 14.8571, 14.8617, 14.8663, 14.8709, 14.8755, 14.8801, 14.8847, 14.8892,
                  14.8937, 14.8983, 14.9028, 14.9073, 14.9118, 14.9163, 14.9207, 14.9252, 14.9296, 14.9341, 14.9385,
                  14.9429, 14.9473, 14.9517, 14.9561, 14.9605, 14.9648, 14.9692, 14.9735, 14.9778, 14.9821, 14.9864,
                  14.9907, 14.995, 14.9993, 15.0036, 15.0078, 15.012, 15.0163, 15.0205, 15.0247, 15.0289, 15.0331,
                  15.0373, 15.0414, 15.0456, 15.0497, 15.0539, 15.058, 15.0621, 15.0662, 15.0703, 15.0744, 15.0785,
                  15.0826, 15.0866, 15.0907, 15.0947, 15.0988, 15.1028, 15.1068, 15.1108, 15.1148, 15.1188, 15.1228,
                  15.1267, 15.1307, 15.1346, 15.1386, 15.1425, 15.1464, 15.1503, 15.1543, 15.1581, 15.162, 15.1659,
                  15.1698, 15.1736, 15.1775, 15.1813, 15.1852, 15.189, 15.1928, 15.1966, 15.2004, 15.2042, 15.208,
                  15.2118, 15.2155, 15.2193, 15.2231, 15.2268, 15.2305, 15.2343, 15.238, 15.2417, 15.2454, 15.2491,
                  15.2528, 15.2565, 15.2601, 15.2638, 15.2675, 15.2711, 15.2747, 15.2784, 15.282, 15.2856, 15.2892,
                  15.2928, 15.2964, 15.3, 15.3036, 15.3072, 15.3107, 15.3143, 15.3178, 15.3214, 15.3249, 15.3284,
                  15.332, 15.3355, 15.339, 15.3425, 15.346, 15.3495, 15.3529, 15.3564, 15.3599, 15.3633, 15.3668,
                  15.3702, 15.3737, 15.3771, 15.3805, 15.3839, 15.3873, 15.3907, 15.3941, 15.3975, 15.4009, 15.4043,
                  15.4077, 15.411, 15.4144, 15.4177, 15.4211, 15.4244, 15.4277, 15.4311, 15.4344, 15.4377, 15.441,
                  15.4443, 15.4476, 15.4509, 15.4542, 15.4574, 15.4607, 15.464, 15.4672, 15.4705, 15.4737, 15.4769,
                  15.4802, 15.4834, 15.4866, 15.4898, 15.493, 15.4962, 15.4994, 15.5026, 15.5058, 15.509, 15.5121,
                  15.5153, 15.5185, 15.5216, 15.5248, 15.5279, 15.531, 15.5342, 15.5373, 15.5404, 15.5435, 15.5466,
                  15.5497, 15.5528, 15.5559, 15.559, 15.5621, 15.5652, 15.5682, 15.5713, 15.5743, 15.5774, 15.5804,
                  15.5835, 15.5865, 15.5895, 15.5926, 15.5956, 15.5986, 15.6016, 15.6046, 15.6076, 15.6106, 15.6136,
                  15.6166, 15.6196, 15.6225, 15.6255, 15.6285, 15.6314, 15.6344, 15.6373, 15.6403, 15.6432, 15.6461,
                  15.6491, 15.652, 15.6549, 15.6578, 15.6607, 15.6636, 15.6665, 15.6694, 15.6723, 15.6752, 15.6781,
                  15.6809, 15.6838, 15.6867, 15.6895, 15.6924, 15.6952, 15.6981, 15.7009, 15.7037, 15.7066, 15.7094,
                  15.7122, 15.715, 15.7178, 15.7206, 15.7234, 15.7262, 15.729, 15.7318, 15.7346, 15.7374, 15.7402,
                  15.7429, 15.7457, 15.7485, 15.7512, 15.754, 15.7567, 15.7595, 15.7622, 15.7649, 15.7677, 15.7704,
                  15.7731, 15.7758, 15.7786, 15.7813, 15.784, 15.7867, 15.7894, 15.7921, 15.7947, 15.7974, 15.8001,
                  15.8028, 15.8055, 15.8081, 15.8108, 15.8134, 15.8161, 15.8187, 15.8214, 15.824, 15.8267, 15.8293,
                  15.8319, 15.8346, 15.8372, 15.8398, 15.8424, 15.845, 15.8476, 15.8502, 15.8528, 15.8554, 15.858,
                  15.8606, 15.8632, 15.8658, 15.8683, 15.8709, 15.8735, 15.876, 15.8786, 15.8811, 15.8837, 15.8862,
                  15.8888, 15.8913, 15.8939, 15.8964, 15.8989, 15.9015, 15.904, 15.9065, 15.909, 15.9115, 15.914,
                  15.9165, 15.919, 15.9215, 15.924, 15.9265, 15.929, 15.9315, 15.9339, 15.9364, 15.9389, 15.9414,
                  15.9438, 15.9463, 15.9487, 15.9512, 15.9536, 15.9561, 15.9585, 15.961, 15.9634, 15.9658, 15.9683,
                  15.9707, 15.9731, 15.9755, 15.9779, 15.9803, 15.9827, 15.9852, 15.9876, 15.99, 15.9923, 15.9947,
                  15.9971, 15.9995, 16.0019, 16.0043, 16.0066, 16.009, 16.0114, 16.0137, 16.0161, 16.0185, 16.0208,
                  16.0232, 16.0255, 16.0279, 16.0302, 16.0325, 16.0349, 16.0372, 16.0395, 16.0419, 16.0442, 16.0465,
                  16.0488, 16.0511, 16.0534, 16.0557, 16.058, 16.0603, 16.0626, 16.0649, 16.0672, 16.0695, 16.0718,
                  16.0741, 16.0764, 16.0786, 16.0809, 16.0832, 16.0854, 16.0877, 16.09, 16.0922, 16.0945, 16.0967,
                  16.099, 16.1012, 16.1035, 16.1057, 16.1079, 16.1102, 16.1124, 16.1146, 16.1169, 16.1191, 16.1213,
                  16.1235, 16.1257, 16.1279, 16.1302, 16.1324, 16.1346, 16.1368, 16.139, 16.1412, 16.1433, 16.1455,
                  16.1477, 16.1499, 16.1521, 16.1543, 16.1564, 16.1586, 16.1608, 16.1629, 16.1651, 16.1673, 16.1694,
                  16.1716, 16.1737, 16.1759, 16.178, 16.1802, 16.1823, 16.1844, 16.1866, 16.1887, 16.1908, 16.193,
                  16.1951, 16.1972, 16.1993, 16.2015, 16.2036, 16.2057, 16.2078, 16.2099, 16.212, 16.2141, 16.2162,
                  16.2183, 16.2204, 16.2225, 16.2246, 16.2267, 16.2287, 16.2308, 16.2329, 16.235, 16.237, 16.2391,
                  16.2412, 16.2433, 16.2453, 16.2474, 16.2494, 16.2515, 16.2535, 16.2556, 16.2576, 16.2597, 16.2617,
                  16.2638, 16.2658, 16.2678, 16.2699, 16.2719, 16.2739, 16.276, 16.278, 16.28, 16.282, 16.284, 16.2861,
                  16.2881, 16.2901, 16.2921, 16.2941, 16.2961, 16.2981, 16.3001, 16.3021, 16.3041, 16.3061, 16.3081,
                  16.3101, 16.312, 16.314, 16.316, 16.318, 16.3199, 16.3219, 16.3239, 16.3259, 16.3278, 16.3298,
                  16.3317, 16.3337, 16.3357, 16.3376, 16.3396, 16.3415, 16.3435, 16.3454, 16.3474, 16.3493, 16.3512,
                  16.3532, 16.3551, 16.357, 16.359, 16.3609, 16.3628, 16.3647, 16.3667, 16.3686, 16.3705, 16.3724,
                  16.3743, 16.3762, 16.3781, 16.38, 16.382, 16.3839, 16.3858, 16.3876, 16.3895, 16.3914, 16.3933,
                  16.3952, 16.3971, 16.399, 16.4009, 16.4028, 16.4046, 16.4065, 16.4084, 16.4103, 16.4121, 16.414,
                  16.4159, 16.4177, 16.4196, 16.4214, 16.4233, 16.4252, 16.427, 16.4289, 16.4307, 16.4326, 16.4344,
                  16.4362, 16.4381, 16.4399, 16.4418, 16.4436, 16.4454, 16.4473, 16.4491, 16.4509, 16.4528, 16.4546,
                  16.4564, 16.4582, 16.46, 16.4619, 16.4637, 16.4655, 16.4673, 16.4691, 16.4709, 16.4727, 16.4745,
                  16.4763, 16.4781, 16.4799, 16.4817, 16.4835, 16.4853, 16.4871, 16.4889, 16.4907, 16.4924, 16.4942,
                  16.496, 16.4978, 16.4995, 16.5013, 16.5031, 16.5049, 16.5066, 16.5084, 16.5102, 16.5119, 16.5137,
                  16.5155, 16.5172, 16.519, 16.5207, 16.5225, 16.5242, 16.526, 16.5277, 16.5295, 16.5312, 16.5329,
                  16.5347, 16.5364, 16.5382, 16.5399, 16.5416, 16.5434, 16.5451, 16.5468, 16.5485, 16.5503, 16.552,
                  16.5537, 16.5554, 16.5571, 16.5589, 16.5606, 16.5623, 16.564, 16.5657, 16.5674, 16.5691, 16.5708,
                  16.5725, 16.5742, 16.5759, 16.5776, 16.5793, 16.581, 16.5827, 16.5844, 16.5861, 16.5877, 16.5894,
                  16.5911, 16.5928, 16.5945, 16.5962, 16.5978, 16.5995, 16.6012, 16.6028, 16.6045, 16.6062, 16.6079,
                  16.6095, 16.6112, 16.6128, 16.6145, 16.6162, 16.6178, 16.6195, 16.6211, 16.6228, 16.6244, 16.6261,
                  16.6277, 16.6294, 16.631, 16.6327, 16.6343, 16.6359, 16.6376, 16.6392, 16.6408, 16.6425, 16.6441,
                  16.6457, 16.6474, 16.649, 16.6506, 16.6522, 16.6539, 16.6555, 16.6571, 16.6587, 16.6603, 16.6619,
                  16.6635, 16.6652, 16.6668, 16.6684, 16.67, 16.6716, 16.6732, 16.6748, 16.6764, 16.678, 16.6796,
                  16.6812, 16.6828, 16.6844, 16.686, 16.6875, 16.6891, 16.6907, 16.6923, 16.6939, 16.6955, 16.6971,
                  16.6986, 16.7002, 16.7018, 16.7034, 16.7049, 16.7065, 16.7081, 16.7096, 16.7112, 16.7128, 16.7143,
                  16.7159, 16.7175, 16.719, 16.7206, 16.7221, 16.7237, 16.7253, 16.7268, 16.7284, 16.7299, 16.7315,
                  16.733, 16.7346, 16.7361, 16.7376, 16.7392, 16.7407, 16.7423, 16.7438, 16.7453, 16.7469, 16.7484,
                  16.7499, 16.7515, 16.753, 16.7545, 16.756, 16.7576, 16.7591, 16.7606, 16.7621, 16.7637, 16.7652,
                  16.7667, 16.7682, 16.7697, 16.7712, 16.7727, 16.7743, 16.7758, 16.7773, 16.7788, 16.7803, 16.7818,
                  16.7833, 16.7848, 16.7863, 16.7878, 16.7893, 16.7908, 16.7923, 16.7938, 16.7953, 16.7967, 16.7982,
                  16.7997, 16.8012, 16.8027, 16.8042, 16.8057, 16.8071, 16.8086, 16.8101, 16.8116, 16.813, 16.8145,
                  16.816, 16.8175, 16.8189, 16.8204, 16.8219, 16.8233, 16.8248, 16.8263, 16.8277, 16.8292, 16.8307,
                  16.8321, 16.8336, 16.835, 16.8365, 16.8379, 16.8394, 16.8408, 16.8423, 16.8437, 16.8452, 16.8466,
                  16.8481, 16.8495, 16.851, 16.8524, 16.8538, 16.8553, 16.8567, 16.8582, 16.8596, 16.861, 16.8625,
                  16.8639, 16.8653, 16.8668, 16.8682, 16.8696, 16.871, 16.8725, 16.8739, 16.8753, 16.8767, 16.8782,
                  16.8796, 16.881, 16.8824, 16.8838, 16.8852, 16.8866, 16.8881, 16.8895, 16.8909, 16.8923, 16.8937,
                  16.8951, 16.8965, 16.8979, 16.8993, 16.9007, 16.9021, 16.9035, 16.9049, 16.9063, 16.9077, 16.9091,
                  16.9105, 16.9119, 16.9133, 16.9147, 16.916, 16.9174, 16.9188, 16.9202, 16.9216, 16.923, 16.9243,
                  16.9257, 16.9271, 16.9285, 16.9299, 16.9312, 16.9326, 16.934, 16.9354, 16.9367, 16.9381, 16.9395,
                  16.9408, 16.9422, 16.9436, 16.9449, 16.9463, 16.9477, 16.949, 16.9504, 16.9517, 16.9531, 16.9545,
                  16.9558, 16.9572, 16.9585, 16.9599, 16.9612, 16.9626, 16.9639, 16.9653, 16.9666, 16.968, 16.9693,
                  16.9707, 16.972, 16.9733, 16.9747, 16.976, 16.9774, 16.9787, 16.98, 16.9814, 16.9827, 16.984,
                  16.9854, 16.9867, 16.988, 16.9894, 16.9907, 16.992, 16.9933, 16.9947, 16.996, 16.9973, 16.9986,
                  17, 17.0013, 17.0026, 17.0039, 17.0052, 17.0065, 17.0079, 17.0092, 17.0105, 17.0118, 17.0131,
                  17.0144, 17.0157, 17.017, 17.0183, 17.0196, 17.021, 17.0223, 17.0236, 17.0249, 17.0262, 17.0275,
                  17.0288, 17.0301, 17.0314, 17.0326, 17.0339, 17.0352, 17.0365, 17.0378, 17.0391, 17.0404, 17.0417,
                  17.043, 17.0443, 17.0455, 17.0468, 17.0481, 17.0494, 17.0507, 17.052, 17.0532, 17.0545, 17.0558,
                  17.0571, 17.0584, 17.0596, 17.0609, 17.0622, 17.0634, 17.0647, 17.066, 17.0673, 17.0685, 17.0698,
                  17.0711, 17.0723, 17.0736, 17.0749, 17.0761, 17.0774, 17.0786, 17.0799, 17.0812, 17.0824, 17.0837,
                  17.0849, 17.0862, 17.0874, 17.0887, 17.0899, 17.0912, 17.0924, 17.0937, 17.0949, 17.0962, 17.0974,
                  17.0987, 17.0999, 17.1012, 17.1024, 17.1037, 17.1049, 17.1061, 17.1074, 17.1086, 17.1098, 17.1111,
                  17.1123, 17.1136, 17.1148, 17.116, 17.1173, 17.1185, 17.1197, 17.1209, 17.1222, 17.1234, 17.1246,
                  17.1259, 17.1271, 17.1283, 17.1295, 17.1307, 17.132, 17.1332, 17.1344, 17.1356, 17.1368, 17.1381,
                  17.1393, 17.1405, 17.1417, 17.1429, 17.1441, 17.1453, 17.1466, 17.1478, 17.149, 17.1502, 17.1514,
                  17.1526, 17.1538, 17.155, 17.1562, 17.1574, 17.1586, 17.1598, 17.161, 17.1622, 17.1634, 17.1646,
                  17.1658, 17.167, 17.1682, 17.1694, 17.1706, 17.1718, 17.173, 17.1742, 17.1754, 17.1765, 17.1777,
                  17.1789, 17.1801, 17.1813, 17.1825, 17.1837, 17.1848, 17.186, 17.1872, 17.1884, 17.1896, 17.1907,
                  17.1919, 17.1931, 17.1943, 17.1955, 17.1966, 17.1978, 17.199, 17.2002, 17.2013, 17.2025, 17.2037,
                  17.2048, 17.206, 17.2072, 17.2083, 17.2095, 17.2107, 17.2118, 17.213, 17.2142, 17.2153, 17.2165,
                  17.2176, 17.2188, 17.22, 17.2211, 17.2223, 17.2234, 17.2246, 17.2258, 17.2269, 17.2281, 17.2292,
                  17.2304, 17.2315, 17.2327, 17.2338, 17.235, 17.2361, 17.2373, 17.2384, 17.2395, 17.2407, 17.2418,
                  17.243, 17.2441, 17.2453, 17.2464, 17.2475, 17.2487, 17.2498, 17.251, 17.2521, 17.2532, 17.2544,
                  17.2555, 17.2566, 17.2578, 17.2589, 17.26, 17.2612, 17.2623, 17.2634, 17.2646, 17.2657, 17.2668,
                  17.2679, 17.2691, 17.2702, 17.2713, 17.2724, 17.2736, 17.2747, 17.2758, 17.2769, 17.278, 17.2792,
                  17.2803, 17.2814, 17.2825, 17.2836, 17.2847, 17.2859, 17.287, 17.2881, 17.2892, 17.2903, 17.2914,
                  17.2925, 17.2936, 17.2947, 17.2959, 17.297, 17.2981, 17.2992, 17.3003, 17.3014, 17.3025, 17.3036,
                  17.3047, 17.3058, 17.3069, 17.308, 17.3091, 17.3102, 17.3113, 17.3124, 17.3135, 17.3146, 17.3157,
                  17.3168, 17.3179, 17.319, 17.32, 17.3211, 17.3222, 17.3233, 17.3244, 17.3255, 17.3266, 17.3277,
                  17.3288, 17.3298, 17.3309, 17.332, 17.3331, 17.3342, 17.3353, 17.3363, 17.3374, 17.3385, 17.3396,
                  17.3407, 17.3417, 17.3428, 17.3439, 17.345, 17.346, 17.3471, 17.3482, 17.3493, 17.3503, 17.3514,
                  17.3525, 17.3535, 17.3546, 17.3557, 17.3568, 17.3578, 17.3589, 17.36, 17.361, 17.3621, 17.3632,
                  17.3642, 17.3653, 17.3663, 17.3674, 17.3685, 17.3695, 17.3706, 17.3716, 17.3727, 17.3738, 17.3748,
                  17.3759, 17.3769, 17.378, 17.379, 17.3801, 17.3811, 17.3822, 17.3832, 17.3843, 17.3854, 17.3864,
                  17.3875, 17.3885, 17.3895, 17.3906, 17.3916, 17.3927, 17.3937, 17.3948, 17.3958, 17.3969, 17.3979,
                  17.3989, 17.4, 17.401, 17.4021, 17.4031, 17.4041, 17.4052, 17.4062, 17.4073, 17.4083, 17.4093,
                  17.4104, 17.4114, 17.4124, 17.4135, 17.4145, 17.4155, 17.4166, 17.4176, 17.4186, 17.4196, 17.4207,
                  17.4217, 17.4227, 17.4238, 17.4248, 17.4258, 17.4268, 17.4279, 17.4289, 17.4299, 17.4309, 17.4319,
                  17.433, 17.434, 17.435, 17.436, 17.437, 17.4381, 17.4391, 17.4401, 17.4411, 17.4421, 17.4431,
                  17.4442, 17.4452, 17.4462, 17.4472, 17.4482, 17.4492, 17.4502, 17.4512, 17.4522, 17.4533, 17.4543,
                  17.4553, 17.4563, 17.4573, 17.4583, 17.4593, 17.4603, 17.4613, 17.4623, 17.4633, 17.4643, 17.4653,
                  17.4663, 17.4673, 17.4683, 17.4693, 17.4703, 17.4713, 17.4723, 17.4733, 17.4743, 17.4753, 17.4763,
                  17.4773, 17.4783, 17.4793, 17.4803, 17.4813, 17.4823, 17.4832, 17.4842, 17.4852, 17.4862, 17.4872,
                  17.4882, 17.4892, 17.4902, 17.4911, 17.4921, 17.4931, 17.4941, 17.4951, 17.4961, 17.4971, 17.498,
                  17.499, 17.5, 17.501, 17.502, 17.5029, 17.5039, 17.5049, 17.5059, 17.5068, 17.5078, 17.5088,
                  17.5098, 17.5107, 17.5117, 17.5127, 17.5137, 17.5146, 17.5156, 17.5166, 17.5176, 17.5185, 17.5195,
                  17.5205, 17.5214, 17.5224, 17.5234, 17.5243, 17.5253, 17.5263, 17.5272, 17.5282, 17.5292, 17.5301,
                  17.5311, 17.532, 17.533, 17.534, 17.5349, 17.5359, 17.5369, 17.5378, 17.5388, 17.5397, 17.5407,
                  17.5416, 17.5426, 17.5436, 17.5445, 17.5455, 17.5464, 17.5474, 17.5483, 17.5493, 17.5502, 17.5512,
                  17.5521, 17.5531, 17.554, 17.555, 17.5559, 17.5569, 17.5578, 17.5588, 17.5597, 17.5607, 17.5616,
                  17.5626, 17.5635, 17.5644, 17.5654, 17.5663, 17.5673, 17.5682, 17.5692, 17.5701, 17.571, 17.572,
                  17.5729, 17.5739, 17.5748, 17.5757, 17.5767, 17.5776, 17.5785, 17.5795, 17.5804, 17.5813, 17.5823,
                  17.5832, 17.5841, 17.5851, 17.586, 17.5869, 17.5879, 17.5888, 17.5897, 17.5907, 17.5916, 17.5925,
                  17.5934, 17.5944, 17.5953, 17.5962, 17.5972, 17.5981, 17.599, 17.5999, 17.6009, 17.6018, 17.6027,
                  17.6036, 17.6045, 17.6055, 17.6064, 17.6073, 17.6082, 17.6091, 17.6101, 17.611, 17.6119, 17.6128,
                  17.6137, 17.6146, 17.6156, 17.6165, 17.6174, 17.6183, 17.6192, 17.6201, 17.621, 17.622, 17.6229,
                  17.6238, 17.6247, 17.6256, 17.6265, 17.6274, 17.6283, 17.6292, 17.6301, 17.6311, 17.632, 17.6329,
                  17.6338, 17.6347, 17.6356, 17.6365, 17.6374, 17.6383, 17.6392, 17.6401, 17.641, 17.6419, 17.6428,
                  17.6437, 17.6446, 17.6455, 17.6464, 17.6473, 17.6482, 17.6491, 17.65, 17.6509, 17.6518, 17.6527,
                  17.6536, 17.6545, 17.6554, 17.6563, 17.6571, 17.658, 17.6589, 17.6598, 17.6607, 17.6616, 17.6625,
                  17.6634, 17.6643, 17.6652, 17.666, 17.6669, 17.6678, 17.6687, 17.6696, 17.6705, 17.6714, 17.6723,
                  17.6731, 17.674, 17.6749, 17.6758, 17.6767, 17.6776, 17.6784, 17.6793, 17.6802, 17.6811, 17.682,
                  17.6828, 17.6837, 17.6846, 17.6855, 17.6864, 17.6872, 17.6881, 17.689, 17.6899, 17.6907, 17.6916,
                  17.6925, 17.6934, 17.6942, 17.6951, 17.696, 17.6968, 17.6977, 17.6986, 17.6995, 17.7003, 17.7012,
                  17.7021, 17.7029, 17.7038, 17.7047, 17.7055, 17.7064, 17.7073, 17.7081, 17.709, 17.7099, 17.7107,
                  17.7116, 17.7125, 17.7133, 17.7142, 17.7151, 17.7159, 17.7168, 17.7176, 17.7185, 17.7194, 17.7202,
                  17.7211, 17.7219, 17.7228, 17.7237, 17.7245, 17.7254, 17.7262, 17.7271, 17.7279]

pi = 3.14159265358979323846264338327950288

log_sqrt_pi = log2(sqrt(pi))

log_of_dbl_pi = log2(2 * pi)


def universal_code_len(number):
    if number <= 2000:
        return universal_code[number]
    res = 1.51856736636  # log2(2.86504), kraft inequality
    previous = number
    while True:
        previous = log2(previous)
        if previous < 1:
            break
        res += previous
    return res


def log_gamma(number):
    if number <= 0:
        return 0
    if number == 0.5:
        return log_sqrt_pi
    return 0.5 * (log_of_dbl_pi - log2(number)) + number * (log2(number + 1/(12 * number - 1/(10 * number))) - 1)


def calc_log_factorial(number):
    if number <= 300:
        return log_factorial[number]
    return number * log2(number) - number + log2(sqrt(2 * pi * number))


def calc_log_double_factorial(number):
    if number <= 1:
        return 0.0
    if number <= 600:
        return log_double_factorial[number]
    #  (2n-1)! = (2n)!/(2^n * n!) <= expand in log2
    two_n = number + 1
    n = two_n / 2
    return calc_log_factorial(two_n) - n - calc_log_factorial(n)
