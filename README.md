# ImmunoPoli

 ImmunoPoli is an information system for managing pandemic information for a given country. 
 The main need to address is to trace contacts between people and to monitor the viral diffusion. 
 It is developed a graph data structure in a NoSQL DB (Neo4j) for supporting the contact tracing application for COVID-19.

## Index

- Group components
- Environment setup 
- Database Generator
  - Neo4j Aura
- GUI
  - Application Login
  - Tests

## Group Components

| Cognome | Nome | e-mail | Matricola | Codice Persona
| ------ | ------ |----- |----- |----- |
| Musumeci | Margherita| margherita.musumeci@mail.polimi.it| 991549| 10600069
| Nunziante |  Matteo| matteo.nunziante@mail.polimi.it | 992518 | 10670132
| Rendina |Piero | piero.rendina@mail.polimi.it  | 991437 | 10629696
| Sanchini |  Andrea | andrea.sanchini@mail.polimi.it | 992072 | 10675541 | 
| Zuccolotto |Enrico | enrico.zuccolotto@mail.polimi.it  | 993209 | 10666354

## Environment Setup

To run the application, all the libraries contained in the following file must be installed:  

```sh
 libraries.txt
```

If any of them is missing it can be installed by typing this command in the terminal:

```sh
 pip install -r libraries.txt
```

## Database Generator

The dataset is drawn from a random generator. It allows enforcing parameters such as the number of visits, tests, COVID-19 vaccinations, families and the probability of being positive.

To generate a new dataset on Neo4j Aura type the following command in the terminal:

```sh
python3 DataBaseGenerator.py
```

### Neo4j Aura 

Credentials for access to the remote Database are the following:

URI 

```sh
neo4j+s://057f4a80.databases.neo4j.io
```
USER 

```sh
neo4j
```

PASSWORD 
```sh
cJhfqi7RhIHR4I8ocQtc5pFPSEhIHDVJBCps3ULNzbA
```

## GUI 

The Graphical User Interface is made with Tkinter library.

To start the application type the following command in the terminal:

```sh
pyhton3 App/Index.py
```
![front page](App/Images/index.png?raw=true)

The App Manager can:
- add new COVID-19 test results
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

### Application Login 
To access the application the IDs are needed. Here there is the list of some IDs to sign in.
Other IDs can be retrieved by looking for them as Person ID inside the Neo4j database.
<div style="text-align: center;">

| App Manager/User | Location Manager
| ---------------- | --------------- |
|    4027          |      4590            
|    4058          |      4560
|    4084          |      4551
|    4307          |      4623
|    3951          |      4592
|    4045          |      4588

</div>

### Tests 
To add a new covid test result the test IDs are needed. Here there is the list of the IDs to use.
<div style="text-align: center;">

| Test Name        | Test ID 
| ---------------- | --------------- |
|   Rapid          |    4653         |
|   Molecular      |    4654         |   
|   PCR            |    4655         |
|   Antibody       |    4656         |

</div>
