from enum import Enum

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from src.controller.question_controller import router
from src.embedding.embedding_service import VectorService
from src.prompt.static_prompt import database_analyst_prompt,display_type_prompt,response_prompt
from fastapi.middleware.cors import CORSMiddleware
# template = """Question:{question};Background Knowledge:{knowledge}"""
# prompt = ChatPromptTemplate.from_template(template)
# model = OllamaLLM(model="llama3.2:1b")
# chain = prompt|model
# dialect = "sqlite"


top_k =1

table_info ="""
table name:
    media_types

    column name:
        MediaTypeId:Integer
        name:NVarchar(120)

table name:
    genres

    column name:
        GenreId:Integer
        Name:NVarchar(120)

table name:
    playlists

    column name:
        PlaylistId:Integer ; foreign key of table playlist_track's column playlistId
        Name:NVarchar(120)

table name:
    playlist_track

    column name:
        PlaylistId:Integer
        TrackId:Integer ;foreign key of table tracks' column trackId

table name:
    tracks

    column name:
        trackId:Integer
        Name:Nvarchar(200)
        AlbumId:Integer; foreign key of table albums' column AlbumId
        MediaTypeId:Integer; foreign key of table media_types' column MediaTypeId
        GenreId:Integer ; foreign key of table Genres' column GenreId
        Composer:Nvarchar(220)
        Milliseconds:Integer
        Bytes:Integer
        UnitPrice:Numeric

table name:
    albums

    column name:
        AlbumId:Integer
        Title:Nvarchar(160)
        ArtisId:Integer; foreign key of table artists' column ArtistId

table name:
    artists

    column name:
        ArtistId:Integer
        Name:NVarchar(120)

table name:
    invoices

    column name:
        InvoiceId:Integer
        CustomerId:Integer; foreign key of table customers' column customerId
        InvoiceDate:Datetime
        BillingAddress:NVarchar(120)
        BillingCity:NVarchar(40)
        BillingState:NVarchar(40)
        BillingCountry:Nvarchar(40)
        BillingPostalCode:NVarchar(10)
        Total:Numeric(10,2)

table name:
    invoice_items

    column name:
        invoiceItemId:Integer
        InvoiceId:Integer
        TrackId:Integer; foreign key of table tracks' column trackId
        UnitPrice:Numeric
        Quantity:Integer

table name:
    costumers

    column name:
        customerId:Integer
        firstName:NVarchar(40)
        LastName:Nvarchar(20)
        Company:Nvarchar(80)
        Address:Nvarchar(70)
        City:Nvarchar(40)
        State:Nvarchar(40)
        Country:NVarchar(40)
        PostalCode:NVarchar(40)
        Phone:NVarchar(24)
        Fax:NVarchar(24)
        Email:Nvarchar(60)
        SupportRepId:Integer; foreign key of employees' column EmployeeId

table name:
    employees:

    column name:
        EmployeeId:Integer
        LastName:NVarchar(20)
        FirstName:NVarchar(20)
        Title:NVarchar(30)
        ReportsTo:Integer; It's also related to EmployeeId
        BirthDate:Datetime
        HireDate:Datetime
        Address:Nvarchar(70)
        City:NVarchar(40)
        State:Nvarchar(40)
        Country:NVarchar(40)
        PostalCode:Nvarchar(10)
        Phone:NVarchar(24)
        Fax:NVarchar(24)
        Email:Nvarchar(60)
"""
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应更严格
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)