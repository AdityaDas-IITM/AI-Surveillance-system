# AI-Surveillance-System
This is a project which builds an AI based model to detect crime using a surveillance camera.
For this project we have implemented the following CVPR 2018 research paper:
[Link](https://openaccess.thecvf.com/content_cvpr_2018/papers/Sultani_Real-World_Anomaly_Detection_CVPR_2018_paper.pdf)

We have built a Deep Learning based 3D convolutional network which takes in a video feed and gives out a score corresponding to whether or not there is an occurence of an anomaly (in our case theft or assault). The scripts used for training are given here: [Scripts](scripts/)

The trained models and weights can be found here: [Models](models/)

The scripts to design the app on Dash can be found here: [App Scripts](app/)

Videos which were marked as an anomaly by the model can be found here: [Anomalous videos](app_uploaded_files/)
