func<-function(x)
{
   mag2<<-mag^2
   f<<-f
        approx(f,mag2,x)$y
}


layout(matrix(c(1,2,3,4), 4, 1, byrow = TRUE))
#SETUP
   T    <- 0.2048 #time 0 -> T 
   dt   <- 1.0/5000 #s
   n    <- T/dt
   F    <- 1/dt # freq domain -F/2 -> F/2
   df   <- 1/T
   t    <- seq(0,T,by=dt)  
   freq <- 1 #Hz

#SIGNAL FUNCTION
   y     <- 10*sin(2*pi*freq*t) 

#FREQ ARRAY
   f <- 1:length(t)/T 

#FOURIER WORK
   Y     <- fft(y)
   mag   <- sqrt(Re(Y)^2+Im(Y)^2)*2/n #Amplitude
   phase <- Arg(Y)*180/pi 
   Yr    <- Re(Y)
   Yi    <- Im(Y)

#PLOT SIGNALS
   plot(t,y,type="l",xlim=c(0,T)) 
   grid(NULL,NULL, col = "lightgray", lty = "dotted",lwd = 1)
   par(mar=c(5, 4, 0, 2) + 0.1)
   
   plot(f[1:length(f)/2],phase[1:length(f)/2],type="l",xlab="Frequency,
Hz",ylab="Phase,deg")
   grid(NULL,NULL, col = "lightgray", lty = "dotted",lwd = 1)
   
   plot(f[1:length(f)/2],mag[1:length(f)/2],type="l",xlab="Frequency,
Hz",ylab="Amplitude")
   grid(NULL,NULL, col = "lightgray", lty = "dotted",lwd = 1) 
   
   plot(f[1:length(f)/2],(mag^2)[1:length(f)/2],type="l",xlab="Frequency,
Hz",ylab="Power, Amp^2",log="xy",ylim=c(10^-6,100))
        
        pref<-20E-6 #pa
        p<-integrate(func,f[1],f[length(f)/2])
   pwrDB<-10*log10(p$value/pref^2)
        cat("Area under power curve: ",p$value,"Pa ",pwrDB," dB\n")

