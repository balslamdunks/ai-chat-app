# Instructions for Setup of AI Chatbot

Welcome to the AI Chatbot Repository. This project consists of a generative AI model developed through LangChain, Azure, and Chainlit/Streamlit for the interface. The purpose of this project is to operate as a privately hosted LLM which has been trained on certain course data and can answer questions about course data/whatever data specified. This document will encompass how to set this up properly.

**Please Note:** This repository in terms of Azure deployment is forked from Coding-Crashkurse's [repo](https://github.com/Coding-Crashkurse/LangChain-On-Azure/commits?author=Coding-Crashkurse)  on LangChain in Azure deployment. 

The setup here can be found in their [video](https://www.youtube.com/watch?v=WAedZvSDZAI).

# Prerequisites

You will need to have some prerequisite elements setup for this project.

 1. Ensure you have python3.7 or above set up in your local environment along with any dependencies such as pip.
 2. Set up an Azure account, you can usually get a free 200 dollar credit for Azure when initially signing up.
 3. For the LLM, this project utilizes OpenAI, if you want to also utilize that you will need to have an enterprise OpenAI account and grab an API key to set up for this project. Instructions can be found [here](https://platform.openai.com/docs/quickstart?context=python)
 4. This code utilizes the files under Data, due to the sensitive nature of the course-based data, those files have not been included under here but instead a sample text file is included. Feel free to add your own files that you would like to use and store in AI Search. 
 5. Install [Docker](https://www.docker.com/get-started/)
 6. **Optional**: I would also recommend using pyenv to easily switch between python versions in case you come across some limitations with your current version.

## High Level Diagram of Setup

![Alt text](diagrams/cloud_representation.drawio.png?raw=true "High Level Overview")

## Local Environment Setup
1. Clone the repo `git clone github.com:balslamdunks/ai-chat-app.gi` somewhere on your local machine.
2. Navigate to the base directory.
3. I would recommend creating a virtual environment to ensure isolated behavior and setup, to do so run:
```
pip install virtualenv
python3 -m venv name_of_your_venv
source name_of_your_venv/bin/activate
```
4. Once inside your virtualenv, you can run
`python3 -m pip install -r requirements.txt` to setup dependencies.

**Note:** If you have the m1 chip or have certain versioning issues you might need to install further packages than specified for local setup.
For instance if you get the error:
`ModuleNotFoundError: No module named 'azure-search'` you may need to manually install this module for local behavior `python3 -m pip install azure-search`, this would not be needed in the docker implementation, however.

## Pipeline Setup
For these steps I would highly recommend watching [Coding Craschourses video](https://www.youtube.com/watch?v=WAedZvSDZAI) on Azure setup but I will go ahead and include them here as well.


### Azure Resource Group Setup
Navigate to Azure UI and create a Resource Group
- Click on Create a resource group
- Write in the name for the resource group you would like to create. **Example:  langchainResourceGroup**
- Fill in the Region, ensuring it is one within your area, be consistent about this region selection across all Azure Services.
- Select **Review + create** and create the resource group.
### Azure Storage Account Setup

Create an Azure Storage Account.
- For the Resource group select the resource created in previous step (langchainResourceGroup)
- Input a name of your choice in Storage Account name (**Example: langchainstoragegroup**)
- For Region select the same region you selected for Resource Group
- Create the storage account.
-	Create a container within the Storage Account you created.
- Select on + Container under the Containers section in your Storage Account
- Name your container however you would like (**example:  langchaincontainer**)
- Select Private access to ensure it is secure
### Upload Dataset to Azure Storage Account
Navigate back to your code, to **blob.py**
- Change the variables **container_name** and **blob_name** to what you named your associate Azure services. 
- For **connection_string** navigate to **Access Keys** under your storage account, click the Copy icon under key1 or key2 of the **Connection String** field.
- Once those fields are inputted run the command `python3 blob.py` this will upload the files you have under Data to the storage account you created in Azure.
### Create Azure Cognitive Search Vector Store
Now create the Azure Cognitive Search (AKA AI Search) service to embed the data you just uplaoded into a vector database,
	- Navigate to Azure Cognitive Search and select **Create**
	- Select the same resource group you created previously
	- Enter in a service name of your preference (**example: langchaincognitivesearch**)
	- Choose the same location you have been selecting before.
	- Switch from Standard to Free Pricing Tier if this is simply for experimentation purposes.
	- Create the Cognitive Search Service
### Setup Your Local Environment Variables
Create a .env file with all of the required keys. 
- The OPENAI_API_KEY is taken from the pre-requisite step.
- The AZURE_COGNITIVE_SEARCH_SERVICE_NAME is what you called the service (**langchaincognitivesearch**)
 - The AZURE_COGNITIVE_SEARCH_INDEX_NAME should match what is shown in **azurecognitive_search.py**
- The AZURE_COGNITIVE_SEARCH_API_KEY can be grabbed from the **Keys** section of the Azure Cognitive Search service
- The AZURE_CONN_STRING is the same variable we grabbed for **connection_string**
 - The CONTAINER_NAME is what we named our initial container (**langchaincontainer**)
### Split Blob Files and Embed + Add to Cognitive Search
In the **azurecognitive_search.py** code, the blob-based data is embedded and then uploaded to the vector store DB we just created.
- After setting up the .env file you can run **python3 azurecognitive_search.py** this should split your blob data and embed and store it into the vector database.
- You can validate this by navigating to the Index you created in the Azure Cognitive Search UI and searching for some text you know is in your dataset.
### Docker Setup
The **application_chainlit.py** code contains the chainlit-based code with the LangChjain implementation, the **application_streamlit.py** file contains the streamlit variation. The Dockerfile is currently set up to deploy the chainlit version, but the streamlit command can be commented in and the chainlit commented out if the streamlit alternative is preferred.

- Create a Container Registry in Azure, navigate to **Container Registry** and click **Create****strong text**
- Use the same resource group you created before.
- Input Name for your registry (**example: chainlitregistry**) 
- Select same Location as always
- Switch SKU from Standard to Basic for sake of demo.
- Navigate to the Access Keys Section, select **Enabled** for the admin user,  copy down the **username** and **password** values as well as the Login Server URL (**example: chainlitregistry.azurecr.io**) 
- In your local environment, ensure Docker is running 
```docker ps```
- Log in to the docker registry you just createde `docker login chainlitregistry.azurecr.io --username USERNAME --password PASSWORD `
- Build your docker file:
	- Standard way `docker build -t chainlitregistry.azurecr.io/app:v1  .`
	- **NOTE** if you have an M1 Mac you might need to transpile your docker build do this by running: `docker buildx build --platform=linux/amd64 -t chainlitregistry.azurecr.io/app:v1  . `
- Now push that dockerfile onto the Container Registry
	- `docker push chainlitregistry.azurecr.io/app:v1`

### Web App Setup
- Navigate to **App Services** in the Azure UI, Create Web App
- Use the same resource group as before
- Create a name for your Web App (**example: AICourseBot**)
	- Select Docker Container for Publish and Linux for Operating System
	- Select the same Region as before
	- Select Free Pricing Plan
- Navigate to the **Docker** tab
	- Select Single Container for Options
	- Select Azure Container Registry for Image Source
	- It should auto-fill the Image and Tag options
- Select **Review + create** and **Create**
- Navigate to your created web app.
- Navigate to the **Configuration** Section
	- Under **Application Settings** 
		- Add the environment variables, this is what the env.json value is for, place the variables in your .env file in that env.json file, append the json values to the already existing Application Settings.
		- Add another application setting called **WEBSITE_PORT** set the value equal to 80 to match your Dockerfile port
		- **Optional** Add variable called WEBSITES_CONTAINER_START_TIME_LIMIT and set it equal to 1800 to prevent timeout errors.
	- Under **General Settings** select **On** for **Always On** this helps with timeout errors.

## Currently Available Apps at Time of Upload:
- [Streamlit](courselangchain.azurewebsites.net)
- [Chainlit](https://aicoursebot.azurewebsites.net/)
	
	