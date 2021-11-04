# ImmunoPoli

 ImmunoPoli is an information system for managing pandemic information for a given country. 
 The main need to address is to trace contacts between people and to monitor the viral diffusion. 
 It is developed a graph data structure in a NoSQL DB (Neo4j) for supporting the contact tracing application for COVID-19.

## Index

- Group components
- Database Generator
- GUI 

## Group Components

| Cognome | Nome | e-mail | Matricola | Codice Persona
| ------ | ------ |----- |----- |----- |
| Musumeci | Margherita| margherita.musumeci@mail.polimi.it| 907435| 10600069
| Nunziante |  Matteo| matteo.nunziante@mail.polimi.it | 913670 | 10670132
| Rendina |Piero | piero.rendina@mail.polimi.it  || 
| Sanchini |  Andrea | andrea.sanchini@mail.polimi.it |  | 
| Zuccolotto |Enrico | enrico.zuccolotto@mail.polimi.it  | 993209 | 10666354

## Database Generator


```sh
pyhton3 DataBaseGenerator.py
```

## GUI 

The Graphical User Interface is made with Tkinter library 

```sh
pyhton3 Index.py
```
![front page](App/Images/index.png?raw=true)
A customer can log in as a "User" or an "App Manager" with his personal and secrete ID.

The User can:
- visualize his personal information 
- modify some of his personal information 
- visualize his green pass
- visualize covid alerts 
- visualize the list of palaces he visited in the last ten days 

The App Manager can:
- add new covid test results
- perform queries to the database 
- see common trends 
