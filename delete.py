import shutil
import os

def delete_folder(folder_name):
    try:
        # Check if the folder exists
        if os.path.exists(folder_name):
            # Remove the folder and its contents recursively
            shutil.rmtree(folder_name)
            print(f"The folder '{folder_name}' has been successfully deleted.")
        else:
            print(f"The folder '{folder_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the folder '{folder_name}': {str(e)}")

# Example usage
folder_name = input("Enter the folder name to delete: ")
opt = input("Are you sure you want to delete the folder " + "'" +folder_name+"'" +" ? -- ")
if(opt.upper() == "YES" or opt.upper() =="Y"):
    delete_folder(folder_name)
else:
    None




