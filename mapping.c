
    
        if (proximityData < -33) {
        input = 0.482 * proximityData + -2.589;
        }
    

    
        else if (proximityData < 12) {
        input = 0.222 * proximityData + -11.167;
        }
    

    
        else if (proximityData < 58) {
        input = 0.054 * proximityData + -9.152;
        }
    

    
        else if (proximityData < 127) {
        input = 0.13 * proximityData + -13.565;
        }
    

    
        else if (proximityData < 223) {
        input = 0.13 * proximityData + -13.536;
        }
    

    
        else if (proximityData < 320) {
        input = 0.062 * proximityData + 1.706;
        }
    

    
        else if (proximityData < 548) {
        input = 0.022 * proximityData + 14.482;
        }
    

    
        else if (proximityData < 845) {
        input = 0.03 * proximityData + 9.894;
        }
    

    
        else if (proximityData < 1197) {
        input = 0.033 * proximityData + 7.893;
        }
    

    
        else if (proximityData < 1803) {
        input = 0.017 * proximityData + 26.26;
        }
    

    
        else if (proximityData < 2606) {
        input = 0.008 * proximityData + 42.905;
        }
    

    
        else if (proximityData < 4115) {
        input = 0.004 * proximityData + 52.775;
        }
    

    
        else if (proximityData < 6480) {
        input = 0.004 * proximityData + 53.1;
        }
    

    
        else if (proximityData < 10446) {
        input = 0.002 * proximityData + 70.697;
        }
    

    
        else {
        input = 0.001 * proximityData + 72.088;
        }
    
