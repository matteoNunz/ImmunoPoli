# ImmunoPoli

 ImmunoPoli is an information system for managing pandemic information for a given country. 
 The main need to address is to trace contacts between people and to monitor the viral diffusion. 
 It is developed a graph data structure in a NoSQL DB (Neo4j) for supporting the contact tracing application for COVID-19.

## Index

- Group components
- Database Generator
- GUI application 

## Group Components

| Cognome | Nome | e-mail | Matricola | Codice Persona
| ------ | ------ |----- |----- |----- |
| Musumeci | Margherita| margherita.musumeci@mail.polimi.it| 907435| 10600069
| Nunziante |  Matteo| matteo.nunziante@mail.polimi.it | 913670 | 10670132
| Rendina |Piero | piero.rendina@mail.polimi.it  || 
| Sanchini |  Andrea | andrea.sanchini@mail.polimi.it |  | 
| Zuccolotto |Enrico | enrico.zuccolotto@mail.polimi.it  |  | 

## Database Generator


```sh
pyhton3 DataBaseGenerator.py
```

## GUI 

The Graphical User Interface is made with Tkinter library 

```sh
pyhton3 Index.py
```
![front page](https://github.com/matteoNunz/ImmunoPoli/App/Images/index.png?raw=true)
