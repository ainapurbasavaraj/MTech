#include <stdio.h>
#include <errno.h>
#include <sys/time.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <signal.h>
#define SA struct sockaddr
#define MAXLINE 100


void	send_all(int,int);
void mcast_join(int,char*);

char GroupIPaddress[MAXLINE];    
int  UDPport;  

int main(int argc, char **argv)
{	
	const int on = 1;
	int c_pid,n;
	char line[MAXLINE];
	struct sockaddr_in groupHost;	
	int sendfd,recvfd;			 	
	u_char loop=32;

	strcpy(GroupIPaddress,argv[1]);
	UDPport = atoi(argv[2]);

	sendfd = socket(AF_INET,SOCK_DGRAM, 0);
	recvfd = socket(AF_INET, SOCK_DGRAM, 0);
	groupHost.sin_family=AF_INET;
      groupHost.sin_port=htons(UDPport);
      groupHost.sin_addr.s_addr = htonl(INADDR_ANY);

	setsockopt(recvfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));
	bind(recvfd,(struct sockaddr *) &groupHost, sizeof(groupHost)); 
	mcast_join(recvfd,GroupIPaddress);
	setsockopt(sendfd,IPPROTO_IP,IP_MULTICAST_LOOP,(char *)&loop,sizeof(u_char));

	if ((c_pid=fork()) == 0)
	{
		for ( ; ; ) {
		   n = recvfrom(recvfd, line, MAXLINE, 0,NULL, 0);
		printf("Not Received\n"); 
		  line[n] =0;	
		   printf("from %s", line);
		}	
	}
send_all(sendfd,c_pid);	
}


void send_all(int sendfd,int childpid)
{
     char line[MAXLINE],buf[MAXLINE];	
    int i;	
    struct sockaddr_in dest,cliaddr;
    struct hostent  *hptr;

    hptr = gethostbyname("aries");
    bcopy ( hptr->h_addr, &(cliaddr.sin_addr), hptr->h_length);

    dest.sin_family = AF_INET;
    dest.sin_port =  htons(UDPport);
    dest.sin_addr.s_addr = inet_addr(GroupIPaddress);

printf("Host Address of this program is: %s\nUser id is %d\n",inet_ntoa(cliaddr.sin_addr),cliaddr.sin_port);

strcpy(buf,"SIGNING IN");	
snprintf(line,sizeof(line),"<host@%s> %s\n",inet_ntoa(cliaddr.sin_addr),buf);
sendto(sendfd, line, strlen(line), 0,(struct sockaddr *)&dest, sizeof(dest));

while(fgets(buf,MAXLINE,stdin) != NULL)
{
snprintf(line,sizeof(line),"<host@%s>%s\n",inet_ntoa(cliaddr.sin_addr),buf);
sendto(sendfd, line, strlen(line), 0,(struct sockaddr *)&dest, sizeof(dest));
}

strcpy(buf,"SIGNING OUT");
snprintf(line,sizeof(line),"<host@%s> %s\n",inet_ntoa(cliaddr.sin_addr),buf);
sendto(sendfd, line, strlen(line), 0,(struct sockaddr *)&dest, sizeof(dest));
close(sendfd);
kill(childpid,9);
exit(-1);
}

void mcast_join(int recvfd,char* group)
{
  struct ip_mreq mreq;
  struct sockaddr_in grp_struct;
  grp_struct.sin_addr.s_addr = inet_addr(group);
  mreq.imr_multiaddr = grp_struct.sin_addr;
  mreq.imr_interface.s_addr = htonl(INADDR_ANY);
 
  if(setsockopt(recvfd,IPPROTO_IP,IP_ADD_MEMBERSHIP,&mreq,sizeof(mreq)) == -1 )
  {
    printf("Error:Group cannot be joined \n");
    exit(-1);
  }
}






