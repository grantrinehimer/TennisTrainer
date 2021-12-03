# TennisTrainer

## Frontend

## Backend

### API Description
=======
Our full stack ios app allows users to upload videos of themselves performing certain tennis strokes. The frontend was constructed using Swift, to be ios compaitable. The backend relies on an S3 bucket for storage and is primarily built using python and various database pacakages. The most difficult aspect of this project thus far has been integrating streaming into the front end and enabling the "GET" requests from the S3 bucket. We choose AWS's S3 bucket because it enabled cheap storage, and allows us to use future AWS products such as EC2 instances for future upgrades to our application. 

This alpha of our product is only the beginning. Once users begin using our alpha to upload themselves hitting certain shots, we will begin training a machine learning model that will offer automatic coaching to clients. Furthermore, we will develop a coache's version that allows instructors to annotate and offer remote feedback to their players. This annotated dataset will further improve our ML model and the feedback clients receive. 

