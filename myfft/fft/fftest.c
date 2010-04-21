#include <stdio.h>
#include <stdlib.h>
#include "myfft.h"

int main()
        {

    FILE *f;
    int n_channels = 1;
    int n_points = 5000;
    int *buffer, *outbuffer;
    int size;
    int i,j,k;
    int p;


    size = sizeof(int)*n_channels*n_points;
    buffer = malloc(size);
    outbuffer = malloc(size);


    f = fopen("15hz.txt","r");
    for (k=0;k<n_points;k++) {
        fscanf(f,"%i\n",&p);
        buffer[0*n_points+k] = p;
    }
    fclose(f);

/*
    f = fopen("10hz.txt","r");
    for (k=0;k<n_points;k++) {
        fscanf(f,"%i\n",&p);
        buffer[1*n_points+k] = p;
    }
    fclose(f);
*/

    do_fft(n_channels, n_points, buffer, outbuffer);

    f = fopen("15hz.fft","w");
    for (k=0;k<n_points;k++) {
        fprintf(f,"%i\n",outbuffer[0*n_points+k]);
    }
    fclose(f);
/*

    f = fopen("10hz.fft","w");
    for (k=0;k<n_points;k++) {
        fprintf(f,"%i\n",outbuffer[1*n_points+k]);
    }
    fclose(f);
*/
    return 0;
}		
