# XÂY DỰNG CHATBOT HỖ TRỢ HỌC LỊCH SỬ VIỆT NAM

# BUILDING A SUPPORT CHATBOT FOR LEARNING VIETNAMESE HISTORY

# I. Introduction

# II. How to run

Step 1: Clone this repository

```
https://github.com/ngovanuc/Vietnamese_History_Chatbot.git
```

Step 2: You must have your LLM api keys

Go to LLM service providers and generate api key, and then insert them in to: `src/llms/...`

Step 3: Install libraries needed

- Create a python virtual enviroment (see more: https://docs.python.org/3/library/venv.html)
- Activate your virtual enviroment
- Install libraries:

  ```
  pip install -r requirements.txt
  ```

  or

  ```
  pip install -r requirements_copy.txt
  ```

Step 4: Make sure you have

* Docker
* MongoDB

Step 5: If you want to sign-up or login with Google/Github account

Generate these token and insert to ***.env*** file:

* OAUTH_GITHUB_CLIENT_ID
* OAUTH_GITHUB_CLIENT_SECRET
* OAUTH_GOOGLE_CLIENT_ID
* OAUTH_GOOGLE_CLIENT_SECRET

Step 6: You also need to generate CHAINLIT_AUTH_SECRET token

Run this in terminal:

```
chainlit create-secret
```

Then copy token and insert to ***.env*** file

Step 7: Open 3 terminal and activate virtual enviroment

Run these:

* Run docker

  ```
  docker compose up
  ```
* For chainlit datalayer. See more at: https://github.com/Chainlit/chainlit-datalayer and https://docs.chainlit.io/data-layers/official

  ```
  npx prisma studio
  ```
* Run app

  ```
  chainlit run app.py -w
  ```

Oke finish!

There are many things to do to run this project successfuly but I'm lazy. If you have any question, let's contact to me! 🛌😴
