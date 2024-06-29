# Goals

- Place to play with libraries ideas for the python ecosystem


# Extensions

## Pydantic

Given that I want to validate/dumpa a Pydantic model instance from a "row"
format (think of row like data comming from sources like CSV, SQL, XLSX)
When I call `BaseModel#model_dump_row` or `BaseModel.model_validate`
Then it does the thing

