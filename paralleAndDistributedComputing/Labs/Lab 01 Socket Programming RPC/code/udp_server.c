#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define BUF_SIZE 500

main (int argc, char *argv[])
{

  char buf[BUF_SIZE];
  int fd = socket (AF_INET, SOCK_DGRAM, 0);
  struct sockaddr_in servaddr, cliaddr;
  servaddr.sin_family = AF_INET;
  servaddr.sin_addr.s_addr = htonl (INADDR_ANY);
  servaddr.sin_port = htons (atoi (argv[1]));
  if (bind (fd, (struct sockaddr *) &servaddr, sizeof (servaddr)))
    {
      perror ("Bind error");
    }


      printf ("Waiting for dgrams\n");
  for (;;)
    {
      char ip[50];
      int len;
      int n =
	recvfrom (fd, buf, BUF_SIZE, 0, (struct sockaddr *) &cliaddr, &len);
      inet_ntop (AF_INET, &(cliaddr.sin_addr.s_addr), ip, sizeof (ip));
      printf ("received %s from %s", buf, ip);
      sendto (fd, buf, sizeof (buf), 0, (struct sockaddr *) &cliaddr, len);

    }





}
