from typing import List
from aws_cdk import(
    aws_ec2 as ec2
)

def file_to_commands(file_path):
    """Given a file path, produces a list of strings which 
    represents the commands in that shell script.

    Args:
        file_path (str): The file path to the script

    Returns:
        List[str]: The list of commands 
    """
    return open(file_path, 'r').read().splitlines()

def generate_user_data(scripts: List[str], logging: bool = True):
    """Generates the relevant user data object for the ec2 
    instance. This uses the file to commands function to 
    produce a list of command strings.

    Args:
	scripts (List(str)): List of file paths for the scripts to 
	be compiled into one user data object. The order is important.
 
        logging (bool, optional): Should the header be included which 
        makes the user data be logged with sudo access on the instance.
        Defaults to True.

    Returns:
        ec2.UserData : The user data object which can be embedded
        into the ec2 instance.
    """

    # We want to execute in bash
    bang = "#!/bin/bash -xe"

    # And log everything to /dev/console and /var/log/user-data.log
    # from https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-log-user-data/
    logging_header = "exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1"

    # Generate a list of commands from combining setup files
    combined = list(
        map(lambda f: str(open(f, 'r').read()), scripts))
    combined.insert(0, bang)

    # Inject logging header if required
    if logging:
        combined.insert(1, logging_header)

    data = "\n".join(combined)

    # Return the created user data instance
    return ec2.UserData.custom(data)
