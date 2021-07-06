#!/usr/bin/python3

import cgi
import subprocess
import re

print("content-type: text/html")
print()

stop_words={'name', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}

f = cgi.FieldStorage()
y = f.getvalue("transcript")
query = []

radio = f.getvalue("radio")

def createcmd(y):
    if ('get' in y or 'show' in y or 'display' in y) and ('po' in y or 'pod' in y or 'pods' in y):
        cmd = "kubectl get pods"
   
    elif ('get'  in y or 'show' in y or 'display' in y) and ('deployments'  in y or 'deployment' in y or 'deploy' in y):
        cmd = "kubectl get deployments"
    
    elif ('get'  in y or 'show'  in y or 'display' in y) and ('svc'  in y or 'service' in y):
        cmd = "kubectl get svc"

    elif ('delete' in y or 'del' in y ) and ( 'all' in y or 'everything' in y):
        cmd = "kubectl delete all --all"
        
    elif ('create' in y or 'run' in y or 'expose' in y or 'delete' in y or 'del' in y or 'remove' in y or 'scale' in y):
        lst = y.split()
        for w in lst:
            if w not in stop_words:
                query.append(w)

        for i in query:
            if (i == 'create' or i == 'run'):
                query.remove(i)
                for j in query:
                    if (j == 'pod' or j == 'po' or j == 'pods'):
                        query.remove(j)
                        if len(query) == 0:
                            cmd = "kubectl run pod --image="+radio
                        else:
                            cmd = "kubectl run "+query[0]+" --image="+radio
                    elif (j == 'deploy' or j == 'deployment' or j == 'deployments'):
                        query.remove(j)
                        if len(query) == 0:
                            cmd = "kubectl create deployment dep --image="+radio
                        else:
                            cmd = "kubectl create deployment "+query[0]+" --image="+radio

            
            elif (i == 'delete' or i == 'del' or i == 'remove'):
                query.remove(i)
                for j in query:
                    if (j == 'pod' or j == 'po' or j == 'pods'):
                        query.remove(j)
                        if len(query) == 0:
                            cmd = "echo 'specify name of pod also'"
                        else:
                            cmd = "kubectl delete pod "+query[0]
                    elif (j == 'deploy' or j == 'deployment' or j == 'deployments'):
                        query.remove(j)
                        if len(query) == 0:
                            cmd = "echo 'specify name of deployment also'"
                        else:
                            cmd = "kubectl delete deployment "+query[0]
            elif (i == 'scale'):
                query.remove(i)
                for j in query:
                    if (j == 'deploy' or j == 'deployment' or j == 'deployments'):
                      query.remove(j)
                      if len(query) == 0:
                          cmd = "echo '0 .specify name of deployment & number of replicas also'"
                      elif len(query) == 1:
                          cmd = "echo '1 .specify name of deployment & number of replicas also'"
                      elif len(query) == 2:
                          
                          z = " ".join(query)
                          r1 = re.findall(r"\d",z)
                          r2 = re.findall(r"[0-9-a-z_A-Z]+",z)
                          name = max(r2)
                          count = int(r1[0])
                          cmd = "kubectl scale deployment {} --replicas={}".format(name, count)
                          break
                      else:
                          cmd = "echo 'enter a simpler statement...'"
                          break
                    else:
                      cmd = "echo 'wrong command'"
    
            elif (i == 'expose'):
                query.remove(i)
                for j in query:
                    if (j == 'deploy' or j == 'deployment' or j == 'deployments'):
                      query.remove(j)
                      if len(query) == 0:
                          cmd = "echo '0 .specify name of deployment & port number also'"
                      elif len(query) == 1:
                          cmd = "echo '1 .specify name of deployment & port number also'"
                      elif len(query) == 2:
                          z = " ".join(query)
                          r1 = re.findall(r"\d",z)
                          r2 = re.findall(r"[0-9-a-z_A-Z]+",z)
                          name = max(r2)
                          port = int(r1[0])
                          cmd = "kubectl expose deployment {} --port={} --type=NodePort".format(name, port)
                          break
                      else:
                          cmd = "echo 'enter a simpler statement...'"
                          break
                    else:
                      cmd = "echo 'wrong command'"
    else:
        cmd = "echo 'please try again with correct command.'"
    return(cmd)

c = createcmd(y)
print(c)
