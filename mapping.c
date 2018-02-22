
    
        if (proximityData < -33) {
        input = 0.482 * proximityData + 5.911;
        }
    

    
        else if (proximityData < 12) {
        input = 0.222 * proximityData + -2.667;
        }
    

    
        else if (proximityData < 58) {
        input = 0.054 * proximityData + -0.652;
        }
    

    
        else if (proximityData < 127) {
        input = 0.13 * proximityData + -5.065;
        }
    

    
        else if (proximityData < 223) {
        input = 0.13 * proximityData + -5.036;
        }
    

    
        else if (proximityData < 320) {
        input = 0.062 * proximityData + 10.206;
        }
    

    
        else if (proximityData < 548) {
        input = 0.022 * proximityData + 22.982;
        }
    

    
        else if (proximityData < 845) {
        input = 0.03 * proximityData + 18.394;
        }
    

    
        else if (proximityData < 1197) {
        input = 0.033 * proximityData + 16.393;
        }
    

    
        else if (proximityData < 1803) {
        input = 0.017 * proximityData + 34.76;
        }
    

    
        else if (proximityData < 2606) {
        input = 0.008 * proximityData + 51.405;
        }
    

    
        else if (proximityData < 4115) {
        input = 0.004 * proximityData + 61.275;
        }
    

    
        else if (proximityData < 6480) {
        input = 0.004 * proximityData + 61.6;
        }
    

    
        else if (proximityData < 10446) {
        input = 0.002 * proximityData + 79.197;
        }
    

    
        else {
        input = 0.001 * proximityData + 80.588;
        }
    
