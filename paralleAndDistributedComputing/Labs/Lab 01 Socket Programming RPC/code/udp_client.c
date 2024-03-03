#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <errno.h>
#include <signal.h>

#define BUF_SIZE 500

void
handler (int signo)
{
  printf ("signal %d recved\n", signo);

}


main (int argc, char *argv[])
{
  struct sigaction disp;

  disp.sa_handler = handler;
  disp.sa_flags = 0;


  char buf[BUF_SIZE];
  int fd = socket (AF_INET, SOCK_DGRAM, 0);

//signal(SIGALRM, handler);
  sigaction (SIGALRM, &disp, NULL);

  struct sockaddr_in destaddr, senderaddr;
  destaddr.sin_family = AF_INET;
  destaddr.sin_addr.s_addr = inet_addr (argv[1]);
  destaddr.sin_port = htons (atoi (argv[2]));

  int seq = 0;
  for (;;)
    {
      char str[50];
//      scanf("%s", str);
      sprintf (str, "%d %d", seq, rand ());
      seq++;
      strcpy (buf, str);

      int retries = 0;
      int n;
    retry:
      printf ("sending %d time\n", retries);
      n = sendto (fd, buf, sizeof (buf), 0, &destaddr, sizeof (destaddr));

      printf ("sent %s %d\n", buf, n);
      if (n < 0)
	perror ("sendto");

      alarm (5);
      n = recvfrom (fd, buf, BUF_SIZE, 0, &senderaddr, sizeof (senderaddr));
      printf ("==%d\n", n);
      if (n < 0)
	{
	  perror ("recvfrom");
	  if (errno == EINTR)
	    {
	      printf ("alarm expired\n");
	      retries++;
	      if (retries >= 5)
		continue;
	      goto retry;
	    }
	  printf ("received %s %d\n", buf, n);
	  printf ("Output: %s \n", buf);

	}

    }
}
