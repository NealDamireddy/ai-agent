import requests
import json
import base64
from smolagents import tool
def get_repo_metadata(owner: str, repo: str) -> dict:
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}" #Url of the specific repository we want to reach
        response = requests.get(url)
        response.raise_for_status() #confirms that the status is correct
        data = response.json()  #turns the json imported by the response into python objects
        name = data["name"]
        branch = data["default_branch"]
        language = data["language"]
        description = data["description"]
        return {
            "name": name,
            "description": description,
            "branch": branch,
            "language": language
        }
    except requests.exceptions.RequestException as e:
        print(f"error occured when handling request {e}") #if there is an error retrieving the data then it will go to this. This is for the agent to knoow that there was an error rather than it just glossing over it
        raise
def list_repo_files(owner: str, repo: str, path: str = "") -> list[dict]:
    files = []
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        data = response.json()
        for item in data:
            files.append({
                "name" : item["name"],
                "path" : item["path"],
                "type" : item["type"]
            })
        return files
    except requests.exceptions.RequestException as e:
         print(f"error occured when handling request {e}") #if there is an error retrieving the data then it will go to this. This is for the agent to knoow that there was an error rather than it just glossing over it
         raise
def read_repo_code(owner: str, repo: str, path: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        data = response.json()
        code = base64.b64decode(data["content"]) #extracting the content from the data which is encoded in Base64
        return code.decode(encoding = "UTF-8") #return text so the tool wrapper can JSON encode it
    except requests.exceptions.RequestException as e:
        print(f"error occured when handling request {e}") #if there is an error retrieving the data then it will go to this. This is for the agent to knoow that there was an error rather than it just glossing over it
        raise
@tool
def github_metadata(owner: str, repo: str) -> str:
    """ The goal of this tool is to retrieve the repo metadata in a dictionary format. you are to use this when you want to get different types of information outlined in the output
        Args:
            owner: This is a string that represents the name of the owner of the repo
            repo: this is a string that represents the name of the repo
        Returns:
            this returns a JSON formatted string with the following info for the repository: the name of the repository, description, branch, and language
        """
    output = json.dumps(get_repo_metadata(owner, repo))
    return output
@tool #for tools you need to define in text what it does, inputs needed, what it returns. When the tool class parses through it creates a specific tool object for this.
def github_repo_files(owner: str, repo: str, path:str = "") -> str:
    """this is a tool that functions to retrieve a list of the files of the repository
    Args:
        owner: string that is the owner of the repo
        repo : string that is the name of the repo
        path: this is the path to get to the repo
    Returns:
        this outputs a JSON formatted string that contains the following:  for each file in the repo, the path to this file, the name of the file, and the file type """
    repo_files_json = json.dumps(list_repo_files(owner, repo, path))
    return repo_files_json
@tool
def github_repo_code(owner: str, repo: str, path : str) -> str:
    """ the premise of this function is to get the code of a specific file in a repository
    Args:
        owner : the owner of the repository
        repo : name of the repository used
        path : the path to the specific file in the repository
    Returns:
        a JSON formatted string of the code used in the requested file
    """
    repo_code = json.dumps(read_repo_code(owner, repo, path)) #for the toolcallingagent we have to condense it to a json string
    return repo_code
