# 21-04-2024-proven-club

Develop a comprehensive RESTful API for a library management system with advanced features like handling book reservations

- Create models for Books, Members, Circulation and Reservation. You may download the 2 datasets below and load to mongodb/mysql/postgresql database based on the database you choose to use for this challenge
    - [**Books](https://drive.google.com/file/d/1YkTIRXYd0FzQsKFGHtzlMmOv2ABlU8Ur/view?usp=sharing) (JSON)**
    - **[Members](https://drive.google.com/file/d/1YKH7YFXDeJOPAd9SlgwYMKLedwjDrJzN/view?usp=sharing) (JSON)**
    - **[Books](https://drive.google.com/file/d/1q1fQCgw2aL1Cx8egnXVgirXebJ8Fogqo/view?usp=sharing) (sql inserts)**
    - **[Members](https://drive.google.com/file/d/1D1E00rAXPG2QS6Wtq7GulN28aJiwPln8/view?usp=sharing) (sql inserts)**
    - Circulation - to include the ‘checkout’ and ‘return’ event types. Checkout is issuing of a book when a member requests for a book to be checked out. Return is the returning of the book
    - Reservation - to ‘reserve’ a book when no copies are available to **checkout** and ‘**fulfill**’ when the copy becomes available (i.e., after it is returned)
- Implement relationships and constraints that handle scenarios like multiple copies of a book, book reservations

1. **API Endpoint(s) for handling book checkouts, returns, reservations and reservation fulfillments** 
- Check out/Issue a book when a copy is available in case of a ‘checkout’ request
- Return a book on a ‘return’ request
- Reserve a book and move to reservation queue when a particular book has no copies available in case of a ‘checkout’ request.
- Fulfill request from the reservation queue once a book is returned and a copy becomes available
- Request Validation and Error handling for edge-cases (e.g. book unavailable but user trying to checkout, etc.)
1. **Optimization:** 
- *Database*
    - **Implement simple/composite indexes on the database columns that help in optimizing the queries for the above APIs.**
- *Caching*
    - **Implement your own caching strategy to avoid unnecessary network calls**

1. **Testing**
    
    Please simulate the below events
    
    1. Checkout
    2. Return
    3. Reserve
    4. Fulfill (Process reservation queue)