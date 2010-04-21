#include <stdio.h>
#include <math.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <cufft.h>

#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int iter = 0;

int do_fft(int n_channels, int n_points, int *buffer, int *outbuffer)
{
    cufftHandle plan;
    cufftComplex *devPtr;
    //cufftReal indata[n_points*n_channels];
    //cufftComplex data[n_points*n_channels];
    //cufftReal *indata;
    cufftComplex *data;
    int i,timer,j,k;
    char fname[15];
    FILE *f;
	int bufsize;
	int toread;
	char *ptr;
    int p,nread;

	data = malloc(n_points*n_channels*sizeof(cufftComplex));
    bufsize = n_points*n_channels*sizeof(int);

    i=0;
    for (j=0;j<n_channels;j++) {
        for (k=0;k<n_points;k++) {
            data[j*n_points+k].x = buffer[j*n_points+k];
            data[j*n_points+k].y = 0;
	    }
	}
    

        /* WORK  WITHOUT SOCKT
	
            f = fopen("1hz.txt","r");
            for (k=0;k<n_points;k++) {
                fscanf(f,"%i\n",&p);
                data[0*n_points+k].x = p;
                data[0*n_points+k].y = 0;
            }
            fclose(f);


            f = fopen("5hz.txt","r");
            for (k=0;k<n_points;k++) {
                fscanf(f,"%i\n",&p);
                data[1*n_points+k].x = p;
                data[1*n_points+k].y = 0;
            }
            fclose(f);
            */
		
    /*
        i=0;
        for (j=0;j<n_channels;j++) {
            sprintf(fname,"%i.txt",j);
            printf("%s\n",fname);
            f = fopen(fname,"r");
            for (k=0;k<n_points;k++) {
                fscanf(f,"%i\n",&p);
                data[j*n_points+k].x = p;
                data[j*n_points+k].y = 0;
            }
            fclose(f);
	*/
/*
        for(i=  0 ; i < n_points*n_channels ; i++){
                //fscanf(f,"%i\n",&p);
                //data[i].x= p;
                data[i].x= 1.0f;
                //printf("%f\n",data[i].x);
                data[i].y = 0.0f;
        }
        //fclose(f)
        */
        //}


        /* creates 1D FFT plan */
        cufftPlan1d(&plan, n_points, CUFFT_C2C, n_channels);


        /*
        cutCreateTimer(&timer);
        cutResetTimer(timer);
        cutStartTimer(timer);
        */
        
    /* GPU memory allocation */
        cudaMalloc((void**)&devPtr, sizeof(cufftComplex)*n_points*n_channels);

    /* transfer to GPU memory */
        cudaMemcpy(devPtr, data, sizeof(cufftComplex)*n_points*n_channels, cudaMemcpyHostToDevice);


        /* executes FFT processes */
        cufftExecC2C(plan, devPtr, devPtr, CUFFT_FORWARD);

        /* executes FFT processes (inverse transformation) */
       //cufftExecC2C(plan, devPtr, devPtr, CUFFT_INVERSE);

    /* transfer results from GPU memory */
        cudaMemcpy(data, devPtr, sizeof(cufftComplex)*n_points*n_channels, cudaMemcpyDeviceToHost);

        /* deletes CUFFT plan */
        cufftDestroy(plan);

    /* frees GPU memory */
        cudaFree(devPtr);

        /*
        cudaThreadSynchronize();
        cutStopTimer(timer);
        printf("%f\n",cutGetTimerValue(timer)/(float)1000);
        cutDeleteTimer(timer);
        */

        /*
        float mag;
        for(i = 0 ; i < n_points*n_channels ; i++){
                //printf("data[%d] %f %f\n", i, data[i].x, data[i].y);
                //printf("%f\n", data[i].x);
                mag = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/n_points;
                printf("%f\n",mag);

        }
        */

/*
        // save as text file
        float mag;
        i=0;
        for (j=0;j<n_channels;j++) {
            sprintf(fname,"%i-mag.txt",j);
            printf("%s\n",fname);
            f = fopen(fname,"w");
            for (k=0;k<n_points;k++) {
                //fscanf(f,"%i\n",&p);
                if (k>50)
                    continue;
                i = j*n_points+k;
                mag = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/n_points;
                fprintf(f,"%f\n",mag);
            }
            fclose(f);
        }
*/


        float mag;
        i=0;
        float *mags;//[n_points];
	mags = malloc(sizeof(float)*n_points);
//        int magsint[n_points*n_channels];
        int *magsint;
	magsint = malloc(sizeof(int)*n_points*n_channels);
        memset(magsint,0,sizeof(int)*n_points*n_channels);
        int u = 0;

        printf("%f %f %f %f\n",data[0].x,data[1].x,data[2].x,data[3].x);

        //printf("%i %i %i %i\n",magsint[0],magsint[1],magsint[2],magsint[3]);

//        f = fopen("ffts.bin","wb");
        for (j=0;j<n_channels;j++) {
            //sprintf(fname,"%i-test.text",j*5);
            //printf("%s\n",fname);

            //f = fopen(fname,"w");
            for (k=0;k<n_points;k++) {
                //fscanf(f,"%i\n",&p);
                /*if (k>=n_fft_points)
                    continue;*/
                i = j*n_points+k;
                mags[k] = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/n_points;
                magsint[u]=mags[k]    ;
                outbuffer[u]=mags[k];
                //fprintf(f,"%i\n",magsint[u]);
                u++;
                
            }
            //fclose(f);
	/*
	    if (j==(n_channels-1)) {
		f = fopen("test.txt","w");
		for (k=0;k<

	    }*/

            //f = fopen(fname,"wb");
  //          fwrite(magsint,sizeof(int)*50,1,f);
        }

        //exit(0);
        /*
        char sign[255];
        
        
        sprintf(fname,"fftout/%i.eeg",iter++);
        
        //sprintf(sign,";EEG binary\n;frequency 5000\n;n-channels %i\n;n-points %i\n;type int\n",
        sprintf(sign,";n-channels %i\n;n-points %i\n",
            n_channels,n_fft_points);
        f = fopen(fname,"wb");
        fwrite(sign,strlen(sign),1,f);
        fwrite(magsint,sizeof(int)*n_channels*n_fft_points,1,f);
        fclose(f);
        


        printf("filename %s\n",fname);
        */
        
        /*
        int n;
        n = write(sockfd,magsint,sizeof(int)*n_channels*n_fft_points);
        printf("%i %i %i %i\n",magsint[0],magsint[1],magsint[2],magsint[3]);
        printf("send ok, size: %i\n",n);
        //fclose(f);
        */
    
	free(magsint);    
	free(data);
	//free(buffer);
	free(mags);
        
    return 0;
}

