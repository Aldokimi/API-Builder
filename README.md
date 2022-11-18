<h1 style="font-weight:normal">
  <p style="display: flex; filter: drop-shadow(2px 4px 8px #3723a1);">👩‍💻 API Builder 👩‍💻</p>
  <a href="https://github.com/Aldokimi/ABI-Builder/releases">
    <img src=https://img.shields.io/github/release/sourcerer-io/sourcerer-app.svg?colorB=58839b>
  </a>
  <a href="https://github.com/Aldokimi/ABI-Builder//blob/master/LICENSE.md">
    <img src=https://img.shields.io/github/license/sourcerer-io/sourcerer-app.svg?colorB=ff0000>
  </a>
</h1>

<h2>SWC team 🧑‍🔧 </h2>
<p> This is a team project for the subject Tools of Software <a href="https://www.elte.hu/en/">@ELTE</a>.</p>

<h2>Quick overview🤳🏼</h2>
<p>API Builder is a tool that help you generate APIs from your data!</p>
<h4>How does this work?</h4>
<ul>
    <li>You register for an account to our API Builder tool website.</li>
    <li>Then you will be able to create a project.</li>
    <li>A project is your space to create your API.</li>
    <li>Then you can upload your data or inject the data manually through the UI.</li>
    <li>Finally you will have a generated URL where you can apply requests on this URL and modify the data inside this project.</li>
    <li>The history of changes over the project will be tracked an you can go back to the data at any state of time!</li>
<ul>

<h2>How to run 🏃🏼‍♀️</h2>
<p>Currently we don't have CD system so there is no factories, but you still can run the docker.</p>
<p>So you can run the program as follows:</p>


#### Clone the project 
```bash
git clone git@github.com:Aldokimi/API-Builder.git
```

#### Build the project's API image
```bash
cd backend
docker build -t api-builder-api:latest .
```

#### Build the project's UI image
```bash
cd fronted/API-Builder-UI
docker build -t api-builder-gui:latest .
```

#### Build the whole application
```bash
docker-compose up
```

