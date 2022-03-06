#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:03:54 2022

@author: jaime
"""



from multiprocessing import Process, BoundedSemaphore, Manager, Lock
import random

iterations = 5
N = 3
a=1
b=1000

def productor(a,b):
    result = [None]*(iterations+1)
    result[0] = random.randint(a,b)
    for i in range(iterations-1):
        result[i+1] = result[i] + random.randint(a,b)
    result[-1] = -1
    return result

def producer(pid, buffer, running, empty, non_empty, lock): # cada productor produce de uno en uno
	for i in range(iterations):
		empty[pid].acquire()
		
		lock.acquire()
		buffer[pid] += random.randint(a, b)
		lock.release()
		
		non_empty[pid].release()
		print(f"Producido {pid}")
	buffer[pid] = -1

def minimo(l):
    result = max(l)
    for i in l:
        if i==-1:
            pass
        elif i<result:
            result=i
    return (result,l.index(result))


def taskproductor(lock,semaforo,almacen,numeros,tid):
    for i in range(iterations+1):
        lock.acquire()
        almacen[tid] = numeros[i]
        print(f"Producido {numeros[i]} en proceso {tid}")
        semaforo.release()
        

def taskmerger(locks,semaforos,almacen,merged_numeros):
    running = True
    while running:
        for j in range(N):
            semaforos[j].acquire()
        (a,pos) = minimo(almacen)
        if a != -1:
            merged_numeros.append(a)
            print("Producción merge originada desde el proceso ",pos,':',a)
        else:
            running = False
        for j in range(N):
            if j == pos:
                locks[j].release()
            else:
                semaforos[j].release()

    

def main():
    lp = []
    manager = Manager()
    almacen = manager.list() #el manager con el almacen sustituye al consumidor
    locks = [None]*N
    semaforos = [None]*N
    for i in range(N):
        almacen.append(-1)
        locks[i] = Lock()
        semaforos[i] = BoundedSemaphore(1)
        semaforos[i].acquire()
       	prod = productor(a,b)
       	print(i,":",prod)
        lp.append(Process(target=taskproductor, 
                args = (locks[i],semaforos[i],almacen,prod,i)))
    result = manager.list()
    lp.append(Process(target=taskmerger, args=(locks,semaforos,almacen,result)))
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print('Resultado final',result)

if __name__ == '__main__':
    main()