# ImmunoPoli

 ImmunoPoli is an information system for managing pandemic information for a given country. 
 The main need to address is to trace contacts between people and to monitor the viral diffusion. 
 It is developed a graph data structure in a NoSQL DB (Neo4j) for supporting the contact tracing application for COVID-19.

## Index

- Group components
- Enviroment setup 
- Database Generator
- GUI 

## Group Components

| Cognome | Nome | e-mail | Matricola | Codice Persona
| ------ | ------ |----- |----- |----- |
| Musumeci | Margherita| margherita.musumeci@mail.polimi.it| 907435| 10600069
| Nunziante |  Matteo| matteo.nunziante@mail.polimi.it | 992518 | 10670132
| Rendina |Piero | piero.rendina@mail.polimi.it  | 991437 | 10629696
| Sanchini |  Andrea | andrea.sanchini@mail.polimi.it | 992072 | 10675541 | 
| Zuccolotto |Enrico | enrico.zuccolotto@mail.polimi.it  | 993209 | 10666354

## Environment Setup

Download the setup file, navigate to the folder with the setup file and execute the following command:  

```sh
pip install -r config_environment.txt
```

## Database Generator

The dataset is drawn from a random generator. It allows enforcing parameterssuch as the number of visits, tests, covid vaccinations, families and the proba-bility of being positive.

To generete a new dataset on Neo4j Aura type the following command in the terminal:

```sh
pyhton3 DataBaseGenerator.py
```

## GUI 

The Graphical User Interface is made with Tkinter library.

To start the application type the following command in the terminal:

```sh
pyhton3 App/Index.py

```
![front page](App/Images/index.png?raw=true)

The App Manager can:
- add new covid test results
- perform queries to the database 
- see common trends

The Location Manager can:
- register a person that is visiting his location on the current day

The User can:
- visualize his personal information 
- modify some of his personal information 
- visualize his green pass
- visualize covid alerts 
- visualize the list of palaces he visited


