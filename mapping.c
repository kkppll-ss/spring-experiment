
    
        if (proximityData < -33) {
        input = 0.482 * proximityData + 15.911;
        }
    

    
        else if (proximityData < 12) {
        input = 0.222 * proximityData + 7.333;
        }
    

    
        else if (proximityData < 58) {
        input = 0.054 * proximityData + 9.348;
        }
    

    
        else if (proximityData < 127) {
        input = 0.13 * proximityData + 4.935;
        }
    

    
        else if (proximityData < 223) {
        input = 0.13 * proximityData + 4.964;
        }
    

    
        else if (proximityData < 320) {
        input = 0.062 * proximityData + 20.206;
        }
    

    
        else if (proximityData < 548) {
        input = 0.022 * proximityData + 32.982;
        }
    

    
        else if (proximityData < 845) {
        input = 0.03 * proximityData + 28.394;
        }
    

    
        else if (proximityData < 1197) {
        input = 0.033 * proximityData + 26.393;
        }
    

    
        else if (proximityData < 1803) {
        input = 0.017 * proximityData + 44.76;
        }
    

    
        else if (proximityData < 2606) {
        input = 0.008 * proximityData + 61.405;
        }
    

    
        else if (proximityData < 4115) {
        input = 0.004 * proximityData + 71.275;
        }
    

    
        else if (proximityData < 6480) {
        input = 0.004 * proximityData + 71.6;
        }
    

    
        else if (proximityData < 10446) {
        input = 0.002 * proximityData + 89.197;
        }
    

    
        else {
        input = 0.001 * proximityData + 90.588;
        }
    
