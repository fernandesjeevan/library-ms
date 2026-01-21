



from datetime import timedelta,datetime , timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pdb
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "9f3b2e6a7c1d4f8a0b6e2d9c5a1f7e3b8d4c2a6f1e9b0c7d3a5f8b2c6d1e4a9b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": get_password_hash("secret"),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": get_password_hash("secret2"),
        "disabled": True,
    },
}

fake_books_db =  {
  "book": [
    {
      "id": "b001",
      "title": "Clean Code",
      "no_of_pages": 464,
      "genre": "Programming",
      "publication": "Prentice Hall",
      "author": "Robert C. Martin"
    },
    {
      "id": "b002",
      "title": "The Pragmatic Programmer",
      "no_of_pages": 352,
      "genre": "Software Engineering",
      "publication": "Addison-Wesley",
      "author": "Andrew Hunt & David Thomas"
    },
    {
      "id": "b003",
      "title": "Harry Potter and the Philosopher's Stone",
      "no_of_pages": 223,
      "genre": "Fantasy",
      "publication": "Bloomsbury",
      "author": "J.K. Rowling"
    }
  ]
}


app = FastAPI()




def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str|None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

class Book(BaseModel):
    id: str
    title:str
    no_of_pages: int|None = None
    genre: str|None  = None
    publication:str|None = None 
    author: str|None = None

class Books(BaseModel):
    book: list[Book]|None = None

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)



def authenticate_user(fake_db,username:str, password:str):
    print(password, "this is password")
    user = get_user(fake_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user


def create_access_token(data:dict, expires_delta:timedelta|None =None):
    to_encode:dict = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) +expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt  = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
                                          headers ={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM]) 
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    user = get_user(fake_users_db,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],)-> Token:
    #print("does it come here")
    user= authenticate_user(fake_users_db,form_data.username,form_data.password)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers = {"WWW-Authenticate":"Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub":user.username},expires_delta=access_token_expires)
    print(access_token)
    return Token(access_token=access_token,token_type="bearer")


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    print(current_user)
    return current_user

@app.get("/users/me/items")
async def read_own_items(
    current_user:Annotated[User,Depends(get_current_active_user)],
):
    return [{"item_id":"congrats", "owner":current_user.username}]

@app.get("/view/books")
async def view_books():
    books = Books.model_validate(fake_books_db)
    return {"list of books":books}

@app.post("/admin/add/")
async def add_books(book:Book):
    
    obj =Book.model_validate(book)
    books = Books.model_validate(fake_books_db)
    books.book.append(obj)
    return {"updated list":books}

