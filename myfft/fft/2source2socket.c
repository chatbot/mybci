#include <stdio.h>
#include <math.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <cufft.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define NX      4096
#define BATCH   12
//#define N_FFT_POINTS 100 // number of fft points to send forward


struct sockaddr_in serv_addr;

int n_channels;
int n_fft_points;
int n_points;
int iter = 0;

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(0);
}

int main2(int sockfd, int inputsock)
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
	//#define BUFSIZE (21*4096*sizeof(int))
	int *buffer;//[BUFSIZE];
	int bufsize;
	int toread;
	char *ptr;


        int p,nread;

	data = malloc(n_points*n_channels*sizeof(cufftComplex));

	bufsize = n_points*n_channels*sizeof(int);
	buffer = malloc(bufsize);

    /* READ NETWORK DATA */
	ptr = buffer;
	toread = bufsize;
	while (toread > 0) {
		nread=recv(inputsock,ptr,toread,0);
        if (nread==0) {
            printf("input socket closed, exiting\n");
            exit(0);
        } else if (nread <0) {
            DieWithError("error on input socket");
        } else {
		    toread-=nread;
		    ptr+=nread;
		    printf("nread=%i\n",nread);
        }
	}


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
                if (k>=n_fft_points)
                    continue;
                i = j*n_points+k;
                mags[k] = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/n_points;
                magsint[u]=mags[k]    ;
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


        int n;
        n = write(sockfd,magsint,sizeof(int)*n_channels*n_fft_points);
        printf("%i %i %i %i\n",magsint[0],magsint[1],magsint[2],magsint[3]);
        printf("send ok, size: %i\n",n);
        //fclose(f);
    
	free(magsint);    
	free(data);
	free(buffer);
	free(mags);
        
        return 0;
}


#define RCVBUFSIZE 32   /* Size of receive buffer */


int main(int argc, char *argv[])
{

    int sock;                        /* Socket descriptor */
    struct sockaddr_in echoServAddr; /* Echo server address */
    unsigned short echoServPort;     /* Echo server port */
    char *servIP;                    /* Server IP address (dotted quad) */
    char *echoString;                /* String to send to echo server */
    char echoBuffer[RCVBUFSIZE];     /* Buffer for echo string */
    unsigned int echoStringLen;      /* Length of string to echo */
    int bytesRcvd, totalBytesRcvd;   /* Bytes read in single recv() 
                                        and total bytes read */

    int sock2;	
    struct sockaddr_in echoServAddr2; /* Echo server address */
    unsigned short echoServPort2;     /* Echo server port */
    char *servIP2;                    /* Server IP address (dotted quad) */
    char *echoString2;                /* String to send to echo server */
    char echoBuffer2[RCVBUFSIZE];     /* Buffer for echo string */
    unsigned int echoStringLen2;      /* Length of string to echo */
    int bytesRcvd2, totalBytesRcvd2;   /* Bytes read in single recv() */

    if (argc!=7)    /* Test for correct number of arguments */
    {
       fprintf(stderr, "Usage: %s <Server IP> <outport> <inport> <n_channels> <n_points> <n_fft_points>\n",
               argv[0]);
       exit(1);
    }

    n_channels = atoi(argv[4]);	
    n_points = atoi(argv[5]);	
    n_fft_points = atoi(argv[6]);	
	
    printf("n_channels = %i, n_points = %i, n_fft_points = %i\n",n_channels,n_points,n_fft_points);
    fflush(stdout);

    servIP = argv[1];             /* First arg: server IP address (dotted quad) */
//    echoString = argv[2];         /* Second arg: string to echo */

  //  if (argc == 5)
        echoServPort = atoi(argv[2]); /* Use given port, if any */
//    else
//        echoServPort = 7;  /* 7 is the well-known port for the echo service */

    /* Create a reliable, stream socket using TCP */
    if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");

    /* Construct the server address structure */
    memset(&echoServAddr, 0, sizeof(echoServAddr));     /* Zero out structure */
    echoServAddr.sin_family      = AF_INET;             /* Internet address family */
    echoServAddr.sin_addr.s_addr = inet_addr(servIP);   /* Server IP address */
    echoServAddr.sin_port        = htons(echoServPort); /* Server port */

    /* Establish the connection to the echo server */
    if (connect(sock, (struct sockaddr *) &echoServAddr, sizeof(echoServAddr)) < 0) {
        DieWithError("connect() failed");
	
	}
    printf("output socket connected\n");
    fflush(stdout);

/// second socket
    servIP2 = argv[1];             /* First arg: server IP address (dotted quad) */
//    echoString2 = argv[2];         /* Second arg: string to echo */

 //   if (argc == 5)
        echoServPort2 = atoi(argv[3]); /* Use given port, if any */
//    else
//        echoServPort2 = 7;  /* 7 is the well-known port for the echo service */

    /* Create a reliable, stream socket using TCP */
    if ((sock2 = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");

    /* Construct the server address structure */
    memset(&echoServAddr2, 0, sizeof(echoServAddr2));     /* Zero out structure */
    echoServAddr2.sin_family      = AF_INET;             /* Internet address family */
    echoServAddr2.sin_addr.s_addr = inet_addr(servIP);   /* Server IP address */
    echoServAddr2.sin_port        = htons(echoServPort2); /* Server port */

    /* Establish the connection to the echo server */
    if (connect(sock2, (struct sockaddr *) &echoServAddr2, sizeof(echoServAddr2)) < 0) {
        DieWithError("connect() failed");
	
	}
    printf("input socket connected\n");
    fflush(stdout);	




    while (1) {
        main2(sock,sock2);
	//printf("sleep\n");
    }

    close(sock);
    exit(0);
}
/*
int main(int argc, char *argv[])
{

    n_channels = 2;	
    n_points = 30000;	
    n_fft_points = 50;	
	
    while (1) {
        main2(1,1);
    }
}*/
