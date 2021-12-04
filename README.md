# AI-Tennis Coach



**The problem** 

Tennis is a highly technical sport that requires more critical feedback than other sports. This means the effort required to improve is substantially higher than other sports. The ability to receive world-class coaching at a low price needs to be accessible for players to improve rapidly.  

**Our Alpha**

Our full stack ios app allows users to upload videos of themselves performing certain tennis strokes. The frontend was constructed using Swift, to be ios compaitable. The backend relies on an S3 bucket for storage and is primarily built using python and various database pacakages. The most difficult aspect of this project thus far has been integrating streaming into the front end and enabling the "GET" requests from the S3 bucket. We choose AWS's S3 bucket because it enabled cheap storage, and allows us to use future AWS products such as EC2 instances for future upgrades to our application. 

**The Future**

This alpha of our product is only the beginning. Once users begin using our alpha to upload themselves hitting certain shots, we will begin training a machine learning model that will offer automatic coaching to clients. Furthermore, we will develop a coach's version that allows instructors to annotate and offer remote feedback to their players. This dataset will further improve our ML model and the feedback clients receive. 

Utilizing the AWS suite of devices, we will train our model using highly scalable EC2 instances from data stored in our S3 bucket. This allows us to scale our backend with demand in a capital effective manner. 

---
Requirements for HackChallenge
---
---
ios Requirements
---
**AutoLayout using NSLayoutContraint or SnapKit**
I used NSLayoutConstraint to position all the components.

**UICollectionView or UITableView**
Used UITableView to display all the buckets for the various categories of videos.

**Navigation**
There's a push navigation controller for each bucket, and it brings the user to a screen where they can play the videos they've uploaded and upload more videos.

**Integrating with API**
I integrated with the backend API. The post and get requests aren't working as expected, but the google authentication does work.

---
Backend Requirements
----

### Deployment to Heroku

Our app is deployed to Heroku at this address: 

https://tennis-trainer.herokuapp.com/

### API Description

**POST: /api/user/authenticate/**

This route takes an encrypted Google authentication token as the request body. It then verifies the token with oauth and
decrypts it. If the user is not in the database, they are added to it. The response then contains the user's information
(such as their display name and email), as well as all their uploads.

Request:
```json
{
    "token": "{User's ID Token}"
}
```

Response:
```json
{
    "uid": "{User's local id}",
    "display_name": "{User's display name}",
    "email": "{User's email}"
    "uploads":
        [
            {
                "vid": "{video id}",
                "display_title": "{display title of video}"
                "tags": [
                    {
                        "tid": 1,
                        "name": "backhand"
                    }
                    ...
                ]
            }
            ...
        ]
}
```

**GET: /api/user/{uid}/media/**

This route gets all the uploads for a user (identified by uid). The uploads do not contain the media but rather
their vid, display title, and tags.

Request: N/A

Response:
```json
{
    "uploads": [
        {
            "vid": 1,
            "display_title": "{the new display title for the video}",
            "tags": [
                {
                    "tid": 1,
                    "name": "backhand"
                }
            ]
        }
    ]
}
```

**POST: /api/media/{vid}/update-title/**

This route updates the display title for an upload identified by vid.

Request:
```json
{
    "new_title": "{the new display title for the video}" or None (keeps display title the same)
}
```

Response:
```json
{
    "vid": "{video id}",
    "display_title": "{display title of video}",
    "tags": [
        {
            "tid": 1,
            "name": "backhand"
        }
    ]
}
```

**GET: /api/media/{vid}/**

This route gets Apple's HTTPS livestreaming (HLS) playlist from our S3 bucket for the specified vid.

Request: N/A

Reponse:
```json
{
    "url": "www.something.m3u8",
}
```

**POST: /api/media/**

This route uses form data to post a video file to the S3 bucket in Apple's HLS format for livestreaming. This works
by first uploading the video to us and then using the vincentbernat/video2hls github repo to convert the video to the
proper HLS files. These are then uploaded to the S3 bucket.

Request encoding = form-data:
```json
{
    "file": <FILEDATA>
    "filename": "backhand.mp4",
    "display_title": "Backhand Serve 12-2-2021",
    "uid": 5
}
```

Response encoding = JSON:
```json
{
    "vid": 4
}
```

**POST /api/media/{vid}/tag/**

This route adds a tag with the specified name to a video. A new tag is only created in the database if it does
not already exist.

Request:
```json
{
    "name": "backhand"
}
```

Response:
```json
{
    "vid": 1,
    "display_title": "{the new display title for the video}",
    "tags": [
        {
            "tid": 1,
            "name": "backhand"
        }
    ]
}
```

**GET /api/media/{vid}/tag/**

This route gets all the tags for a video identified with vid.

Request: N/A

Response:
```json
{
    "tags": [
        {
            "tid": 1,
            "name": "backhand"
        }
    ]
}
```

**DELETE /api/media/{vid}/tag/{tid}/**

This route deletes a tag from a video. It does not delete the tag from the database, though.

Request: N/A

Response:
```json
{
    "vid": 1,
    "display_title": "{the display title for the video}",
    "tags": []
}
```



### Database Model

Our database contains three tables: "user", "upload", and "tag". We make use of a PostgreSQL database hosted
on Heroku that we connect to. 

The user table contains an uid as the primary key, the user's google id (used for
authentication), the display name (the user's google name), and the email.

The upload table contains a vid as the primary key, a display title, a vkey (this is the video's filename, vid, and uid
hashed together that acts at its object name in our S3 bucket), and the video's related uid.

The tag table simply contains a tid as the primary key and a name.

There is a one-to-many relationship between users and uploads, and there is a many-to-many relationship
between uploads and tags.


### Third Party APIs

We made use of AWS's S3 service to host our stream files. We used a publicly available github repo
(vincentbernat/video2hls) to prepare uploaded videos for HLS streaming. These HLS streaming files were then uploaded 
to our S3 bucket.

We used Google's OAuth API to authorize sign-on tokens provided my the frontend. We then
stored these users in our database to associate uploads with them.

We integrated with Heroku's PostgreSQL to host our database.
