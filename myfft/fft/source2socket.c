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


struct sockaddr_in serv_addr;



int main2(int sockfd)
{
        cufftHandle plan;
        cufftComplex *devPtr;
        cufftReal indata[NX*BATCH];
        cufftComplex data[NX*BATCH];
        int i,timer,j,k;
        char fname[15];
        FILE *f;
	#define BUFSIZE (21*4096*sizeof(int))
	int buffer[BUFSIZE];

        int p,nread;


	f = fopen("21-4096","rb");
	nread=fread(buffer,BUFSIZE,1,f);
	printf("nread=%i\n",nread);
	fclose(f);

        i=0;
        for (j=0;j<BATCH;j++) {
            for (k=0;k<NX;k++) {
                data[j*NX+k].x = buffer[j*NX+k];
                data[j*NX+k].y = 0;
            }
	}


        //f=fopen("y.txt","r");
    /* source data creation */

        //int sockfd = myconnect();
        //printf("connected\n");
	
		

        /* WORKING!!!!!!!!
        i=0;
        for (j=0;j<BATCH;j++) {
            sprintf(fname,"%i.txt",j);
            printf("%s\n",fname);
            f = fopen(fname,"r");
            for (k=0;k<NX;k++) {
                fscanf(f,"%i\n",&p);
                data[j*NX+k].x = p;
                data[j*NX+k].y = 0;
            }
            fclose(f);
	*/
/*
        for(i=  0 ; i < NX*BATCH ; i++){
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
        cufftPlan1d(&plan, NX, CUFFT_C2C, BATCH);


        /*
        cutCreateTimer(&timer);
        cutResetTimer(timer);
        cutStartTimer(timer);
        */
        
    /* GPU memory allocation */
        cudaMalloc((void**)&devPtr, sizeof(cufftComplex)*NX*BATCH);

    /* transfer to GPU memory */
        cudaMemcpy(devPtr, data, sizeof(cufftComplex)*NX*BATCH, cudaMemcpyHostToDevice);


        /* executes FFT processes */
        cufftExecC2C(plan, devPtr, devPtr, CUFFT_FORWARD);

        /* executes FFT processes (inverse transformation) */
       //cufftExecC2C(plan, devPtr, devPtr, CUFFT_INVERSE);

    /* transfer results from GPU memory */
        cudaMemcpy(data, devPtr, sizeof(cufftComplex)*NX*BATCH, cudaMemcpyDeviceToHost);

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
        for(i = 0 ; i < NX*BATCH ; i++){
                //printf("data[%d] %f %f\n", i, data[i].x, data[i].y);
                //printf("%f\n", data[i].x);
                mag = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/NX;
                printf("%f\n",mag);

        }
        */

/*
        // save as text file
        float mag;
        i=0;
        for (j=0;j<BATCH;j++) {
            sprintf(fname,"%i-mag.txt",j);
            printf("%s\n",fname);
            f = fopen(fname,"w");
            for (k=0;k<NX;k++) {
                //fscanf(f,"%i\n",&p);
                if (k>50)
                    continue;
                i = j*NX+k;
                mag = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/NX;
                fprintf(f,"%f\n",mag);
            }
            fclose(f);
        }
*/


        float mag;
        i=0;
        float mags[NX];
        int magsint[NX*BATCH];
        memset(magsint,0,sizeof(int)*NX*BATCH);
        int u = 0;

        printf("%f %f %f %f\n",data[0].x,data[1].x,data[2].x,data[3].x);

        //printf("%i %i %i %i\n",magsint[0],magsint[1],magsint[2],magsint[3]);

//        f = fopen("ffts.bin","wb");
        for (j=0;j<BATCH;j++) {
//            sprintf(fname,"%i-bin.dat",j);
//            printf("%s\n",fname);

            for (k=0;k<NX;k++) {
                //fscanf(f,"%i\n",&p);
                if (k>50)
                    continue;
                i = j*NX+k;
                mags[k] = sqrtf(data[i].x*data[i].x+data[i].y*data[i].y)*2.0/NX;
                magsint[u]=mags[k]    ;
                u++;
                //fprintf(f,"%f\n",mag);
                
            }

            //f = fopen(fname,"wb");
  //          fwrite(magsint,sizeof(int)*50,1,f);
        }
        int n;
        n = write(sockfd,magsint,sizeof(int)*BATCH*50);
        printf("%i %i %i %i\n",magsint[0],magsint[1],magsint[2],magsint[3]);
        printf("send ok, size: %i\n",n);
        //fclose(f);
        
        
        return 0;
}


#define RCVBUFSIZE 32   /* Size of receive buffer */

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(1);
}

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

    if ((argc < 3) || (argc > 4))    /* Test for correct number of arguments */
    {
       fprintf(stderr, "Usage: %s <Server IP> <Echo Word> [<Echo Port>]\n",
               argv[0]);
       exit(1);
    }

    servIP = argv[1];             /* First arg: server IP address (dotted quad) */
    echoString = argv[2];         /* Second arg: string to echo */

    if (argc == 4)
        echoServPort = atoi(argv[3]); /* Use given port, if any */
    else
        echoServPort = 7;  /* 7 is the well-known port for the echo service */

    /* Create a reliable, stream socket using TCP */
    if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");

    /* Construct the server address structure */
    memset(&echoServAddr, 0, sizeof(echoServAddr));     /* Zero out structure */
    echoServAddr.sin_family      = AF_INET;             /* Internet address family */
    echoServAddr.sin_addr.s_addr = inet_addr(servIP);   /* Server IP address */
    echoServAddr.sin_port        = htons(echoServPort); /* Server port */

    /* Establish the connection to the echo server */
    if (connect(sock, (struct sockaddr *) &echoServAddr, sizeof(echoServAddr)) < 0)
        DieWithError("connect() failed");

    while (1) {
        main2(sock);
	printf("sleep\n");
	sleep(1);
    }

    close(sock);
    exit(0);
}

