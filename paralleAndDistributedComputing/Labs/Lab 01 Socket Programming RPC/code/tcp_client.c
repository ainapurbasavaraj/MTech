#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>
#define BUF_SIZE 100
main (int argc, char **argv)
{
  int sd;
	char buf[BUF_SIZE];
  struct sockaddr_in server;


  server.sin_family = AF_INET;
  server.sin_addr.s_addr = inet_addr (argv[1]);
  //inet_aton(argv[1],&server.sin_addr);
  //inet_pton(AF_INET, argv[1], &server.sin_addr);
  server.sin_port = htons (atoi (argv[2]));


  for (;;)
    {
  sd = socket (AF_INET, SOCK_STREAM, 0);
  int ret = connect (sd, (struct sockaddr *) &server, sizeof (server));
  if (ret < 0)
    {
      perror ("connect");
      exit (-1);
    }
      fgets(buf, BUF_SIZE, stdin);	
      send (sd, buf, sizeof(buf), 0);
      int n;
	while((n=recv(sd, buf, BUF_SIZE,0))>0){
	buf[n]='\0';
      printf("Output:\n%s", buf);
	}
      printf("Reciceived all data\n");
      //sleep (2);
    }
}
