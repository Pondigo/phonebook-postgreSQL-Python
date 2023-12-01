from fastapi import FastAPI
from config.db import Database
from models.contact import Contact

app = FastAPI()
DATABASE = Database()

# Fetch the results
DATABASE.execute("""CREATE TABLE IF NOT EXISTS public.contacts(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(12) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    fav boolean DEFAULT false,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email))""")

@app.get("/")
async def root():
    return {"message": "Hello"}

# Create
@app.post("/contact")
async def create_contact(new_contact: Contact):
    """
    Create new contact.

    Returns:
        int: The ID created
    
    Raises:
        HTTPException: If there is an error while querying the database. 
    """
    return DATABASE.execute("INSERT INTO contacts (name,phone,email) VALUES ('{}','{}','{}')"
                            .format(new_contact.name,new_contact.phone,new_contact.email))

# Read
@app.get("/contacts")
async def get_contacts():
    """
    Retrieve a list of all contacts.

    Returns:
        List[dict]: A list containing dictionaries representing each contact.
        
    Raises:
        HTTPException: If there is an error while querying the database.
    """
    return DATABASE.query("SELECT * FROM contacts")

# Update
@app.put("/contact/name/{contact_id}")
async def update_contact(contact_updated: Contact, contact_id: str):
    """
    Update the name of a contact.

    Args:
        contact_updated (Contact): The updated contact information.
        contact_id (str): The ID of the contact to be updated.

    Returns:
        dict: A dictionary indicating the success of the update.

    Raises:
        HTTPException: If there is an error while updating the contact.
    """
    return DATABASE.execute("UPDATE contacts SET name='{}' WHERE id={}"
                            .format(contact_updated.name, contact_id))

# Delete
@app.delete("/contact/{contact_id}")
async def delete_contact(contact_id: str):
    """
    Delete a contact.

    Args:
        contact_id (str): The ID of the contact to be deleted.

    Returns:
        dict: A dictionary indicating the success of the deletion.

    Raises:
        HTTPException: If there is an error while deleting the contact.
    """
    return DATABASE.execute("DELETE FROM contacts WHERE id={}"
                            .format(contact_id))
