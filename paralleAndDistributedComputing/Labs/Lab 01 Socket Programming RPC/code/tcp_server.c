#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>
#include <signal.h>

void
handler (int signo)
{

  while (waitpid (-1, NULL, WNOHANG) > 0);

}


main (int argc, char *argv[])
{
  int sd, psd;
  struct sockaddr_in name, client;
  char buf[1024], *ipaddress;
  int cc, clilen;
  clilen = sizeof (client);


  signal (SIGCHLD, handler);

  sd = socket (AF_INET, SOCK_STREAM, 0);
  name.sin_family = AF_INET;
  name.sin_addr.s_addr = htonl (INADDR_ANY);
  name.sin_port = htons (atoi (argv[1]));

  int ret = bind (sd, (struct sockaddr *) &name, sizeof (name));
  if (ret < 0)
    {
      perror ("bind");
      exit (-1);
    }
  listen (sd, 1);
  for (;;)
    {
      psd = accept (sd, (struct sockaddr *) &client, &clilen);
      //ipaddress=inet_ntop(AF_INET,&client.sin_addr, ipaddress, clilen);
      //ipaddress=inet_ntoa(client.sin_addr);
      //printf("client address :%s\n",ipaddress);

      if (fork () == 0)
	{


	  for (;;)
	    {
	      cc = recv (psd, buf, sizeof (buf), 0);
	      if (cc == 0)
		exit (0);
	      buf[cc] = '\0';
	      printf ("message received: %s\n", buf);
	      int p[2];
	      pipe (p);
	      if (fork () == 0)
		{
		  close (1);
		  //dup (p[1]);
		  dup (psd);
		  char cmd[100];
		  sprintf (cmd, "/bin/sh -c %s", buf);
		  printf ("command:%s\n", cmd);
		  execl ("/bin/sh", "sh", "-c", buf, NULL);
		  perror ("execl");
		  printf ("after exec\n");
		}
	      close (p[1]);
//	      while ((cc = read (p[0], buf, 100)) > 0)
//		{
//		  write (psd, buf, cc);
		  //      buf[cc]='\0';
//		  printf ("data size: %d\n", cc);
//		  printf ("data sent: %s\n", buf);
//		}
	      printf ("sending data complete\n");
	      exit (0);
	    }



	}

      close (psd);

    }
}
